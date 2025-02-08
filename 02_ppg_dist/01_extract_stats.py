import os
import pandas as pd


MODE = "SouthernEngland_cosine"
IN_FOLDER = "./all"
OUT_FOLDER = "./analysis"

stats_alls = {}
for file in os.listdir(IN_FOLDER):
    if not file.endswith(MODE+".csv"):
        continue
    system = file.split("_")[1].replace("xttscorrupt", "")
    stats = pd.read_csv(os.path.join(IN_FOLDER, file), delimiter=",")
    stats_all = [stats["mean"].to_list()[0], stats["std_dev"].to_list()[0], stats["std_err"].to_list()[0]]
    stats_alls[system] = stats_all
stats_alls = pd.DataFrame.from_dict(stats_alls, orient="index", columns=["mean","std_dev","std_err"])
stats_alls.index.name = "system"
stats_alls = stats_alls.sort_index()
stats_alls.to_csv(os.path.join(OUT_FOLDER, MODE+".csv"))