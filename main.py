import re, os, sys, glob
import ffmpeg

from threading import Thread

'''

dev.lst file formatting:
...
- [ ] 0905 31-38
- [ ] 0907 01-05; 07-16; 17-22; 22-35; 54-60; 98-103; 109-112; 120-125;
...

'''

class NoTrailingSlashError(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

def cut_fragment(work_dir, file_number, start, end):
    try:
        res_f = '%sIMG_%s_cut_%s_%s.MOV' % (work_dir, file_number, start, end)
        # raise ffmpeg._run.Error('Info about error here.', stdout=sys.stdout, stderr=sys.stderr)
        if not os.path.isfile(res_f):
            print('Cut video %s' % res_f, file=sys.stdout)
            ffmpeg.input(filename).filter('trim', start=start, end=end).output(res_f).run()
        else:
            print('File %s exists!' % res_f, file=sys.stdout)
    except ffmpeg._run.Error as e:
        print('[ERROR] IMG_%s.MOV, exception was:' % (file_number, e), file=sys.stderr)

    return file_number

try:
    work_dir = sys.argv[1]
    if work_dir[-1] != '/':
        raise NoTrailingSlashError('No slash in path!')
except IndexError:
    print('Need to pass working directory!', file=sys.stderr)
except NoTrailingSlashError as e:
    print('[ERROR] %s' % e, file=sys.stderr)


vids_one_fragment_re = r'^- \[ \] (\d{4}) (\d{1,2}-\d{2})$'
vids_multiple_re = r'^- \[ \] (\d{4})(( \d{1,4}-\d{1,4};)+)$'
try:
    for l in open('%sdev.lst' % work_dir, 'r').readlines():
        res = re.search(vids_one_fragment_re, l)
        res_m = re.findall(vids_multiple_re, l)
        if res:
            file_number = res.group(1)
            filename = '%sIMG_%s.MOV' % (work_dir, file_number)
            start = res.group(2).split('-')[0]
            end = res.group(2).split('-')[1]
            cut_fragment(work_dir, file_number, start, end)
        elif res_m:
            for r in res_m:
                file_number = r[0]
                times = [x.strip() for x in r[1].split(';') if len(x) > 0]
                for t in times:
                    (start, end) = (t.split('-')[0], t.split('-')[1])
                    th = Thread(target=cut_fragment, args=(work_dir, file_number, start, end))
                    th.start()

except FileNotFoundError:
    print('Need the "dev.lst" file with videos descriptions!', file=sys.stderr)

