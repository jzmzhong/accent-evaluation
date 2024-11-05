
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--norm-level", help="normalisation intensity from 1 to 5", type=int, default=1)
parser.add_argument("--sil", help="silence length (ms)", type=int, default=100)
parser.add_argument("--sil-db", help="silence db threshold", type=int, default=-60)
parser.add_argument("--in-dir", help="input wav folder", type=str)
parser.add_argument("--out-dir", help="output wav folder", type=str)
args = parser.parse_args()

FFMPEG="/work/tc062/tc062/jzmzhong/myvenvs/mymodules/ffmpeg-git-20240629-amd64-static/ffmpeg"

NORM_CMDS = {
    1: "speechnorm=e=3:r=0.00001:l=1",
    2: "speechnorm=e=6.25:r=0.00001:l=1",
    3: "speechnorm=e=12.5:r=0.0001:l=1",
    4: "speechnorm=e=25:r=0.0001:l=1",
    5: "speechnorm=e=50:r=0.0001:l=1",
    }
NORM_CMD = NORM_CMDS[args.norm_level]
SIL_ADD_CMD = f"adelay={args.sil}:all=true,apad=pad_dur={args.sil}ms"
SIL_REM_CMD = f"silenceremove=start_periods=1:start_silence={args.sil/1000}:start_threshold={args.sil_db}dB:"
SIL_REM_CMD += f"stop_periods=1:stop_silence={args.sil/1000}:stop_threshold={args.sil_db}dB"

IN_DIR = args.in_dir
OUT_DIR = args.out_dir

for ACC in os.listdir(IN_DIR):
    ACC_IN_DIR = os.path.join(IN_DIR, ACC)
    ACC_OUT_DIR = os.path.join(OUT_DIR, ACC)
    if not os.path.isdir(ACC_IN_DIR):
        continue
    for SPK in os.listdir(ACC_IN_DIR):
        SPK_IN_DIR = os.path.join(ACC_IN_DIR, SPK)
        SPK_OUT_DIR = os.path.join(ACC_OUT_DIR, SPK)
        os.makedirs(SPK_OUT_DIR, exist_ok=True)
        if not os.path.isdir(SPK_IN_DIR):
            continue
        for WAV_NAME in os.listdir(SPK_IN_DIR):
            IN_WAV = os.path.join(SPK_IN_DIR, WAV_NAME)
            OUT_WAV = os.path.join(SPK_OUT_DIR, WAV_NAME)
            os.system(f"{FFMPEG} -i {IN_WAV} -af {NORM_CMD},{SIL_ADD_CMD},{SIL_REM_CMD} {OUT_WAV}")