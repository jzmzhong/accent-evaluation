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

GPU = None

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
    
    # set distance function
    if type.lower() == "manhattan":
        dist = lambda x, y: np.abs(x - y)
    elif type.lower() == "cosine":
        dist = lambda x, y: 1-np.dot(x,y)/norm(x)/norm(y)
    elif type.lower() == "jensenshannon":
        dist = lambda x, y: distance.jensenshannon(x,y)
    else:
        raise NotImplementedError
    
    # DTW align
    dist, cost, acc_cost, path = dtw(ppg_a.T, ppg_b.T, dist=dist)
    # visualise
    # import matplotlib.pyplot as plt
    # plt.imshow(acc_cost.T, origin='lower', cmap='gray', interpolation='nearest')
    # plt.plot(path[0], path[1], 'w')
    # plt.show()
    
    return dist / len(path[0]) # normalised by aligned steps


# for TYPE in ["jensenshannon", "cosine"]:
for TYPE in ["cosine"]:
    # for ACC in ["Edinburgh", "Dublin", "SouthernEngland"]:
    for ACC in ["SouthernEngland"]:
        # for STEPS in ["0", "copysynth",
        #             "10", "20", "30", "40", "50",
        #             "60", "70", "80", "90", "100",
        #             "110", "120", "130", "140", "150",
        #             ]:
        for STEPS in ["70", "80", "90", "100",
                    "110", "120", "130", "140", "150",
                    ]:
            print("-----", TYPE, ACC, STEPS, "-----")

            ACC_DIR_A = "../gt_22.05k/{}".format(ACC)
            if STEPS == "0":
                ACC_DIR_B = "../xtts_22.05k_vol0.4_100ms/{}".format(ACC)
                OUT_CSV = "../results/gt_xtts_{}_{}.csv".format(ACC, TYPE)
            elif STEPS == "copysynth":
                ACC_DIR_B = "../copysyn_hifiganv1/{}".format(ACC)
                OUT_CSV = "../results/gt_copysyn_{}_{}.csv".format(ACC, TYPE)
            else:
                ACC_DIR_B = "../xtts_22.05k_corrupt{}k_vol0.4_100ms/{}".format(STEPS, ACC)
                OUT_CSV = "../results/gt_xttscorrupt{}k_{}_{}.csv".format(STEPS, ACC, TYPE)

            distances = {"all":[]}
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

                    if "_024" in WAV_NAME: # skip the reference speech
                        continue

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
                distances["all"] += distances[SPK]
                distances[SPK] = (np.mean(distances[SPK]), np.std(distances[SPK], ddof=1), np.std(distances[SPK], ddof=1)/np.sqrt(len(distances[SPK])))
            distances["all"] = (np.mean(distances["all"]), np.std(distances["all"], ddof=1), np.std(distances["all"], ddof=1)/np.sqrt(len(distances["all"])))

            df = pd.DataFrame.from_dict(distances).transpose()
            df = df.set_axis(['mean', 'std_dev', 'std_err'], axis='columns')
            df.to_csv(OUT_CSV, index=True)