import os
import librosa
import soundfile as sf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--sr", help="target sampling rate", type=int, default=22050)
parser.add_argument("--in-dir", help="input wav folder", type=str)
parser.add_argument("--out-dir", help="output wav folder", type=str)
args = parser.parse_args()

SR = args.sr
IN_DIR = args.in_dir
OUT_DIR = args.out_dir

os.makedirs(OUT_DIR, exist_ok=True)

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
        for ORIWAV in os.listdir(SPK_IN_DIR):
            if not (ORIWAV.endswith(".flac") or ORIWAV.endswith(".wav")):
                continue
            ORIWAV_PATH = os.path.join(SPK_IN_DIR, ORIWAV)
            NEWWAV_PATH = os.path.join(SPK_OUT_DIR, ORIWAV.replace(".flac", ".wav"))
            y, _ = librosa.load(ORIWAV_PATH, sr=SR)
            sf.write(NEWWAV_PATH, y, SR, subtype='PCM_16')
