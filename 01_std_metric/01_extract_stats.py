import os
import numpy as np
import pandas as pd
import json

ACC = "Edinburgh"
SPKS = ["p252", "p262", "p272", "p281", "p285"]
SYSTEMS = ["copysyn", "xtts", "xtts10k", "xtts20k", "xtts30k", "xtts40k", "xtts50k", "xtts60k", "xtts70k", "xtts80k", "xtts90k", "xtts100k", "xtts110k", "xtts120k", "xtts130k", "xtts140k", "xtts150k"]
MODES= ["fpc", "f0_periodicity_rmse", "f0rmse", "v_uv_f1", "cer", "wer", "similarity", "mcd"]

IN_FOLDER = "./all"
OUT_FOLDER = "./analysis"

stats_alls = {MODE: {} for MODE in MODES}
for SYSTEM in SYSTEMS:
    stats = {MODE: [] for MODE in MODES}
    for SPK in SPKS:
        filepath = os.path.join(IN_FOLDER, "_".join(["result", SYSTEM, ACC, SPK])+".json")
        with open(filepath, mode="r") as f:
            stat = json.load(f)
        for MODE in MODES:
            stats[MODE].append(float(stat[MODE]))
    for MODE in MODES:
        mean, std_dev, std_err = np.mean(stats[MODE]), np.std(stats[MODE], ddof=1), np.std(stats[MODE], ddof=1)/np.sqrt(len(SPKS))
        stats_alls[MODE][SYSTEM] = [mean, std_dev, std_err]

for MODE in MODES:
    df = pd.DataFrame.from_dict(stats_alls[MODE], orient="index", columns=["mean","std_dev","std_err"])
    df.index.name = "system"
    df = df.reindex(SYSTEMS)
    df.to_csv(os.path.join(OUT_FOLDER, "stats_"+ACC+"_"+MODE+".csv"))
