import os
import args
import ppgs
import torch

# Choose a gpu index to use for inference. Set to None to use cpu.
GPU = None

# IN_DIR = args.in_dir
# OUT_DIR = args.out_dir

# for ACC in os.listdir(IN_DIR):
#     ACC_IN_DIR = os.path.join(IN_DIR, ACC)
#     ACC_OUT_DIR = os.path.join(OUT_DIR, ACC)
#     if not os.path.isdir(ACC_IN_DIR):
#         continue

# ACC_DIR_A = args.dir_a
# ACC_DIR_B = args.dir_b
ACC_DIR_A = "../gt_22.05k/SouthernEngland"
ACC_DIR_B = "../xtts_22.05k_vol0.4_100ms/SouthernEngland"


def mean_PPG_byphone(wav):
    audio = ppgs.load.audio(wav)
    ppg = ppgs.from_audio(audio, ppgs.SAMPLE_RATE, gpu=GPU)
    pred_phones_byframe = torch.argmax(ppg, dim=1)
    pred_phones, frames_byphone = torch.unique_consecutive(pred_phones_byframe, return_counts=True)
    ends = torch.cumsum(frames_byphone, dim=0)
    starts = torch.cat([torch.tensor([0]), ends[:-1]])
    mean_ppg = [ppg[:,:,start:end].mean(dim=2).squeeze(0) for start, end in zip(starts, ends)]
    return pred_phones, mean_ppg


for SPK in os.listdir(ACC_DIR_A):
    SPK_DIR_A = os.path.join(ACC_DIR_A, SPK)
    SPK_DIR_B = os.path.join(ACC_DIR_B, SPK)
    if not os.path.exists(SPK_DIR_B):
        print("Skipping speaker:", SPK)
        continue
    for WAV_NAME in os.listdir(SPK_DIR_A):
        WAV_A = os.path.join(SPK_DIR_A, WAV_NAME)
        WAV_B = os.path.join(SPK_DIR_B, WAV_NAME.replace("_mic1", ""))
        if not os.path.exists(WAV_B):
            print("Skipping wav:", SPK, WAV_NAME)
            continue
        pred_phones_a, mean_ppg_a = mean_PPG_byphone(WAV_A)
        pred_phones_b, mean_ppg_b = mean_PPG_byphone(WAV_B)
        import pdb; pdb.set_trace()
        print()

