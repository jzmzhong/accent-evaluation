import os
import args
from tqdm import tqdm
import ppgs
from dtw import dtw
import torch
import numpy as np
from numpy.linalg import norm
from scipy.spatial import distance
import pandas as pd
import math

GPU = None

# TYPE = "cosine"
TYPE = "jensenshannon-normalised"

# STEPS = "50"
# STEPS = "100"
# STEPS = "150"
# for STEPS in ["50", "60", "70", "80", "90", "100"]:

# ACC_DIR_A = args.dir_a
# ACC_DIR_B = args.dir_b

ACC_DIR_A = "../gt_22.05k/SouthernEngland"

# ACC_DIR_B = "../xtts_22.05k_corrupt{}k_vol0.4_100ms/SouthernEngland".format(STEPS)
# OUT_CSV = "../results/gt_xttscorrupt{}k_southernengland_{}.csv".format(STEPS, TYPE)

ACC_DIR_B = "../xtts_22.05k_vol0.4_100ms/SouthernEngland"
OUT_CSV = "../results/gt_xtts_southernengland_{}.csv".format(TYPE)

# ACC_DIR_B = "../copysyn_hifiganv1/SouthernEngland"
# OUT_CSV = "../results/gt_copysyn_southernengland_{}.csv".format(TYPE)

SIM_MATRIX = torch.load(ppgs.SIMILARITY_MATRIX_PATH).float().numpy()
SIM_EXP = ppgs.SIMILARITY_EXPONENT
NORMALISER = SIM_MATRIX.T ** SIM_EXP

def remove_sil(ppg):
    pred_phones = np.argmax(ppg, axis=0)
    start = np.argmax(pred_phones != 39)
    end = np.argmax(pred_phones[::-1] != 39)
    if end == 0: # special case where end is 0
        ppg = ppg[:,start:]
    else:
        ppg = ppg[:,start:-end]
    return ppg

def DTW_PPG(ppg_a, ppg_b, type):
    # remove start and end silence
    ppg_a = remove_sil(ppg_a)
    ppg_b = remove_sil(ppg_b)

    # # for numerical stability
    # ppg_a = np.clip(ppg_a, 1e-8, 1-1e-8)
    # ppg_b = np.clip(ppg_b, 1e-8, 1-1e-8)

    # set distance function
    if type.lower() == "manhattan":
        DIST = lambda x, y: np.abs(x - y)
    elif type.lower() == "cosine":
        DIST = lambda x, y: 1-np.dot(x,y)/norm(x)/norm(y)
    elif type.lower() == "jensenshannon":
        DIST = lambda x, y: distance.jensenshannon(x,y)
    elif type.lower() == "jensenshannon-normalised":
        DIST = lambda x, y: distance.jensenshannon(np.clip(NORMALISER @ x, 1e-8, 1-1e-8), np.clip(NORMALISER @ y, 1e-8, 1-1e-8))
    else:
        raise NotImplementedError
    
    # DTW align
    dist, cost, acc_cost, path = dtw(ppg_a.T, ppg_b.T, dist=DIST)

    if math.isnan(dist):
        import pdb; pdb.set_trace()

        # visualise
        import matplotlib.pyplot as plt
        plt.imshow(acc_cost.T, origin='lower', cmap='gray', interpolation='nearest')
        plt.plot(path[0], path[1], 'r')
        plt.show()
    
    return dist / len(path[0]) # normalised by aligned steps


distances = {}
for SPK in os.listdir(ACC_DIR_A):
    SPK_DIR_A = os.path.join(ACC_DIR_A, SPK)
    SPK_DIR_B = os.path.join(ACC_DIR_B, SPK)
    if not os.path.exists(SPK_DIR_B):
        print("Skipping speaker:", SPK)
        continue
    else:
        print("Processing speaker:", SPK)
        distances[SPK] = []
    for WAV_NAME in tqdm(os.listdir(SPK_DIR_A)):
        WAV_A = os.path.join(SPK_DIR_A, WAV_NAME)
        WAV_B = os.path.join(SPK_DIR_B, WAV_NAME.replace("_mic1", "")) # for xtts2 generation
        if not os.path.exists(WAV_B):
            WAV_B = os.path.join(SPK_DIR_B, WAV_NAME.replace(".wav", "_generated.wav")) # for hifigan copy-synthesis
        if not os.path.exists(WAV_B):
            print("Skipping wav:", SPK, WAV_NAME)
            continue
        audio_a = ppgs.load.audio(WAV_A)
        audio_b = ppgs.load.audio(WAV_B)
        ppg_a = ppgs.from_audio(audio_a, ppgs.SAMPLE_RATE, gpu=GPU).squeeze(0).float().numpy()
        ppg_b = ppgs.from_audio(audio_b, ppgs.SAMPLE_RATE, gpu=GPU).squeeze(0).float().numpy()
        dist = DTW_PPG(ppg_a, ppg_b, TYPE)
        distances[SPK].append(dist)
    # distances[SPK] = (np.mean(distances[SPK]), np.std(distances[SPK]))
    distances[SPK] = (np.nanmean(distances[SPK]), np.nanstd(distances[SPK]))

df = pd.DataFrame.from_dict(distances).transpose()
df = df.set_axis(['mean', 'std_dev'], axis='columns')
df.to_csv(OUT_CSV, index=True)