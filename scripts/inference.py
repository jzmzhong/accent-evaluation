import os
from TTS.api import TTS

# using the default version set in 🐸TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

# # using a specific version
# # 👀 see the branch names for versions on https://huggingface.co/coqui/XTTS-v2/tree/main
# # ❗some versions might be incompatible with the API
# tts = TTS("xtts_v2.0.2", gpu=True)

# # getting the latest XTTS_v2
# tts = TTS("xtts", gpu=False)

# generate speech by cloning a voice using default settings
DATA_ROOT = "/work/tc062/tc062/jzmzhong/models/accent_evaluation"

# ACC = "Edinburgh"
# TEST_TXT2SPK = {
#    "p252": ["p252"],
#    "p272": ["p272"],
#    "p281": ["p281"],
#    "p285": ["p285"],
#    "p262": ["p262"],
# }

# ACC = "Dublin"
# TEST_TXT2SPK = {
#    "p288": ["p288"],
#    "p295": ["p295"],
#    "p340": ["p340"],
#    "p245": ["p245"],
# }

ACC = "SouthernEngland"
# TEST_TXT2SPK = {
#    "p225": ["p225"],
#    "p228": ["p228"],
#    "p229": ["p229"],
#    "p231": ["p231"],
# }
TEST_TXT2SPK = {
   "p232": ["p232"],
   "p240": ["p240"],
   "p257": ["p257"],
   "p258": ["p258"],
   "p268": ["p268"],
}

for TXT, SPKS in TEST_TXT2SPK.items():
    TEST_TXT_DIR = os.path.join(DATA_ROOT, "gt_trans", ACC, TXT)
    for SPK in SPKS:
        REFERENCE_WAV = os.path.join(DATA_ROOT, "gt_48k", ACC, SPK, SPK+"_024_mic1.flac")
        if not os.path.exists(REFERENCE_WAV):
            continue
        OUTPUT_WAV_FOLDER = os.path.join(DATA_ROOT, "xtts_24k", ACC, SPK)
        os.makedirs(OUTPUT_WAV_FOLDER, exist_ok=True)
        for TXT_FILE in sorted(os.listdir(TEST_TXT_DIR)):
            txt_path = os.path.join(TEST_TXT_DIR, TXT_FILE)
            with open(txt_path, encoding="utf-8", mode="r") as f:
                txt = f.read().strip()
            tts.tts_to_file(text=txt,
                            speaker_wav=REFERENCE_WAV,
                            language="en",
                            file_path=os.path.join(OUTPUT_WAV_FOLDER, TXT_FILE.replace(TXT, SPK).replace(".txt", ".wav")),
                            split_sentences=False)