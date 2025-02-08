import os
import torchaudio
from tqdm import tqdm

# all accents
ACCENTS = {
    "Edinburgh": "scottish",
    "Dublin": "irish",
    "SouthernEngland": "english",
}

# all systems
SYSTEMS = {
    "gt": "ref_22.05k",
    "copysyn": "copysyn_hifiganv1",
    "xtts": "xtts_22.05k_vol0.4_100ms"
    }
for i in range(10, 160, 10):
    SYSTEMS["xtts"+str(i)+"k"] = "xtts_22.05k_corrupt"+str(i)+"k_vol0.4_100ms"

DIR_PATHS = {k: "../"+v for k, v in SYSTEMS.items()}

OUT_FILE = 'all_file_paths.csv'


ID = 0
all_entries = ["ID,utt_id,wav,wav_format,text,duration,speaker,gender,accent"]
for system, dir_path in tqdm(DIR_PATHS.items()):
    for root, dirs, files in sorted(os.walk(dir_path)):
        for file in sorted(files):
            if file.endswith(".wav"):
                utt_id = "_".join(["VCTK", system, file[:-4]])
                spk = file.split("_")[0]
                acc = root.split("/")[-2]
                full_path = os.path.join(root, file)
                info = torchaudio.info(full_path)
                dur = info.num_frames / info.sample_rate
                full_path = full_path.replace("../", "data_root/")
                # ID,utt_id,wav,wav_format,text,duration,speaker,gender,accent
                entry = ",".join([str(ID), utt_id, full_path, "wav", "", str(dur), spk, "", ACCENTS[acc]])
                all_entries.append(entry)
                ID += 1

with open(OUT_FILE, 'w') as f:
    for entry in all_entries:
        f.write(entry + '\n')
