## Simple video dev tool:
- cut fragments of videos in directory by their description;

#### Install:
sudo apt install ffmpeg
#### Format info:
1. "dev.lst" file should be in directory with videos
2. "dev.lst" contents example:
```
...
- [ ] 0905 31-38
- [ ] 0907 01-05; 07-16; 17-22; 22-35; 54-60; 98-103; 109-112; 120-125;
...
```
3. Format description:` - \[ \] {file_number} {start_sec-end_sec}; `

#### Usage:
`python3 main.py /path/to/videos/dir/`

#### Requirements:
`requirements.txt` file, and ffmpeg on your system.


`ffmpeg -i IMG_0907.MOV -filter_complex [0]trim=end=112:start=109[s0] -map [s0] test109112.mov`