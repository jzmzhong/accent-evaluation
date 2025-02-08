import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ACC = "Edinburgh"
MODES= ["fpc", "f0_periodicity_rmse", "f0rmse", "v_uv_f1", "cer", "wer", "similarity", "mcd"]

for MODE in MODES:

    TITLE = "Edinburgh " + MODE + " Experiments, Each with 5 Speakers & 23 Utterances"
    YLABEL = MODE
    MODE = ACC + "_" + MODE
    
    stats = pd.read_csv(f"./analysis/stats_{MODE}.csv", delimiter=",")

    exp_names = stats["system"].to_list()
    means = stats["mean"].to_list()
    standard_errors = stats["std_err"]

    experiments = np.arange(1, len(exp_names) + 1)

    plt.figure(figsize=(20, 10))
    plt.errorbar(exp_names, means, yerr=np.array(standard_errors)*1.96, fmt='o', capsize=5, capthick=2, label='Mean ± 95%CI')

    plt.title(TITLE)
    plt.xlabel('Evaluated System')
    plt.ylabel(YLABEL)
    plt.xticks(exp_names)
    plt.grid(True)
    plt.legend()
    plt.savefig(f"./analysis/error_bar_{MODE}.png")
    # plt.show()
    plt.clf()
