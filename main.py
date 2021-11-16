import re, os, sys
import glob
import ffmpeg

'''

dev.lst file formatting:
...
- [ ] 0905 31-38
- [ ] 0907 01-05; 07-16; 17-22; 22-35; 54-60; 98-103; 109-112; 120-125;
...

'''

class NoTrailingSlash(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

try:
    work_dir = sys.argv[1]
    if work_dir[-1] != '/':
        raise NoTrailingSlashError('[ERROR] No slash in path!')
except IndexError:
    print('Need to pass working directory!')
except NoTrailingSlashError:
    print('Error with path!')


vids_one_fragment_re = r'^- \[ \] (\d{4}) (\d{1,2}-\d{2})$'
vids_multiple_re = r'^- \[ \] (\d{4})(\s\d{1,4}-\d{1,4};)+'
try:
    for l in open('%sdev.lst' % work_dir, 'r').readlines():
        res = re.search(vids_one_fragment_re, l)
        res_m = re.search(vids_multiple_re, l)
        if res:
            file_number = res.group(1)
            filename = '%sIMG_%s.MOV' % (work_dir, file_number)
            start = res.group(2).split('-')[0]
            end = res.group(2).split('-')[1]
            try:
                path_to_chk = '%sIMG_%s_cut_%s_%s.MOV' % (work_dir, file_number, start, end)
                print(path_to_chk)
                # if not os.path.isfile(path_to_chk):
                    # ffmpeg.input(filename).filter('trim', start=start, end=end).output('%sIMG_%s_cut_%s_%s.mov' % (work_dir, file_number, start, end)).run()
            except ffmpeg._run.Error:
                print('No such file! %s' % 'IMG_%s.MOV' % res.group(1))
        elif res_m:
            print(res_m)
except FileNotFoundError:
    print('Need the "dev.lst" file with videos descriptions!')

