import os
import numpy as np
import pandas as pd

MODES = ["Edinburgh_cosine", "Edinburgh_jensenshannon", "SouthernEngland_cosine", "SouthernEngland_jensenshannon"]
SYSTEMS = ["copysyn", "xtts", "xtts10k", "xtts20k", "xtts30k", "xtts40k", "xtts50k", "xtts60k", "xtts70k", "xtts80k", "xtts90k", "xtts100k", "xtts110k", "xtts120k", "xtts130k", "xtts140k", "xtts150k"]

IN_FOLDER = "./all"
OUT_FOLDER = "./analysis"

for MODE in MODES:
    stats_alls = {}
    for file in os.listdir(IN_FOLDER):
        if not file.endswith(MODE+".csv"):
            continue
        system = file.split("_")[1].replace("corrupt", "")
        stats = pd.read_csv(os.path.join(IN_FOLDER, file), delimiter=",")
        # stats_all = [stats["mean"].to_list()[0], stats["std_dev"].to_list()[0], stats["std_err"].to_list()[0]]
        measurements = stats["mean"].to_list()[1:]
        stats_all = [np.mean(measurements), np.std(measurements, ddof=1), np.std(measurements, ddof=1)/np.sqrt(len(measurements))]
        stats_alls[system] = stats_all
    stats_alls = pd.DataFrame.from_dict(stats_alls, orient="index", columns=["mean","std_dev","std_err"])
    stats_alls.index.name = "system"
    # stats_alls = stats_alls.sort_index()
    stats_alls = stats_alls.reindex(SYSTEMS)
    stats_alls.to_csv(os.path.join(OUT_FOLDER, "stats_"+MODE+".csv"))