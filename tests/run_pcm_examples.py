"""Build both PCM sample-ID demos; verify waveform output and PCM envelopes.

Requires the same HuC/HuCC toolchain and Mesen setup as run_runtime.py.
Generated logs and scripts stay under tests/.tmp/pcm-examples.
"""
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/.tmp/pcm-examples'
MESEN = Path(os.environ.get('MESEN', 'Mesen.exe'))


def symbols(path):
    """Read global labels from either compiler's PCEAS symbol format."""
    result = {}
    for line in path.read_text().splitlines():
        match = re.match(r'^([\da-fA-F]+):([\da-fA-F]+)\s+[\da-fA-F]+\s+\S+\s+(\S+)', line)
        if not match:
            match = re.match(r'\s*([\da-fA-F-]+)\s+([\da-fA-F]+)\s+(\S+)', line)
        if match:
            bank, address, label = match.groups()
            result[label] = (int(bank, 16) if bank != '-' else None, int(address, 16))
    return result


def run(compiler):
    project = ROOT / 'example' / (compiler + '_pcm_sample_ids')
    folder = project / 'main'
    output = OUT / compiler
    output.mkdir(parents=True, exist_ok=True)
    build = subprocess.run(['cmd.exe', '/d', '/c', str(folder / ('build_' + compiler + '.bat'))],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
    (output / 'build.log').write_text(build.stdout + build.stderr, encoding='utf-8')
    assert build.returncode == 0, build.stdout + build.stderr
    sym = symbols(folder / 'pcm_sample_ids.sym')
    source = (folder / 'pcm_sample_ids.c').read_text(encoding='utf-8')
    stream = re.search(r'const char pcm_then_wave_sfx\[\] = \{(.*?)\};', source, re.S)[1]
    wave_id = int(re.search(r'HuChanWFupdate\((\d+)\)', stream)[1])
    values = []
    for line in (project / 'assets/sfx/main.wf.inc').read_text(encoding='utf-8').splitlines():
        line = line.split(';', 1)[0]
        if '.db' in line:
            values.extend(int(v, 16) for v in re.findall(r'\$([\da-fA-F]+)', line))
    expected_wave = values[32 * wave_id:32 * (wave_id + 1)]
    assert len(expected_wave) == 32
    report = output / 'result.json'
    report.unlink(missing_ok=True)
    lua = '''local n=0
local pcmFrames=0
local waveFrames=0
local lateWrites=0
local selectedChannel=0
local periodLow=0
local periodHigh=0
local expected={@WAVE@}
local envelopeLevels={12,20,27,31,27,23,19,15,11,7,3,0}
local envelopeDurations={6,6,6,36,12,12,12,12,12,12,12,6}
local envelopeFrames=0
local envelopeStage=1
local stageFrames=0
local lastPosition=nil
local silentWrites=0
local function r(a) return emu.read(a,emu.memType.pceDebug) end
local function w(a) return r(a)+256*r(a+1) end
emu.addMemoryCallback(function(address,value)
  if address==0x800 then selectedChannel=value%8 end
  if selectedChannel~=5 then return end
  if address==0x802 then periodLow=value end
  if address==0x803 then periodHigh=value%16 end
  if address==0x806 and waveFrames>0 and n<160 then lateWrites=lateWrites+1 end
  if address==0x806 and n>=180 and n<360 and envelopeStage==12 then
    silentWrites=silentWrites+1
  end
end,emu.callbackType.write,0x800,0x806)
emu.addEventCallback(function()
  emu.setInput({i=n==40 or n==180 or n==400,ii=n==410,
    left=n==370 or n==380 or n==390,right=n==30 or n==170 or n==430,
    up=false,down=false,run=false,select=false},0)
end,emu.eventType.inputPolled)
local function tick()
  n=n+1
  if n==25 then
    assert(w(@READY@)==1,'sample registration failed')
    assert(w(@ID0@)==0 and w(@ID1@)==1 and w(@ID2@)==2,'wrong registered IDs')
  end
  if n==35 then assert(w(@SELECTED@)==1,'PCM + waveform menu selection failed') end
  if n==175 then assert(w(@SELECTED@)==2,'PCM envelope menu selection failed') end
  local s=emu.getState()
  local enabled=s['psg.channels[5].enabled']
  local dda=s['psg.channels[5].ddaEnabled']
  if enabled and dda and n<160 then pcmFrames=pcmFrames+1 end
  if enabled and not dda and n<160 then
    assert(pcmFrames>0,'waveform was not preceded by PCM')
    assert(w(@ACTIVE@)==1,'waveform playing outside active effect')
    assert(s['psg.channels[5].amplitude']==31,'waveform volume is not maximum')
    assert(s['psg.channels[5].leftVolume']>0 and s['psg.channels[5].rightVolume']>0,'waveform pan is muted')
    assert(not s['psg.channels[5].noiseEnabled'],'noise mode left enabled')
    assert(periodLow+256*periodHigh==0x140,'wrong waveform period')
    assert(r(@INACTIVE@+5)==128,'PCM writer still active')
    local low=31
    local high=0
    for i=0,31 do
      local v=s['psg.channels[5].waveRam['..i..']']
      if v==nil then v=s['psg.channels[5].waveData'..i] end
      assert(v==expected[i+1],'waveform upload mismatch at sample '..i..': got '..tostring(v)..', expected '..expected[i+1]..', frame '..n)
      low=math.min(low,v)
      high=math.max(high,v)
    end
    assert(high>low,'PCM + waveform example selected a constant (silent) waveform')
    waveFrames=waveFrames+1
  end
  if n==160 then
    assert(pcmFrames>0 and waveFrames==30,'missing or truncated PCM/waveform playback')
    assert(lateWrites==0,'PCM overwrote the waveform after upload')
    assert(w(@ACTIVE@)==0 and not enabled,'effect failed to stop')
    assert(r(@RESERVED@+5)==0,'channel was not released')
  end
  if n>=180 and n<360 and w(@ACTIVE@)==1 and r(@OWNED@+5)==1 then
    assert(enabled and dda,'envelope changed away from enabled PCM mode')
    assert(r(@INACTIVE@+5)==0,'envelope stopped its PCM early')
    if stageFrames==envelopeDurations[envelopeStage] then
      envelopeStage=envelopeStage+1
      stageFrames=0
    end
    assert(envelopeStage<=#envelopeLevels,'envelope ran longer than scheduled')
    assert(s['psg.channels[5].amplitude']==envelopeLevels[envelopeStage],
      'wrong envelope volume at update '..envelopeFrames..': '..tostring(s['psg.channels[5].amplitude']))
    local position=r(@BANK@+5)*8192+(r(@HI@+5)%32)*256+r(@LO@+5)
    if lastPosition then
      assert(position>lastPosition and position-lastPosition<256,
        'volume command restarted, stalled or skipped PCM')
    end
    lastPosition=position
    stageFrames=stageFrames+1
    envelopeFrames=envelopeFrames+1
  end
  if n==360 then
    assert(envelopeFrames==144 and envelopeStage==12 and stageFrames==6,
      'envelope duration or final silent step mismatch')
    assert(silentWrites>0,'silent volume incorrectly paused PCM')
    assert(w(@ACTIVE@)==0 and not enabled,'envelope failed to stop')
    assert(r(@RESERVED@+5)==0 and r(@OWNED@+5)==0 and r(@INACTIVE@+5)==128,
      'envelope failed to stop PCM and release ownership')
  end
  if n==395 then assert(w(@SELECTED@)==2,'left menu wrap failed') end
  if n==405 then
    assert(w(@ACTIVE@)==1 and enabled and dda and s['psg.channels[5].amplitude']==12,
      'envelope did not restart at its quiet attack level')
  end
  if n==420 then
    assert(w(@ACTIVE@)==0 and not enabled,'II failed to silence envelope')
    assert(r(@RESERVED@+5)==0 and r(@OWNED@+5)==0 and r(@INACTIVE@+5)==128,
      'II failed to release envelope PCM')
  end
  if n==440 then
    assert(w(@SELECTED@)==0,'right menu wrap failed')
    local f=assert(io.open(@REPORT@,'w'))
    f:write(string.format('{"pcm_frames":%d,"waveform_frames":%d,"late_writes":%d,"envelope_frames":%d,"envelope_steps":%d,"silent_pcm_writes":%d}',
      pcmFrames,waveFrames,lateWrites,envelopeFrames,envelopeStage,silentWrites))
    f:close()
    emu.stop(0)
  end
end
emu.addEventCallback(function()
  local ok,message=pcall(tick)
  if not ok then
    local f=assert(io.open(@REPORT@,'w'))
    f:write('FAILED: '..tostring(message))
    f:close()
    emu.log(tostring(message))
    emu.stop(1)
  end
end,emu.eventType.endFrame)
'''
    for key, label in {
        'READY': '_samples_ready', 'ID0': '_hypercocoon_id',
        'ID1': '_stage_clear_id', 'ID2': '_shubibinman_id',
        'SELECTED': '_selected_example', 'ACTIVE': '_effect_active',
        'INACTIVE': 'HuTrack.dda.inactive', 'RESERVED': 'HuTrack.SFX.inProgress',
        'OWNED': 'HuSFX.pcm.owned', 'BANK': 'HuTrack.dda.bank',
        'LO': 'HuTrack.dda.addr.lo', 'HI': 'HuTrack.dda.addr.hi',
    }.items():
        lua = lua.replace('@' + key + '@', str(sym[label][1]))
    lua = lua.replace('@WAVE@', ','.join(map(str, expected_wave)))
    lua = lua.replace('@REPORT@', json.dumps(report.as_posix()))
    script = output / 'validate.lua'
    script.write_text(lua, encoding='utf-8')
    result = subprocess.run([str(MESEN), '--testrunner', '--timeout=25', '--enableStdout',
                             '--debug.scriptwindow.allowioosaccess=true',
                             '--pcengine.port1.type=PceController', str(script),
                             str(folder / 'pcm_sample_ids.pce')],
                            cwd=ROOT, capture_output=True, text=True, timeout=35)
    (output / 'emulator.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    details = report.read_text() if report.is_file() else 'No emulator report was written.'
    assert result.returncode == 0 and report.is_file(), details + '\n' + result.stdout + result.stderr
    assert not re.search(r'\b(?:error|uninitialized)\b', result.stdout + result.stderr, re.I), result.stdout + result.stderr
    print(compiler, json.loads(report.read_text()), flush=True)


if __name__ == '__main__':
    if not MESEN.is_file():
        raise SystemExit('Set MESEN to your Mesen 2 executable before running this test.')
    for compiler in ('huc', 'hucc'):
        run(compiler)
