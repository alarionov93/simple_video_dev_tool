import sys
import ffmpeg
from json import load

x = load(open(sys.argv[1], 'r'))
clips = x['clips']

for clip in clips: 
   try:
      ffmpeg
      .input(clip['reader']['path']) 
      .filter('trim', start=clip['start'], end=clip['end']) 
      .output('out_%s.mov' % clip['reader']['path'].split('_')[-1].split('.')[0]) 
      .run(capture_stdout=True)
   except ffmpeg._run.Error as e:
      print('[ERROR] %s, ffmpeg exception was: %s' % (clip['reader']['path'], e), file=sys.stderr)

   # vid = ffmpeg.input('IMG_3057.MOV')
   # res = vid.filter('trim', start=4.4, end=8.23)
   # out = ffmpeg.output(res, 'out_3057.mov')\
   # out.run()