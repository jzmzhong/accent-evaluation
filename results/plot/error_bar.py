import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# MODE = "edi_cos"
# TITLE = "Edinburgh Cosine Similarity Experiments, Each with 5 Speakers & 23 Utterances"

# MODE = "edi_ppg"
# TITLE = "Edinburgh PPG DTW-JS Experiments, Each with 5 Speakers & 23 Utterances"

MODE = "sou_cos"
TITLE = "SouthernEngland Cosine Similarity Experiments, Each with 10 Speakers & 23 Utterances"

# MODE = "sou_ppg"
# TITLE = "SouthernEngland PPG DTW-JS Experiments, Each with 10 Speakers & 23 Utterances"

stats = pd.read_csv(f"stats_{MODE}.csv", delimiter=",")

exp_names = stats["system"].to_list()
means = stats["mean"].to_list()
standard_errors = stats["std_err"]

experiments = np.arange(1, len(exp_names) + 1)

plt.figure(figsize=(20, 10))
plt.errorbar(exp_names, means, yerr=np.array(standard_errors)*1.96, fmt='o', capsize=5, capthick=2, label='Mean ± 95%CI')

plt.title(TITLE)
plt.xlabel('Evaluated System')
plt.ylabel('PPG DTW-JS Pronunciation Distance')
plt.xticks(exp_names)
plt.grid(True)
plt.legend()
plt.savefig(f"error_bar_{MODE}.png")
# plt.show()
plt.clf()
