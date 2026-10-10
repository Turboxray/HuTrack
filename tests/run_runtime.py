"""Build and run the C API/PSG regressions in HuC and HuCC with Mesen 2.

Set HUC_HOME (toolchain root) and MESEN (executable), then run this script.
Generated ROMs, logs and reports stay in tests/.tmp/runtime.
"""
from pathlib import Path
import contextlib
import io
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/.tmp/runtime'
TOOLCHAIN = Path(os.environ.get('HUC_HOME', 'C:/huc'))
MESEN = Path(os.environ.get('MESEN', 'Mesen.exe'))
sys.path.insert(0, str(ROOT/'utils'))
from support.dmfReader import ConvertDeflemask
from support.hutrackLib import HuTrackExportPCE


def macro(values=(), loop=255):
    return bytes([len(values)]) + b''.join(struct.pack('<i', v) for v in values) + (bytes([loop]) if values else b'')


def symbols(path):
    result={};scope=''
    for line in path.read_text().splitlines():
        modern=re.match(r'^([0-9a-fA-F]+):([0-9a-fA-F]+)\s+[0-9a-fA-F]+\s+\S+\s+(\S+)',line)
        if modern:
            bank,address,label=modern.groups();result[label]=(int(bank,16),int(address,16));continue
        m=re.match(r'\s*([0-9a-fA-F-]+)\s+([0-9a-fA-F]+)\s+(\S+)',line)
        if not m:continue
        bank,address,label=m.groups()
        if label.startswith('.'):label=scope+label
        else:scope=label
        result[label]=(int(bank,16) if bank!='-' else None,int(address,16))
    # HuCC's modern symbol format omits local labels; recover linked locations.
    listing=path.with_suffix('.lst')
    if listing.exists():
        scope=''
        for line in listing.read_text(errors='replace').splitlines():
            global_label=re.search(r'\t([A-Za-z_][\w.]*):\s',line)
            if global_label:scope=global_label[1]
            m=re.search(r'\b([0-9A-F]{2}):([0-9A-F]{4})\s+\t([\w.]+):?\s*(?:;.*)?$',line)
            if not m:continue
            bank,address,label=m.groups()
            if label.startswith('.'):
                if scope:result.setdefault(scope+label,(int(bank,16),int(address,16)))
            else:
                scope=label
    return result


def prepare():
    OUT.mkdir(exist_ok=True, parents=True)
    for name, use_pcm in (('constant', False), ('pcm', True), ('cut_pcm', True), ('cut_wave', False), ('wave_changes', False), ('delayed_retrigger', False)):
        speed = 6 if name == 'delayed_retrigger' else 4
        data = b'.DelekDefleMask.' + bytes([24,5,0,0,4,16,0,speed,speed,1,0]) + b'060' + struct.pack('<I',64) + bytes([1]) + bytes(6)
        wave_macro = macro([0,1],0) if name == 'wave_changes' else macro()
        volume_macro = [31,16,0] if name == 'delayed_retrigger' else [31]
        data += bytes([1,0,0]) + macro(volume_macro,0) + macro() + bytes([0]) + macro() + wave_macro
        wave_count = 2 if name == 'wave_changes' else 1
        data += bytes([wave_count])
        for wave_id in range(wave_count):
            data += struct.pack('<I',32) + struct.pack('<32I', *[v ^ (31*wave_id) for v in range(32)])
        for ch in range(6):
            data += bytes([1])
            for row in range(64):
                n, octave, volume, inst = (12,3,31,0) if row == 0 else (0,0,-1,-1)
                fx = (0xee,0 if row == 0 else 255) if ch == 0 and row < 2 else (-1,-1)
                if use_pcm and ch == 5 and row == 0:
                    octave = 0
                    fx = (0x17,1)
                if name.startswith('cut_') and ch == 5 and row == 1:
                    fx = (0xec,1)
                if name == 'delayed_retrigger' and ch == 5:
                    if row in (0,2):
                        fx = (0x0c,1)
                    elif row == 1:
                        n, octave, fx = 12,4,(0xed,3)
                data += struct.pack('<6h', n, octave, volume, *fx, inst)
        if use_pcm:
            samples = [-16000,16000] * 12000
            data += bytes([1]) + struct.pack('<I', len(samples)) + bytes([0,1,5,50,16]) + struct.pack('<'+'h'*len(samples), *samples)
        else:
            data += bytes([0])
        path = OUT / (name+'.dmf')
        path.write_bytes(zlib.compress(data))
        params = dict(filein=str(path), songName=name, subFolder=name, destinationPath=str(OUT),
                      includePath='', debug=False, no_songname=False, no_author=False,
                      playback='6960', resampleFilter='kaiser_best')
        with contextlib.redirect_stdout(io.StringIO()):
            ok, song = ConvertDeflemask(params).process()
            assert ok
            HuTrackExportPCE(song, params).process()
    def db(name, values):
        text = ''.join(' .db '+','.join(str(x) for x in values[i:i+32])+'\n' for i in range(0,len(values),32))
        (OUT/name).write_text(text, encoding='utf-8')
    db('sfx_waves.inc', [31]*16+[0]*16)
    db('sfx_a.inc', [0x9f,0xa5,0x39,0xb0,0,0xc1,0x80,0xfe,100,0xfb])
    db('pcm_cross.inc', [0,0,0]+list(range(32))*625+[0x81])
    db('pcm_short.inc', [0,0,0,16,31,0,16,128])
    db('pcm_empty.inc', [0,0,0,128])
    db('pcm_empty_repeat.inc', [0,0,0,129])
    program = (ROOT/'tests/runtime_controls.c').read_text(encoding='utf-8')
    for compiler in ('huc', 'hucc'):
        folder = OUT/compiler
        folder.mkdir(exist_ok=True)
        for p in (ROOT/'example'/compiler/'main').iterdir():
            if p.suffix in ('.inc', '.asm'):
                shutil.copyfile(p, folder/p.name)
        shutil.copyfile(ROOT/'tests/runtime_assembly.inc', folder/'runtime_assembly.inc')
        standalone = (ROOT/'lib/HuSFX/HuSFX_lib.asm').read_text(encoding='utf-8')
        (folder/'runtime_standalone.inc').write_text('HuSFX.process\n' + standalone.split('\nHuSFX.process\n', 1)[1], encoding='utf-8')
        config = folder/('libslot1.asm' if compiler == 'huc' else 'hucc-final-extra.asm')
        with config.open('a', encoding='utf-8') as output:
            output.write('\n .include "runtime_assembly.inc"\n')
        (folder/'controls.c').write_text(re.sub(r'vsync\((\d+)\)', r'ticks(\1)', program), encoding='utf-8')


def run(compiler, inject_failure=None):
    folder=OUT/compiler
    env=dict(os.environ,PCE_INCLUDE=os.pathsep.join(map(str, (ROOT/'lib', OUT, TOOLCHAIN/'include'/compiler))),
             PCE_BINPATH=str(TOOLCHAIN/'bin'),PCE_PCEAS=str(TOOLCHAIN/'bin/pceas.exe'))
    r=subprocess.run([str(TOOLCHAIN/'bin'/(compiler+'.exe')),'-v','-v','-msmall','-fno-recursive','controls.c',
                      '-T' if compiler=='huc' else '-gL'],cwd=folder,env=env,capture_output=True,text=True)
    (folder/'build.log').write_text(r.stdout+r.stderr)
    assert r.returncode==0,r.stdout+r.stderr
    sym=symbols(folder/'controls.sym');a=lambda n:sym[n][1]
    report=folder/('result.json' if inject_failure is None else f'failure_{inject_failure}.json')
    report.unlink(missing_ok=True)
    lua='''local n=0
local marks=0
local lastStage=0
local once=false
local ticks=0
local rows=0
local selectedChannel=0
local edgeBytes=nil
local cutWrites=nil
local panHardware={}
local lfoControl=0
local musicLimit=nil
local musicWaveWrites=0
local retriggerCheck=false
local delayedTicks=0
local emptyRows=0
local masterControl=0
local failed=false
local function checked(callback)
  return function(...)
    if failed then return end
    local ok,message=pcall(callback,...)
    if not ok then
      failed=true
      local f=io.open(@report@,'w')
      if f then f:write('FAILED: '..tostring(message));f:close() end
      emu.log('TEST FAILURE: '..tostring(message))
      emu.stop(1)
    end
  end
end
local function r(a) return emu.read(a,emu.memType.pceDebug) end
local function w(a) return r(a)+256*r(a+1) end
local function mapped(page,bank) return emu.getState()['memoryManager.mpr['..page..']']==bank end
local function on(ch) return emu.getState()['psg.channels['..ch..'].enabled'] end
local function amp(ch) return emu.getState()['psg.channels['..ch..'].amplitude'] end
local function silence() for ch=0,4 do assert(not on(ch),'music sounding, stage '..lastStage..' ch '..ch) end end
local function sound() for ch=0,4 do assert(on(ch),'music silent, stage '..lastStage..' ch '..ch) end end
emu.addMemoryCallback(checked(function(address,value)
  @writeFault@
  if address==0x800 then selectedChannel=value%8 end
  if address==0x805 then panHardware[selectedChannel]=value end
  if address==0x801 then masterControl=value end
  if address==0x809 then lfoControl=value end
  if musicLimit and address==0x804 and value>=128 then
    assert(value%32<=musicLimit,'wave update exceeded music volume: '..value%32)
  end
  if musicLimit and address==0x806 then musicWaveWrites=musicWaveWrites+1 end
  if address==0x806 and selectedChannel==5 and edgeBytes then table.insert(edgeBytes,value) end
  if address==0x806 and selectedChannel==5 and cutWrites then cutWrites=cutWrites+1 end
end),emu.callbackType.write,0x800,0x809)
emu.addMemoryCallback(checked(function() if mapped(@oncePage@,@onceBank@) then once=true end end),emu.callbackType.exec,@once@)
emu.addMemoryCallback(checked(function() if once and mapped(@enginePage@,@engineBank@) then ticks=ticks+1 end end),emu.callbackType.exec,@engine@)
emu.addMemoryCallback(checked(function() if once and mapped(@parserPage@,@parserBank@) then rows=rows+1 end end),emu.callbackType.exec,@parser@)
emu.addMemoryCallback(checked(function()
  if once and mapped(@endPage@,@endBank@) then
    assert(rows==64 and ticks==260,'last row truncated: '..rows..' rows, '..ticks..' ticks')
    once=false
  end
end),emu.callbackType.exec,@end@)
emu.addMemoryCallback(checked(function()
  if emu.getState()['memoryManager.mpr[@checkpointpage@]']~=@checkpointbank@ then return end
  lastStage=w(@stage@);marks=marks+1
  @checkpointFault@
  if lastStage==37 then assert(not on(5),'EC01 did not silence channel');cutWrites=0 end
  if lastStage==38 then
    assert(cutWrites==0,'PCM writes after EC01: '..tostring(cutWrites));cutWrites=nil
    assert(on(4),'EC01 stopped unrelated SFX')
  end
  if lastStage==39 then assert(panHardware[5]==r(@panSetting@+5),'persistent SFX pan lost after reservation') end
  if lastStage==40 then assert(lfoControl==1,'unrelated stop changed LFO') end
  if lastStage==41 then assert(lfoControl==0,'SFX stop left LFO enabled') end
  if lastStage==42 or lastStage==44 then musicLimit=lastStage==42 and 0 or 15;musicWaveWrites=0 end
  if lastStage==43 then assert(musicWaveWrites>=64,'wave macro was not exercised');musicLimit=nil end
  if lastStage==45 then retriggerCheck=true;delayedTicks=0;emptyRows=0 end
  if lastStage==46 then
    assert(delayedTicks==3 and emptyRows>0,'delayed and empty rows were not exercised')
    retriggerCheck=false
  end
  if lastStage>=47 and lastStage<=49 then
    local expected=({[47]=0x35,[48]=0xa6,[49]=0xff})[lastStage]
    assert(masterControl==expected and r(@global@)==expected,'master-volume ABI failed')
  end
  if lastStage==36 then edgeBytes={} end
  if lastStage==32 and edgeBytes then
    assert(#edgeBytes==4,'incorrect bank-crossing PCM length: '..#edgeBytes)
    for i,v in ipairs({31,1,16,0}) do assert(edgeBytes[i]==v,'incorrect bank-crossing sample') end
    edgeBytes=nil
  end
  if lastStage==1 or lastStage==3 then sound();assert(on(5)) end
  if lastStage==2 or lastStage==4 or lastStage==14 or lastStage==17 then silence();assert(not on(5)) end
  if lastStage==5 or lastStage==7 then assert(on(5));assert(amp(5)==31) end
  if lastStage==6 then sound();assert(not on(5),'SFX release resurrected held note') end
  if lastStage==26 then assert(on(5));assert(not emu.getState()['psg.channels[5].noiseEnabled'],'assembly PCM left noise enabled') end
  if lastStage==30 then assert(on(5));assert(emu.getState()['psg.channels[5].ddaEnabled']) end
  if lastStage==31 then
    assert(on(5));assert(not emu.getState()['psg.channels[5].ddaEnabled'],'waveform still in DDA mode')
    local state=emu.getState()
    for i=0,31 do
      local value=state['psg.channels[5].waveRam['..i..']']
      if value==nil then value=state['psg.channels[5].waveData'..i] end
      assert(value==(i<16 and 31 or 0),'waveform damaged by PCM')
    end
  end
  if lastStage==32 then assert(not on(5),'finished PCM still sounds') end
  if lastStage>=33 and lastStage<=35 then
    assert(on(5));assert(emu.getState()['psg.channels[5].ddaEnabled'])
    assert(amp(5)==({[33]=19,[34]=3,[35]=0})[lastStage],'PCM stream volume lost')
  end
  if lastStage>=8 and lastStage<=13 then
    assert(on(5),'fade touched SFX');assert(amp(5)==31,'fade scaled SFX')
    if lastStage==8 then for ch=0,4 do assert(amp(ch)==15,'gain failed') end end
    if lastStage==9 then for ch=0,4 do assert(amp(ch)==0,'fade failed') end end
    if lastStage==10 or lastStage==12 then sound(); for ch=0,4 do assert(amp(ch)==31) end end
    if lastStage==11 or lastStage==13 then silence() end
    assert(r(@global@)==0x97,'music gain changed master gain')
  end
  if lastStage>=18 and lastStage<=25 then
    assert(on(5),'SFX group stopped stream')
    local expected=({[18]=19,[19]=3,[20]=15,[21]=9,[22]=9,[23]=9,[24]=0,[25]=31})[lastStage]
    assert(amp(5)==expected,'SFX group mix '..amp(5)..' expected '..expected)
    if lastStage>=21 then
      assert(on(4) and amp(4)==expected,'PCM group volume failed')
      if lastStage>=22 then
        for ch=0,3 do assert(on(ch) and amp(ch)==(lastStage==22 and 31 or 15),'SFX volume changed music') end
      end
    end
    assert(r(@global@)==0x97,'SFX gain changed master gain')
  end
end),emu.callbackType.exec,@checkpoint@)
emu.addEventCallback(checked(function()
 n=n+1
 if retriggerCheck then
  local row=r(@rowPosition@+5)
  if r(@rowDelay@+5)>0 then
    delayedTicks=delayedTicks+1
    assert(r(@retriggerSpeed@+5)==1 and amp(5)==31,'ED cleared previous retrigger too soon')
  elseif row==2 or row==4 then
    assert(r(@retriggerSpeed@+5)==0,'completed/empty row kept previous retrigger')
    if row==4 then emptyRows=emptyRows+1 end
  end
 end
 if w(@done@)~=0 or w(@error@)~=0 or n>=1500 then
  local f=assert(io.open(@report@,'w'))
  f:write(string.format('{"frames":%d,"done":%d,"error":%d,"checks":%d,"marks":%d,"stage":%d,"endFrame":%d}',n,w(@done@),w(@error@),w(@checks@),marks,lastStage,w(@frame@)))
  f:close();emu.stop(0)
 end
end),emu.eventType.endFrame)
'''
    for kind in ('write','checkpoint'):
        lua=lua.replace('@'+kind+'Fault@', f"assert(false,'FORCED_{kind}_FAILURE')" if inject_failure==kind else '')
    for n in ('stage','done','error','checks','frame','checkpoint'):
        lua=lua.replace('@'+n+'@',str(a('_'+n)))
    lua=lua.replace('@global@',str(a('HuTrack.Global.SetVolume'))).replace('@report@',json.dumps(report.as_posix()))
    lua=lua.replace('@panSetting@',str(a('HuSFX.vol.pan')))
    for key,label in [('rowPosition','HuTrack.channel.rowPos'),('rowDelay','HuTrack.P.rowDelay'),('retriggerSpeed','HuTrack.P.retrigSpeed')]:
        lua=lua.replace('@'+key+'@',str(a(label)))
    lua=lua.replace('@checkpointpage@',str(a('_checkpoint')>>13)).replace('@checkpointbank@',str(sym['_checkpoint'][0]))
    for n,label in [('once','_HuTrackEngine_PlayOnce.1'),('engine','HuTrackEngine.EngineCall'),
                    ('parser','HuTrackEngine.Parser'),('end','HuTrackEngine.EndSong')]:
        lua=lua.replace('@'+n+'@',str(a(label)))
        lua=lua.replace('@'+n+'Page@',str(a(label)>>13)).replace('@'+n+'Bank@',str(sym[label][0]))
    script=folder/('validate.lua' if inject_failure is None else f'failure_{inject_failure}.lua');script.write_text(lua)
    r=subprocess.run([str(MESEN),'--testrunner','--timeout=30','--enableStdout','--debug.scriptwindow.allowioosaccess=true',
                      str(script),str(folder/'controls.pce')],cwd=ROOT,capture_output=True,text=True,timeout=40)
    (folder/'emulator.log').write_text(r.stdout+r.stderr)
    if report.exists() and report.read_text().startswith('FAILED:'):
        raise RuntimeError(report.read_text())
    assert r.returncode==0 and report.exists(),r.stdout+r.stderr
    assert not re.search(r'\b(?:error|uninitialized)\b', r.stdout+r.stderr, re.I), r.stdout+r.stderr
    result=json.loads(report.read_text());print(compiler,result,flush=True)
    music=sym['HuTrack.CodeEnd'][1]-sym['HuTrackEngine.Parser'][1]
    fixed=sym['HuTrack.FixedCodeEnd'][1]-sym['HuTrack.FixedCodeStart'][1]
    assert 0 < music <= 8192 and sym['HuTrack.CodeEnd'][0] == sym['HuTrackEngine.Parser'][0]
    assert sym['HuTrack.FixedCodeEnd'][0] == sym['HuTrack.FixedCodeStart'][0]
    print(f'{compiler}: music code {music}/8192 bytes, fixed code {fixed} bytes')
    assert result['done']==1 and result['error']==0 and result['checks']==415 and result['marks']==113,result
    return result
if __name__=='__main__':
    if not MESEN.is_file():
        raise SystemExit('Set MESEN to your Mesen 2 executable before running this test.')
    for tool in ('huc', 'hucc', 'pceas'):
        if not (TOOLCHAIN/'bin'/(tool+'.exe')).is_file():
            raise SystemExit('Set HUC_HOME to your HuC/HuCC 4.x toolchain root.')
    prepare()
    for compiler in ('huc','hucc'):run(compiler)
    if '--check-failure-paths' in sys.argv:
        for compiler in ('huc','hucc'):
            for kind in ('write','checkpoint'):
                try:
                    run(compiler, inject_failure=kind)
                except RuntimeError as failure:
                    assert f'FORCED_{kind}_FAILURE' in str(failure), failure
                    print(f'{compiler}: forced {kind} assertion correctly rejected')
                else:
                    raise AssertionError(f'{compiler}: ignored forced {kind} assertion')
