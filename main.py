import re, os, sys, glob
from threading import Thread
from multiprocessing import Process
try:
    import ffmpeg
except ModuleNotFoundError:
    print('[FATAL ERROR] No ffmpeg or ffmpeg-python installed!\n \tTo fix this -> run `sudo apt install ffmpeg`,\n \tand then `pip3 install ffmpeg-python`.')
    exit(-1)
'''

dev.lst file formatting:
...
- [ ] 0905 31-38
- [ ] 0907 01-05; 07-16; 17-22; 22-35; 54-60; 98-103; 109-112; 120-125;
...

'''

ffmpeg_threads = []
procs = []
class NoTrailingSlashError(Exception):
    def __init__(self, message):
        self.message = message

def cut_fragment(work_dir, file_number, start, end):
    try:
        res_f = '%sIMG_%s_cut_%s_%s.MOV' % (work_dir, file_number, start, end)
        # raise ffmpeg._run.Error('Info about error here.', stdout=sys.stdout, stderr=sys.stderr)
        if not os.path.isfile(res_f):
            print('Cut video %s' % res_f, file=sys.stdout)
            filename = '%sIMG_%s.MOV' % (work_dir, file_number)
            fmg = ffmpeg.input(filename).filter('trim', start=start, end=end).output(res_f)
            print(fmg.compile(), file=sys.stdout)
            fmg.run()
        else:
            print('File %s exists!' % res_f, file=sys.stdout)
    except ffmpeg._run.Error as e:
        print('[ERROR] IMG_%s.MOV, ffmpeg exception was: %s' % (file_number, e), file=sys.stderr)

    return file_number

try:
    work_dir = sys.argv[1]
    if work_dir[-1] != '/':
        raise NoTrailingSlashError('No slash in path!')
    vids_one_fragment_re = r'^- \[ \] (\d{4}) (\d{1,2}-\d{2})$'
    vids_multiple_re = r'^- \[ \] (\d{4})(( \d{1,4}-\d{1,4};)+)$'
    try:
        l_cnt = 0
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
                        # cut_fragment(work_dir, file_number, start, end)
                        # th = Thread(target=cut_fragment, args=(work_dir, file_number, start, end))
                        # th.start()
                        # ffmpeg_threads += [th]
                        p = Process(target=cut_fragment, args=(work_dir, file_number, start, end))
                        p.start()
                        procs += [p]
            else:
                print('[INFO] Maybe problem with format, check line %s of "dev.lst". \n See README.md for formatting info.' % (l_cnt+1), file=sys.stderr)
            l_cnt += 1
    except FileNotFoundError:
        print('[FATAL ERROR] Need the "dev.lst" file with videos descriptions right in the work_dir!', file=sys.stderr)
except IndexError:
    print('[FATAL ERROR] Need to pass working directory!', file=sys.stderr)
except NoTrailingSlashError as e:
    print('[FATAL ERROR] %s' % e, file=sys.stderr)

# for th in ffmpeg_threads:
    # print('Working...')
    # sleep(1)
    # th.join()

for p in procs:
    print('Working...')
    sleep(1)
    p.join()
