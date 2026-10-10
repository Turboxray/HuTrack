"""Play every replacement track through its loop in HuC, HuCC and PCEAS.

Requires the installed 4.x toolchain and MESEN, like run_pcm_examples.py.
Exercises the actual menus and banked assets; output stays in tests/.tmp.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

from run_pcm_examples import symbols

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/.tmp/music-examples'
MESEN = Path(os.environ.get('MESEN', 'Mesen.exe'))


def run(compiler):
    folder = ROOT/'example'/compiler/'main'
    output = OUT/compiler
    output.mkdir(parents=True, exist_ok=True)
    script = {'huc':'build_huc_v4.bat', 'hucc':'build_hucc.bat', 'pceas':'build_asm_rom.bat'}[compiler]
    build = subprocess.run(['cmd.exe','/d','/c',str(folder/script)], cwd=ROOT,
                           capture_output=True, text=True, timeout=30)
    (output/'build.log').write_text(build.stdout+build.stderr, encoding='utf-8')
    assert build.returncode == 0, build.stdout+build.stderr
    sym = symbols(folder/(compiler+'_example.sym'))
    report = output/'result.json'
    report.unlink(missing_ok=True)
    lua = '''local n=0
local stage=0
local start=0
local previous=0
local visited={}
local audible={}
local noiseFrames=0
local pcmWrites=0
local selected=0
local controls={0,0,0,0,0,0}
local titles={'Air Zonk - Aqua Base','The Legendary Axe - Level 2','Aero Blasters - Seaside Front',"Bonk's Adventure - Round 1"}
local orderCounts={22,11,18,8}
local loopRows={5534,2688,4480,2048}
local pcmChannels={5,-1,-1,0}
local noiseChannels={-1,4,4,-1}
local results={}
local failed=false
local finished=false
local function r(a) return emu.read(a,emu.memType.pceDebug) end
local function title()
  local s=''
  for i=0,47 do
    local v=r(@TITLE@+i)
    if v==0 then return s end
    s=s..string.char(v)
  end
  error('unterminated title')
end
local function guarded(fn)
  return function(...)
    if failed or finished then return end
    local ok,message=pcall(fn,...)
    if not ok then
      failed=true
      local f=assert(io.open(@REPORT@,'w'))
      f:write('FAILED: '..tostring(message));f:close()
      emu.log(tostring(message));emu.stop(1)
    end
  end
end
emu.addEventCallback(guarded(function()
  local elapsed=n-start
  emu.setInput({up=stage>=1 and stage<=4 and elapsed>=2 and elapsed<10,
    i=(@IS_C@ and ((stage==0 and n>=60 and n<65) or (stage>=1 and stage<=4 and elapsed>=18 and elapsed<23))) or (stage==5 and elapsed>=10 and elapsed<15),
    down=false,left=false,right=false,ii=false,run=false,select=false},0)
end),emu.eventType.inputPolled)
local function nextSong()
  stage=stage+1;start=n;previous=0;visited={};audible={};noiseFrames=0;pcmWrites=0
  for ch=0,5 do visited[ch]={};audible[ch]=0 end
end
local function finish()
  finished=true
  local f=assert(io.open(@REPORT@,'w'))
  f:write('['..table.concat(results,',')..']');f:close();emu.stop(0)
end
emu.addMemoryCallback(guarded(function(a,v)
  if a==0x800 then selected=v%8 end
  if a==0x804 and selected<6 then controls[selected+1]=v end
  local channel=stage==5 and 5 or pcmChannels[stage]
  if a==0x806 and selected==channel and controls[selected+1]>=0xc0 then pcmWrites=pcmWrites+1 end
end),emu.callbackType.write,0x800,0x806)
local function tick()
  n=n+1
  if n==100 then
    assert(r(@SLOTS@)==5,'expected SMB3 plus four game tracks')
    assert(r(@PLAYBACK@)==1,'SMB3 did not start')
    assert(r(@FORMAT@)==0,'existing SMB3 asset unexpectedly changed')
    nextSong()
  end
  if stage<1 then return end
  local elapsed=n-start
  if stage==5 then
    if elapsed>=100 then
      assert(pcmWrites>100,'relocated PCEAS SFX sample did not play')
      finish()
    end
    return
  end
  if elapsed<40 then return end
  assert(title()==titles[stage],'wrong menu song: '..title())
  assert(r(@PLAYBACK@)==1,'playback stopped during '..titles[stage])
  assert(r(@FORMAT@)==1,'new song is not using banked assets')
  local count=orderCounts[stage]
  assert(r(@ORDERS@)==count,'wrong order count')
  local s=emu.getState()
  for ch=0,5 do
    local order=r(@ORDER@+ch)
    assert(order<count,'order escaped song data')
    visited[ch][order]=true
    if s['psg.channels['..ch..'].enabled'] and s['psg.channels['..ch..'].amplitude']>0 then
      audible[ch]=audible[ch]+1
    end
  end
  local noise=noiseChannels[stage]
  if noise>=0 and s['psg.channels['..noise..'].noiseEnabled'] and s['psg.channels['..noise..'].amplitude']>0 then noiseFrames=noiseFrames+1 end
  local order=r(@ORDER@)
  if previous==count-1 and order==0 then
    for ch=0,5 do
      for i=0,count-1 do assert(visited[ch][i], 'missing order '..i..' on channel '..ch) end
      if stage==3 and ch==5 then
        assert(audible[ch]==0,'Aero Blasters unused channel retained previous song audio')
      else
        assert(audible[ch]>100, 'channel '..ch..' was silent')
      end
    end
    if noise>=0 then assert(noiseFrames>100,'missing noise percussion') end
    if pcmChannels[stage]>=0 then assert(pcmWrites>1000,'missing PCM percussion')
    else assert(pcmWrites==0,'unexpected PCM output') end
    assert(math.abs(elapsed-loopRows[stage])<40,'wrong loop duration')
    results[#results+1]=string.format('{"title":"%s","frames":%d,"orders_per_channel":%d,"noise_frames":%d,"pcm_writes":%d}',titles[stage],elapsed,count,noiseFrames,pcmWrites)
    if stage==4 then
      if @IS_C@ then finish() else nextSong() end
    else
      nextSong()
    end
    return
  end
  previous=order
  assert(elapsed<loopRows[stage]+100,'song never looped')
end
emu.addEventCallback(guarded(tick),emu.eventType.endFrame)
'''
    for key,label in {'TITLE':'HuTrack.songName', 'SLOTS':'song_slot', 'PLAYBACK':'HuTrack.playbackState',
                      'FORMAT':'HuTrack.song.format', 'ORDERS':'HuTrack.patternListlen',
                      'ORDER':'HuTrack.channel.pattern.num'}.items():
        lua=lua.replace('@'+key+'@',str(sym[label][1]))
    lua=lua.replace('@REPORT@',json.dumps(report.as_posix())).replace('@IS_C@','false' if compiler=='pceas' else 'true')
    script=output/'validate.lua'
    script.write_text(lua,encoding='utf-8')
    result=subprocess.run([str(MESEN),'--testrunner','--timeout=90','--enableStdout',
                           '--debug.scriptwindow.allowioosaccess=true','--pcengine.port1.type=PceController',
                           str(script),str(folder/(compiler+'_example.pce'))],
                          cwd=ROOT,capture_output=True,text=True,timeout=100)
    (output/'emulator.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    details=report.read_text() if report.exists() else 'No report was written'
    assert result.returncode==0 and not details.startswith('FAILED'),details+'\n'+result.stdout+result.stderr
    assert not re.search(r'\b(?:error|uninitialized)\b',result.stdout+result.stderr,re.I),result.stdout+result.stderr
    data=json.loads(details)
    assert len(data)==4 and [row['title'] for row in data]==[
        'Air Zonk - Aqua Base', 'The Legendary Axe - Level 2',
        'Aero Blasters - Seaside Front', "Bonk's Adventure - Round 1"],data
    print(compiler,json.dumps(data),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler',choices=('huc','hucc','pceas'))
    args=parser.parse_args()
    if not MESEN.is_file():
        raise SystemExit('Set MESEN to your Mesen 2 executable.')
    for compiler in (args.compiler,) if args.compiler else ('huc','hucc','pceas'):
        run(compiler)
