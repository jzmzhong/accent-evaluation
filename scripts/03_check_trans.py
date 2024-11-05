import os

TRANS_DIR = "../gt_trans"

template = {}
for ACC in os.listdir(TRANS_DIR):
    ACC_DIR = os.path.join(TRANS_DIR, ACC)
    if not os.path.isdir(ACC_DIR):
        continue
    for SPK in os.listdir(ACC_DIR):
        SPK_DIR = os.path.join(ACC_DIR, SPK)
        if not os.path.isdir(SPK_DIR):
            continue
        for TXT in sorted(os.listdir(SPK_DIR)):
            TXT_PATH = os.path.join(SPK_DIR, TXT)
            ID = TXT.split("_")[-1]
            with open(TXT_PATH, encoding="utf-8", mode="r") as f:
                sent = f.read().strip()
                if ID not in template:
                    template[ID] = sent
                else:
                    if sent != template[ID]:
                        print(TXT_PATH, sent, template[ID])
            
        