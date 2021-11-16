import re, sys
import glob
import ffmpeg

'''

dev.lst file formatting:
...
- [ ] 0905 31-38
- [ ] 0907 01-05; 07-16; 17-22; 22-35; 54-60; 98-103; 109-112; 120-125;
...

'''


vids_one_fragment_re = r'^- \[ \] (\d{4}) (\d{1,2}-\d{2})$'
vids_multiple_re = r'^- \[ \] (\d{4})(\s\d{1,4}-\d{1,4};)+'

for l in open('dev.lst', 'r').readlines():
    res = re.search(vids_one_fragment_re, l)
    res_m = re.search(vids_multiple_re, l)
    if res:
        file_number = res.group(1)
        start = res.group(2).split('-')[0]
        end = res.group(2).split('-')[1]
        try:
            # ffmpeg.input('IMG_%s.MOV' % file_number)
            # .filter('trim', start=start, end=end)
            # .output('IMG_%s_cut_%s_%s.mov' % (res.group(1), start, end)).run()
            print(file_number)
        except ffmpeg._run.Error:
            print('No such file! %s' % 'IMG_%s.MOV' % res.group(1))
    elif res_m:
        print(res_m)


