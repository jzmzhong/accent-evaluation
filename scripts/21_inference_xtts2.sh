export TTS_HOME="/work/tc062/tc062/jzmzhong/coqui_tts_cache"
export HF_HOME="/work/tc062/tc062/jzmzhong/.cache/huggingface/"

TAR_DIR=/work/tc062/tc062/jzmzhong/coqui-TTS
cp ./inference.py $TAR_DIR
cd $TAR_DIR
python -m inference