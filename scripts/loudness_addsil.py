
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--volume", help="normalisation intensity from 1 to 5", type=float, default=1.0)
parser.add_argument("--sil", help="silence length (ms)", type=int, default=100)
parser.add_argument("--in-dir", help="input wav folder", type=str)
parser.add_argument("--out-dir", help="output wav folder", type=str)
args = parser.parse_args()

FFMPEG="/work/tc062/tc062/jzmzhong/myvenvs/mymodules/ffmpeg-git-20240629-amd64-static/ffmpeg"

VOL_CMD = f"volume={args.volume}"
# SIL_ADD_CMD = f"adelay={args.sil}:all=true,apad=pad_dur={args.sil}ms" # add silence to both beginning and end
SIL_ADD_CMD = f"adelay={args.sil}:all=true" # add silence to just beginning

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
            os.system(f"{FFMPEG} -i {IN_WAV} -af {VOL_CMD},{SIL_ADD_CMD} {OUT_WAV}")