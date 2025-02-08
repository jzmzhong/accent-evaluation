import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ACC = "Edinburgh"

METRIC2PATH = {
    "PPG (cosine)": f"../02_ppg_dist/analysis/stats_{ACC}_cosine.csv",
    "PPG (Jensen-Shannon)": f"../02_ppg_dist/analysis/stats_{ACC}_jensenshannon.csv",
    "GenAID (cosine)": f"../03_aid_sim/analysis/stats_{ACC}_aid_cosine.csv",
    "WavLM (cosine)": f"../01_std_metric/analysis/stats_{ACC}_similarity.csv",
    "Whisper (WER)": f"../01_std_metric/analysis/stats_{ACC}_wer.csv",
    "Whisper (CER)": f"../01_std_metric/analysis/stats_{ACC}_cer.csv",
    "MCD": f"../01_std_metric/analysis/stats_{ACC}_mcd.csv",
    "F0 (RMSE)": f"../01_std_metric/analysis/stats_{ACC}_f0rmse.csv",
    "F0 (Period. RMSE)": f"../01_std_metric/analysis/stats_{ACC}_f0_periodicity_rmse.csv",
    "F0 (Pearson Coeff.)": f"../01_std_metric/analysis/stats_{ACC}_fpc.csv",
    "Voiced/Unvoiced F1": f"../01_std_metric/analysis/stats_{ACC}_v_uv_f1.csv",
}
SYSTEMS = ["copysyn", "xtts", "xtts10k", "xtts20k", "xtts30k", "xtts40k", "xtts50k", "xtts60k", "xtts70k", "xtts80k", "xtts90k", "xtts100k", "xtts110k", "xtts120k", "xtts130k", "xtts140k", "xtts150k"]

def read_means(csv_path):
    stats = pd.read_csv(csv_path, delimiter=",")
    # exp_names = stats["system"].to_list()
    # if "_aid_cosine" in csv_path:
    #     means = (1. - stats["mean"]).to_list()
    # else:
    #     means = stats["mean"].to_list()
    means = stats["mean"].to_list()
    return means

metrics = {"Hypoth. Rank": np.arange(1, 17)}
for metric_name, path in METRIC2PATH.items():
    metrics[metric_name] = read_means(path)

metrics = pd.DataFrame.from_dict(metrics, orient="index", columns=SYSTEMS).T

correlation_matrix = metrics.corr("spearman")
plt.figure(figsize=(15, 10))
sns.heatmap(np.round(np.abs(correlation_matrix), decimals=3), annot=True, fmt='.3g')
plt.xticks(rotation=20)
plt.savefig("./heatmap_corr.pdf")