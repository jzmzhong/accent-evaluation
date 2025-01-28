import os
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import torch
import soundfile as sf

for STEPS in ["10", "20", "30", "40", "50",
              "60", "70", "80", "90", "100",
              "110", "120", "130", "140", "150",
              ]:

    # Device configuration
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Model paths
    xtts_checkpoint = "/work/tc062/tc062/jzmzhong/models/xtts2/GPT_XTTS_v2.0_LJSpeech_FT-January-08-2025_05+25PM-dbf1a08a/checkpoint_"+STEPS+"000.pth"
    xtts_config = "/work/tc062/tc062/jzmzhong/models/xtts2/GPT_XTTS_v2.0_LJSpeech_FT-January-08-2025_05+25PM-dbf1a08a/config.json"
    xtts_vocab = "/work/tc062/tc062/jzmzhong/models/xtts2/XTTS_v2.0_original_model_files/vocab.json"

    # Load model
    config = XttsConfig()
    config.load_json(xtts_config)
    XTTS_MODEL = Xtts.init_from_config(config)
    XTTS_MODEL.load_checkpoint(config, checkpoint_path=xtts_checkpoint, vocab_path=xtts_vocab, use_deepspeed=False)
    XTTS_MODEL.to(device)

    # reference speech and target text paths
    DATA_ROOT = "/work/tc062/tc062/jzmzhong/models/accent_evaluation"

    ACC = "Edinburgh"
    TEST_TXT2SPK = {
    "p252": ["p252"],
    "p272": ["p272"],
    "p281": ["p281"],
    "p285": ["p285"],
    "p262": ["p262"],
    }

    # ACC = "Dublin"
    # TEST_TXT2SPK = {
    #    "p288": ["p288"],
    #    "p295": ["p295"],
    #    "p340": ["p340"],
    #    "p245": ["p245"],
    # }

    # ACC = "SouthernEngland"
    # TEST_TXT2SPK = {
    #    "p225": ["p225"],
    #    "p226": ["p226"],
    #    "p228": ["p228"],
    #    "p229": ["p229"],
    #    "p231": ["p231"],
    #    "p232": ["p232"],
    #    "p240": ["p240"],
    #    "p257": ["p257"],
    #    "p258": ["p258"],
    #    "p268": ["p268"],
    # }

    # config
    LANG = "en"
    SR = 24000

    for TXT, SPKS in TEST_TXT2SPK.items():
        TEST_TXT_DIR = os.path.join(DATA_ROOT, "gt_trans", ACC, TXT)
        for SPK in SPKS:
            REFERENCE_WAV = os.path.join(DATA_ROOT, "gt_48k", ACC, SPK, SPK+"_024_mic1.flac")
            if not os.path.exists(REFERENCE_WAV):
                continue
            
            # conditioning latents of reference wav
            gpt_cond_latent, speaker_embedding = XTTS_MODEL.get_conditioning_latents(
                audio_path=REFERENCE_WAV,
                gpt_cond_len=XTTS_MODEL.config.gpt_cond_len,
                max_ref_length=XTTS_MODEL.config.max_ref_len,
                sound_norm_refs=XTTS_MODEL.config.sound_norm_refs,
            )

            # setup output folder
            OUTPUT_WAV_FOLDER = os.path.join(DATA_ROOT, "xtts_24k_corrupt"+STEPS+"k", ACC, SPK)
            os.makedirs(OUTPUT_WAV_FOLDER, exist_ok=True)
            for TXT_FILE in sorted(os.listdir(TEST_TXT_DIR)):
                txt_path = os.path.join(TEST_TXT_DIR, TXT_FILE)
                
                # read text
                with open(txt_path, encoding="utf-8", mode="r") as f:
                    txt = f.read().strip()
                print(txt)

                # generate wav
                wav = XTTS_MODEL.inference(
                    text=txt,
                    language=LANG,
                    gpt_cond_latent=gpt_cond_latent,
                    speaker_embedding=speaker_embedding,
                    # temperature=0.1,
                    # length_penalty=1.0,
                    # repetition_penalty=10.0,
                    # top_k=10,
                    # top_p=0.3,
                )

                wav = wav["wav"]

                # save wav
                OUTPUT_WAV_PATH = os.path.join(OUTPUT_WAV_FOLDER, TXT_FILE.replace(TXT, SPK).replace(".txt", ".wav"))
                sf.write(OUTPUT_WAV_PATH, wav, SR)