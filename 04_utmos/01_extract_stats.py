import os
import numpy as np
from numpy.linalg import norm
import pandas as pd
import torch
import fsspec

ACCS = {
    "Edinburgh": ["p252", "p262", "p272", "p281", "p285"],
    "SouthernEngland": ["p225", "p226", "p228", "p229", "p231", "p232", "p240", "p257", "p258", "p268"],
    # "Dublin": ["p245", "p288", "p295", "p340"],
    "Dublin": ["p245", "p288", "p340"],
}

# all systems
SYSTEMS = {
    "copysyn": "copysyn_hifiganv1",
    "xtts": "xtts_22.05k_vol0.4_100ms"
    }
for i in range(10, 160, 10):
    SYSTEMS["xtts"+str(i)+"k"] = "xtts_22.05k_corrupt"+str(i)+"k_vol0.4_100ms"

IN_DIR = "./all"

OUT_DIR = "./analysis"
os.makedirs(OUT_DIR, exist_ok=True)

raw_data = {}
for SYSTEM in SYSTEMS:
    with open(os.path.join(IN_DIR, SYSTEM+".csv"), encoding="utf-8", mode="r") as f:
        for line in f:
            path, mos = line.strip().split("\t")
            raw_data[path] = float(mos)

stats_alls = {}
missing_files = []
for ACC, SPKS in ACCS.items():
    stats_alls = {}
    for SYSTEM, SYSTEM_PATH in SYSTEMS.items():
        all_mos_scores = []
        for SPK in SPKS:
            mos_scores = []
            for i in range(23):
                key = f"../accent-evaluation/{SYSTEM_PATH}/{ACC}/{SPK}/{SPK}_{str(i+1).zfill(3)}.wav"
                if key in raw_data:
                    mos_scores.append(raw_data[key])
                else:
                    missing_file = "_".join([ACC, SPK, str(i+1).zfill(3)])
                    if missing_file not in missing_files:
                        missing_files.append(missing_file)
            all_mos_scores.append(np.mean(mos_scores))
        stats_all = [np.mean(all_mos_scores), np.std(all_mos_scores, ddof=1), np.std(all_mos_scores, ddof=1)/np.sqrt(len(all_mos_scores))]
        stats_alls[SYSTEM] = stats_all
    stats_alls = pd.DataFrame.from_dict(stats_alls, orient="index", columns=["mean","std_dev","std_err"])
    stats_alls.index.name = "system"
    stats_alls = stats_alls.reindex(SYSTEMS)
    stats_alls.to_csv(os.path.join(OUT_DIR, "stats_"+ACC+"_utmos.csv"))

print("\n".join(missing_files))