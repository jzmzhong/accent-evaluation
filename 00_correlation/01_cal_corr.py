import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ACC = "Edinburgh"

METRIC2PATH = {
    "Pronunciation\n(PPG cosine)": f"../02_ppg_dist/analysis/stats_{ACC}_cosine.csv",
    "Pronunciation\n(PPG Jensen-Shannon)": f"../02_ppg_dist/analysis/stats_{ACC}_jensenshannon.csv",
    "Accent\n(GenAID cosine)": f"../03_aid_sim/analysis/stats_{ACC}_aid_cosine.csv",
    # "Accent\n(GenAID cosine)": f"../03_aid_sim/analysis_beforeDNNBN/stats_{ACC}_aid_cosine.csv",
    "Accent\n(CommonAccent cosine)": f"../03_aid_sim/analysis_opensource/stats_{ACC}_aid_cosine.csv",
    "Speaker\n(WavLM cosine)": f"../01_std_metric/analysis/stats_{ACC}_similarity.csv",
    "Intelligbility\n(Whisper WER)": f"../01_std_metric/analysis/stats_{ACC}_wer.csv",
    "Intelligbility\n(Whisper CER)": f"../01_std_metric/analysis/stats_{ACC}_cer.csv",
    "Predicted MOS\n(UTMOS)": f"../04_utmos/analysis/stats_{ACC}_UTMOS.csv",
    "MCD": f"../01_std_metric/analysis/stats_{ACC}_mcd.csv",
    "F0\n(RMSE)": f"../01_std_metric/analysis/stats_{ACC}_f0rmse.csv",
    "F0\n(Period. RMSE)": f"../01_std_metric/analysis/stats_{ACC}_f0_periodicity_rmse.csv",
    "F0\n(Pearson Coeff.)": f"../01_std_metric/analysis/stats_{ACC}_fpc.csv",
    "Voicing\n(F1-score)": f"../01_std_metric/analysis/stats_{ACC}_v_uv_f1.csv",
}

# NUM_SYS = 17
NUM_SYS = 5
# NUM_SYS = 7

if NUM_SYS == 17:
    SYSTEMS = ["copysyn", "xtts", "xtts10k", "xtts20k", "xtts30k", "xtts40k", "xtts50k", "xtts60k", "xtts70k", "xtts80k", "xtts90k", "xtts100k", "xtts110k", "xtts120k", "xtts130k", "xtts140k", "xtts150k"]
elif NUM_SYS == 5:
    SYSTEMS = ["copysyn", "xtts", "xtts50k", "xtts100k", "xtts150k"]
elif NUM_SYS == 7:
    SYSTEMS = ["copysyn", "xtts", "xtts30k", "xtts60k", "xtts90k", "xtts120k", "xtts150k"]

def read_means(csv_path):
    stats = pd.read_csv(csv_path, delimiter=",")
    if "_similarity" in csv_path: # convert similarity to distance
        means = (1. - stats["mean"]).to_list()
    elif "_fpc" in csv_path or "_v_uv_f1" in csv_path: # convert correlation/f1 to negative
        means = (-1 * stats["mean"]).to_list()
    else:
        means = stats["mean"].to_list()
    if NUM_SYS == 5:
        means = means[:2] + means[6:7] + means[11:12] + means[16:17]
    elif NUM_SYS == 7:
        means = means[:2] + means[4:5] + means[7:8] + means[10:11]  + means[13:14] + means[16:17]
    return means

metrics = {"Hypoth. Rank": np.arange(1, NUM_SYS+1)}
for metric_name, path in METRIC2PATH.items():
    metrics[metric_name] = read_means(path)

metrics = pd.DataFrame.from_dict(metrics, orient="index", columns=SYSTEMS).T
metrics.to_csv(f"./all_metrics_{NUM_SYS}.csv")

correlation_matrix = metrics.corr("spearman")
plt.figure(figsize=(15, 15))
sns.heatmap(np.round(correlation_matrix, decimals=3), annot=True, fmt='.3g')
plt.xticks(rotation=45)
plt.savefig(f"./heatmap_corr_{NUM_SYS}.pdf")
