"""Build and run HuSFX stream bank-boundary regressions in HuC and HuCC.

Set HUC_HOME (toolchain root) and MESEN (Mesen 2 executable), then run:
    python tests/run_sfx_boundaries.py

Each compiler runs 11 cases through the C-interface and standalone assembly
decoders, with two checkpoints per case (44 total). All fixtures, ROMs, logs,
and reports are generated under tests/.tmp/sfx_boundaries. The optional
--check-failure-paths also verifies that Lua callback errors reach Python.
"""

from dataclasses import dataclass
from pathlib import Path
import argparse
import json
import os
import re
import shutil
import subprocess

from run_runtime import symbols


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/.tmp/sfx_boundaries'
TOOLCHAIN = Path(os.environ.get('HUC_HOME', 'C:/huc'))
MESEN = Path(os.environ.get('MESEN', 'Mesen.exe'))
COMPILERS = ('huc', 'hucc')
DECODERS = ('C interface', 'standalone assembly')


@dataclass(frozen=True)
class Case:
    name: str
    bank: int
    address: int
    data: tuple
    first: dict


# Streams straddle $5fff, placing opcodes or their operands on either side.
# The assembler continues in the next physical bank, mapped back at $4000 by
# the decoder. $fb operands remain data; only $fb fetched as an opcode is EOF.
CASES = (
    Case('wave_opcode', 32, 0x5fff, (0xb0, 0, 0x9f, 0xc1, 0xfb, 0xff, 0xfb),
         {'waveCorrect': True, 'period': 0x1fb, 'control': 0x9f}),
    Case('wave_operand', 34, 0x5ffe, (0xb0, 0, 0x9f, 0xc1, 0xfb, 0xff, 0xfb),
         {'waveCorrect': True, 'period': 0x1fb, 'control': 0x9f}),
    Case('pan_operand', 36, 0x5fff, (0xa5, 0xfb, 0x9f, 0xff, 0xfb),
         {'pan': 0xfb, 'control': 0x9f}),
    Case('period_operand', 38, 0x5fff, (0xc1, 0xfb, 0x9f, 0xff, 0xfb),
         {'period': 0x1fb, 'control': 0x9f}),
    Case('wait_operand', 40, 0x5fff, (0xfe, 0xfb, 0xfb), {}),
    Case('pcm_opcode', 42, 0x5fff, (0xfc, 0, 1, 0xff, 0xfb),
         {'pcmOwned': 1, 'pcmInactive': 0, 'control': 0xdf}),
    Case('pcm_id', 44, 0x5ffe, (0xfc, 0, 1, 0xff, 0xfb),
         {'pcmOwned': 1, 'pcmInactive': 0, 'control': 0xdf}),
    Case('pcm_flag', 46, 0x5ffd, (0xfc, 0, 1, 0xff, 0xfb),
         {'pcmOwned': 1, 'pcmInactive': 0, 'control': 0xdf}),
    Case('raw_control', 48, 0x5fff, (0xa4, 0x20, 0xff, 0xfb),
         {'control': 0x20, 'pcmInactive': 0x80}),
    Case('metadata', 50, 0x5fff, (0xaa, 0xfb, 0x9f, 0xff, 0xfb),
         {'control': 0x9f}),
    Case('eof', 52, 0x5fff, (0xfb, 0x9f, 0xff, 0xfb), {}),
)


def prepare():
    """Generate the ROM harness, waveform, sample, and split-bank streams."""
    program = '''#include "huc.h"
#include "HuTrack/Huc_interface/HuTrack.c"
#include "HuSFX/HuC_interface/HucSFX.c"
#include "HuCsupport/HuCsupport.h"
#asm
.bank HUC_USER_RESERVED
#endasm
#incasmlabel(sfx_waves, "waves.inc", 2);
const char pcm[] = {0,0,0,31,0,16,0x80};
int done,stage,step,decoder;
#pragma fastcall checkpoint();
#pragma fastcall assemblySfx();
void tick(void) {if(decoder)assemblySfx();else HuSFXprocess();}
'''
    program += ''.join(f'extern char {case.name}[];\n' for case in CASES)
    program += '''int main(void) {
    HuTrack_Init();
    HuSFX_Init(getBank(sfx_waves),getAddress(sfx_waves));
    HuSFX_QueuePCM(pcm);
    HuTrackEnginePauseDDA();
    for(decoder=0;decoder<2;decoder++) {
'''
    for stage, case in enumerate(CASES):
        program += f'''        HuTrackEngine_TryReserve(5);
        HuSFXplay(5,getBank({case.name}),getAddress({case.name}));
        stage={stage};
        step=1;tick();checkpoint();
        step=2;tick();checkpoint();
        HuTrackEngine_chanRelease(5);
'''
    program += '    }\n    done=1;\n    while(1)vsync();\n    return 0;\n}\n'

    bridge = '''_checkpoint:
 rts
_assemblySfx:
 tma #6
 pha
 lda #bank(HuSFX.process)
 tam #6
 jsr HuSFX.process
 pla
 tam #6
 rts
 .bank 60
 .org $c000
 .include "standalone.inc"
'''
    for case in CASES:
        split = 0x6000 - case.address
        bridge += f' .bank {case.bank}\n .org ${case.address:04x}\n_{case.name}:\n'
        bridge += ' .db ' + ','.join(map(str, case.data[:split])) + '\n'
        bridge += ' .page 2\n .db ' + ','.join(map(str, case.data[split:])) + '\n'

    # The standalone decoder shares variables/macros with the C interface, but
    # uses its own production instruction stream in an explicitly mapped bank.
    source = (ROOT / 'lib/HuSFX/HuSFX_lib.asm').read_text(encoding='utf-8')
    marker = '\nHuSFX.process\n'
    if source.count(marker) != 1:
        raise RuntimeError('Cannot locate the standalone HuSFX.process entry point')
    standalone = 'HuSFX.process\n' + source.split(marker, 1)[1]

    for compiler in COMPILERS:
        folder = OUT / compiler
        folder.mkdir(parents=True, exist_ok=True)
        for path in (ROOT / 'example' / compiler / 'main').iterdir():
            if path.suffix in ('.inc', '.asm'):
                shutil.copyfile(path, folder / path.name)
        config = folder / ('libslot1.asm' if compiler == 'huc' else 'hucc-final-extra.asm')
        with config.open('a', encoding='utf-8') as output:
            output.write('\n .include "bridge.inc"\n')
        for name, contents in {
            'boundaries.c': program,
            'bridge.inc': bridge,
            'standalone.inc': standalone,
            'waves.inc': ' .db ' + ','.join(map(str, [31] * 16 + [0] * 16)) + '\n',
        }.items():
            (folder / name).write_text(contents, encoding='utf-8')


def build(compiler):
    folder = OUT / compiler
    for suffix in ('.pce', '.sym', '.lst'):
        (folder / ('boundaries' + suffix)).unlink(missing_ok=True)
    env = dict(os.environ,
               PCE_INCLUDE=os.pathsep.join(map(str, (ROOT / 'lib', folder,
                                                     TOOLCHAIN / 'include' / compiler))),
               PCE_BINPATH=str(TOOLCHAIN / 'bin'),
               PCE_PCEAS=str(TOOLCHAIN / 'bin/pceas.exe'))
    result = subprocess.run(
        [str(TOOLCHAIN / 'bin' / (compiler + '.exe')), '-v', '-v', '-msmall',
         '-fno-recursive', 'boundaries.c', '-T' if compiler == 'huc' else '-gL'],
        cwd=folder, env=env, capture_output=True, text=True)
    (folder / 'build.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    if result.returncode != 0:
        raise RuntimeError(f'{compiler} build failed:\n{result.stdout}{result.stderr}')
    if not all((folder / ('boundaries' + suffix)).is_file() for suffix in ('.pce', '.sym')):
        raise RuntimeError(f'{compiler} build did not generate its ROM and symbols')


LUA = '''local n=0
local selected=0
local control=0
local pan=255
local low=0
local high=0
local records={}
local failed=false
local function checked(callback)
 return function(...)
  if failed then return end
  local ok,message=pcall(callback,...)
  if not ok then
   failed=true
   local f=io.open(@REPORT@,'w')
   if f then f:write('FAILED: '..tostring(message));f:close() end
   emu.log('TEST FAILURE: '..tostring(message))
   emu.stop(1)
  end
 end
end
local function r(a) return emu.read(a,emu.memType.pceDebug) end
local function w(a) return r(a)+256*r(a+1) end
emu.addMemoryCallback(checked(function(address,value)
 @WRITE_FAULT@
 if address==0x800 then selected=value%8 end
 if selected~=5 then return end
 if address==0x802 then low=value end
 if address==0x803 then high=value end
 if address==0x804 then control=value end
 if address==0x805 then pan=value end
end),emu.callbackType.write,0x800,0x809)
emu.addMemoryCallback(checked(function()
 if emu.getState()['memoryManager.mpr[@PAGE@]']~=@BANK@ then return end
 @CHECKPOINT_FAULT@
 local wave=true
 local s=emu.getState()
 for i=0,31 do
  local v=s['psg.channels[5].waveRam['..i..']']
  if v==nil then v=s['psg.channels[5].waveData'..i] end
  if v~=(i<16 and 31 or 0) then wave=false end
 end
 records[#records+1]=string.format('{"decoder":%d,"stage":%d,"step":%d,"bank":%d,"delay":%d,"control":%d,"pan":%d,"period":%d,"pcmInactive":%d,"pcmOwned":%d,"waveCorrect":%s}',w(@DECODER@),w(@STAGE@),w(@STEP@),r(@STREAMBANK@+5),r(@DELAY@+5),control,pan,high*256+low,r(@INACTIVE@+5),r(@OWNED@+5),tostring(wave))
end),emu.callbackType.exec,@CHECKPOINT@)
emu.addEventCallback(checked(function()
 @FRAME_FAULT@
 n=n+1
 if w(@DONE@)~=0 then
  local f=assert(io.open(@REPORT@,'w'))
  f:write(string.format('{"done":%d,"frames":%d,"records":[',w(@DONE@),n)..table.concat(records,',')..']}')
  f:close()
  emu.stop(0)
 else
  assert(n<120,'ROM did not finish within 120 frames')
 end
end),emu.eventType.endFrame)
'''


def validate_report(result):
    """Check observed values and require every decoder/case/step exactly once."""
    if not isinstance(result, dict) or result.get('done') != 1:
        raise RuntimeError(f'Boundary ROM did not complete: {result!r}')
    if type(result.get('frames')) is not int or not 1 <= result['frames'] <= 120:
        raise RuntimeError(f'Invalid frame count: {result.get("frames")!r}')
    records = result.get('records')
    if not isinstance(records, list):
        raise RuntimeError('Boundary report is missing its records array')
    expected_keys = {(decoder, stage, step) for decoder in range(len(DECODERS))
                     for stage in range(len(CASES)) for step in (1, 2)}
    seen = set()
    for row in records:
        if not isinstance(row, dict):
            raise RuntimeError(f'Invalid boundary record: {row!r}')
        for field in ('decoder', 'stage', 'step', 'bank', 'delay', 'control',
                      'pan', 'period', 'pcmInactive', 'pcmOwned'):
            if type(row.get(field)) is not int:
                raise RuntimeError(f'Missing or invalid {field}: {row!r}')
        if type(row.get('waveCorrect')) is not bool:
            raise RuntimeError(f'Missing or invalid waveCorrect: {row!r}')
        key = row['decoder'], row['stage'], row['step']
        if key not in expected_keys:
            raise RuntimeError(f'Unexpected boundary checkpoint: {key}')
        if key in seen:
            raise RuntimeError(f'Duplicate boundary checkpoint: {key}')
        seen.add(key)
        decoder, stage, step = key
        case = CASES[stage]
        if case.name == 'wait_operand':
            expected = {'bank': case.bank + 1, 'delay': 251 - step}
        elif step == 2 or case.name == 'eof':
            expected = {'bank': 0xff, 'control': 0, 'pcmInactive': 0x80, 'pcmOwned': 0}
        else:
            expected = {'bank': case.bank + 1, 'delay': 0, **case.first}
        for field, value in expected.items():
            if row[field] != value:
                raise RuntimeError(f'{DECODERS[decoder]} {case.name} step {step}: '
                                   f'{field}={row[field]!r}, expected {value!r}; {row!r}')
    missing = expected_keys - seen
    if missing:
        raise RuntimeError(f'Missing boundary checkpoints: {sorted(missing)}')
    return len(records)


def run(compiler, inject_failure=None):
    folder = OUT / compiler
    sym = symbols(folder / 'boundaries.sym')
    report = folder / ('result.json' if inject_failure is None else f'failure_{inject_failure}.json')
    report.unlink(missing_ok=True)
    mapping = {
        'PAGE': sym['_checkpoint'][1] >> 13,
        'BANK': sym['_checkpoint'][0],
        'REPORT': json.dumps(report.as_posix()),
    }
    for key, label in {
        'CHECKPOINT': '_checkpoint', 'DONE': '_done', 'DECODER': '_decoder',
        'STAGE': '_stage', 'STEP': '_step', 'STREAMBANK': 'HuSFX.stream.bnk',
        'DELAY': 'HuSFX.delay', 'INACTIVE': 'HuTrack.dda.inactive', 'OWNED': 'HuSFX.pcm.owned',
    }.items():
        mapping[key] = sym[label][1]
    for kind in ('write', 'checkpoint', 'frame'):
        mapping[kind.upper() + '_FAULT'] = (
            f"assert(false,'FORCED_{kind}_FAILURE')" if inject_failure == kind else '')
    lua = LUA
    for key, value in mapping.items():
        lua = lua.replace('@' + key + '@', str(value))
    if re.search(r'@[A-Z_]+@', lua):
        raise RuntimeError('Unresolved placeholder in boundary observer')
    stem = 'observe' if inject_failure is None else f'failure_{inject_failure}'
    script = folder / (stem + '.lua')
    script.write_text(lua, encoding='utf-8')
    result = subprocess.run(
        [str(MESEN), '--testrunner', '--timeout=10', '--enableStdout',
         '--debug.scriptwindow.allowioosaccess=true', str(script), str(folder / 'boundaries.pce')],
        cwd=ROOT, capture_output=True, text=True, timeout=20)
    log = result.stdout + result.stderr
    (folder / (stem + '.log')).write_text(log, encoding='utf-8')
    contents = report.read_text(encoding='utf-8') if report.is_file() else ''
    if contents.startswith('FAILED:'):
        raise RuntimeError(contents)
    if result.returncode != 0 or not contents:
        raise RuntimeError(f'{compiler}: emulator failed or produced no report:\n{log}')
    if re.search(r'\b(?:error|uninitialized)\b', log, re.I):
        raise RuntimeError(f'{compiler}: emulator reported an error:\n{log}')
    count = validate_report(json.loads(contents))
    print(f'{compiler}: {len(CASES)} cases, {count} boundary checkpoints passed '
          '(C interface + standalone assembly)', flush=True)
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-failure-paths', action='store_true')
    args = parser.parse_args()
    if not MESEN.is_file():
        raise SystemExit('Set MESEN to your Mesen 2 executable before running this test.')
    for tool in ('huc', 'hucc', 'pceas'):
        if not (TOOLCHAIN / 'bin' / (tool + '.exe')).is_file():
            raise SystemExit('Set HUC_HOME to your HuC/HuCC 4.x toolchain root.')
    prepare()
    for compiler in COMPILERS:
        build(compiler)
        run(compiler)
        if args.check_failure_paths:
            for kind in ('write', 'checkpoint', 'frame'):
                try:
                    run(compiler, inject_failure=kind)
                except RuntimeError as failure:
                    if f'FORCED_{kind}_FAILURE' not in str(failure):
                        raise
                    print(f'{compiler}: forced {kind} callback failure correctly rejected', flush=True)
                else:
                    raise RuntimeError(f'{compiler}: ignored forced {kind} callback failure')


if __name__ == '__main__':
    main()
