import os
from collections import Counter
from utils.prompt_making import make_prompt
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import librosa
import soundfile as sf

preload_models()
print("Model loaded!")
print("Sampling rate of generated speech:", SAMPLE_RATE)

DATA_ROOT = "/work/tc062/tc062/jzmzhong/models/accent_evaluation"

ACC2SPKS = {
    "Edinburgh": ["p252", "p262", "p272", "p281", "p285"],
    "Dublin": ["p245", "p288", "p340"],
}

for ACC, SPKS in ACC2SPKS.items():
    for SPK in SPKS:
        
        # prepare out folder
        out_folder = os.path.join(DATA_ROOT, "vallex_24k", ACC, SPK)
        os.makedirs(out_folder, exist_ok=True)

        # make audio prompt
        audio_prompt_path = os.path.join(DATA_ROOT, "gt_24k", ACC, SPK, f"{SPK}_024_mic1.wav")
        prompt_name = f"{SPK}_024"
        trans_path = os.path.join(DATA_ROOT, "gt_trans", ACC, SPK, f"{SPK}_024.txt")
        with open(trans_path, encoding="utf-8", mode="r") as f:
            text = f.read().strip()
        make_prompt(name=prompt_name, audio_prompt_path=audio_prompt_path,
                    transcript=text)

        # make text prompts
        text_prompts_dir = os.path.join(DATA_ROOT, "gt_trans", ACC, SPK)
        for text_prompt_filename in os.listdir(text_prompts_dir):
            if text_prompt_filename.endswith(".txt"):
                text_prompt_path = os.path.join(text_prompts_dir, text_prompt_filename)
                with open(text_prompt_path, encoding="utf-8", mode="r") as f:
                    text_prompt = f.read().strip()
                audio_array = generate_audio(text_prompt, prompt=prompt_name)
                out_path = os.path.join(out_folder, text_prompt_filename.replace(".txt", ".wav"))
                write_wav(out_path, SAMPLE_RATE, audio_array)
