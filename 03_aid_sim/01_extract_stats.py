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
SYSTEMS = ["copysyn", "xtts", "xtts10k", "xtts20k", "xtts30k", "xtts40k", "xtts50k", "xtts60k", "xtts70k", "xtts80k", "xtts90k", "xtts100k", "xtts110k", "xtts120k", "xtts130k", "xtts140k", "xtts150k"]

# IN_PATH = "./all/accents_v2.5.0.pth"
# IN_PATH = "./all/accents_opensource.pth"
# IN_PATH = "./all/accents_v2.5.0_beforeBN.pth"
IN_PATH = "./all/accents_v2.5.0_beforeDNNBN.pth"

# OUT_FOLDER = "./analysis"
# OUT_FOLDER = "./analysis_opensource"
# OUT_FOLDER = "./analysis_beforeBN"
OUT_FOLDER = "./analysis_beforeDNNBN"

os.makedirs(OUT_FOLDER, exist_ok=True)

with fsspec.open(IN_PATH, "rb") as f:
    accent_mapping = torch.load(f)

def cos_dist(x, y):
    return 1-np.dot(x,y)/norm(x)/norm(y)

stats_alls = {}
missing_files = []
for ACC, SPKS in ACCS.items():
    stats_alls = {}
    for SYSTEM in SYSTEMS:
        all_cos_dists = []
        for SPK in SPKS:
            cos_dists = []
            for i in range(23):
                ref_key = "_".join(["VCTK", "gt", SPK, str(i+1).zfill(3)])
                tar_key = "_".join(["VCTK", SYSTEM, SPK, str(i+1).zfill(3)])
                if ref_key in accent_mapping and tar_key in accent_mapping:
                    ref_emb = accent_mapping[ref_key]['embedding']
                    tar_emb = accent_mapping[tar_key]['embedding']
                    cos_dists.append(cos_dist(ref_emb, tar_emb))
                else:
                    missing_file = "_".join([ACC, SPK, str(i+1).zfill(3)])
                    if missing_file not in missing_files:
                        missing_files.append(missing_file)
            all_cos_dists.append(np.mean(cos_dists))
        stats_all = [np.mean(all_cos_dists), np.std(all_cos_dists, ddof=1), np.std(all_cos_dists, ddof=1)/np.sqrt(len(all_cos_dists))]
        stats_alls[SYSTEM] = stats_all
    stats_alls = pd.DataFrame.from_dict(stats_alls, orient="index", columns=["mean","std_dev","std_err"])
    stats_alls.index.name = "system"
    stats_alls = stats_alls.reindex(SYSTEMS)
    stats_alls.to_csv(os.path.join(OUT_FOLDER, "stats_"+ACC+"_aid_cosine.csv"))

print("\n".join(missing_files))