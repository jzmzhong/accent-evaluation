export MPLCONFIGDIR="/work/tc062/tc062/jzmzhong/.config/matplotlib/"

cd /work/tc062/tc062/jzmzhong/hifi-gan/

WAV_DIR="/work/tc062/tc062/jzmzhong/models/accent_evaluation"

# ACC="Edinburgh"
# for SPK in p252 p272 p281 p285 p262;
# do
#     mkdir -p ${WAV_DIR}/copysyn_hifiganv1/${ACC}/${SPK}
#     python inference.py \
#         --input_wavs_dir ${WAV_DIR}/gt_22.05k/${ACC}/${SPK} \
#         --output_dir ${WAV_DIR}/copysyn_hifiganv1/${ACC}/${SPK} \
#         --checkpoint_file "/work/tc062/tc062/jzmzhong/models/vocoder/HiFiGAN_V1_VCTK/generator_v1"
# done

# ACC="Dublin"
# for SPK in p288 p295 p340 p245;
# do
#     mkdir -p ${WAV_DIR}/copysyn_hifiganv1/${ACC}/${SPK}
#     python inference.py \
#         --input_wavs_dir ${WAV_DIR}/gt_22.05k/${ACC}/${SPK} \
#         --output_dir ${WAV_DIR}/copysyn_hifiganv1/${ACC}/${SPK} \
#         --checkpoint_file "/work/tc062/tc062/jzmzhong/models/vocoder/HiFiGAN_V1_VCTK/generator_v1"
# done

ACC="SouthernEngland"
# for SPK in p225 p228 p229 p231 p232;
# for SPK in p240 p257 p258 p268;
for SPK in p226;
do
    mkdir -p ${WAV_DIR}/copysyn_hifiganv1/${ACC}/${SPK}
    python inference.py \
        --input_wavs_dir ${WAV_DIR}/gt_22.05k/${ACC}/${SPK} \
        --output_dir ${WAV_DIR}/copysyn_hifiganv1/${ACC}/${SPK} \
        --checkpoint_file "/work/tc062/tc062/jzmzhong/models/vocoder/HiFiGAN_V1_VCTK/generator_v1"
done