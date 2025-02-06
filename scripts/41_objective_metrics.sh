#!/usr/bin/env bash
source /home/s2526235/miniconda3/bin/activate amphion_py39torch20cuda117

DATA_DIR=/home/s2526235/accent-evaluation
CODE_DIR=/home/s2526235/Amphion

declare -A SYSTEMS
SYSTEMS["copysyn"]="copysyn_hifiganv1"
SYSTEMS["xtts"]="xtts_22.05k_vol0.4_100ms"
SYSTEMS["xtts10k"]="xtts_22.05k_corrupt10k_vol0.4_100ms"
SYSTEMS["xtts20k"]="xtts_22.05k_corrupt20k_vol0.4_100ms"
SYSTEMS["xtts30k"]="xtts_22.05k_corrupt30k_vol0.4_100ms"
SYSTEMS["xtts40k"]="xtts_22.05k_corrupt40k_vol0.4_100ms"
SYSTEMS["xtts50k"]="xtts_22.05k_corrupt50k_vol0.4_100ms"
SYSTEMS["xtts60k"]="xtts_22.05k_corrupt60k_vol0.4_100ms"
SYSTEMS["xtts70k"]="xtts_22.05k_corrupt70k_vol0.4_100ms"
SYSTEMS["xtts80k"]="xtts_22.05k_corrupt80k_vol0.4_100ms"
SYSTEMS["xtts90k"]="xtts_22.05k_corrupt90k_vol0.4_100ms"
SYSTEMS["xtts100k"]="xtts_22.05k_corrupt100k_vol0.4_100ms"
SYSTEMS["xtts110k"]="xtts_22.05k_corrupt110k_vol0.4_100ms"
SYSTEMS["xtts120k"]="xtts_22.05k_corrupt120k_vol0.4_100ms"
SYSTEMS["xtts130k"]="xtts_22.05k_corrupt130k_vol0.4_100ms"
SYSTEMS["xtts140k"]="xtts_22.05k_corrupt140k_vol0.4_100ms"
SYSTEMS["xtts150k"]="xtts_22.05k_corrupt150k_vol0.4_100ms"

cd ${CODE_DIR}/pretrained
sh offline_models_setup.sh
cd ..

for SYS in copysyn xtts xtts10k;
# for SYS in copysyn;
do
	for ACC in Edinburgh;
	do
		for SPK in p252 p262 p272 p281 p285;
		# for SPK in p262;
		do
			echo ${DATA_DIR}/${SYSTEMS[${SYS}]}/${ACC}/${SPK}
			sh egs/metrics/run.sh \
				--reference_folder ${DATA_DIR}/ref_22.05k/${ACC}/${SPK} \
				--generated_folder ${DATA_DIR}/${SYSTEMS[${SYS}]}/${ACC}/${SPK} \
				--dump_folder ${DATA_DIR}/objective_analysis \
				--metrics "fpc f0_periodicity_rmse f0rmse v_uv_f1 cer wer similarity mcd" \
				--similarity_model wavlm \
				--similarity_mode pairwith \
				--intelligibility_mode gt_content \
				--ltr_path ${DATA_DIR}/scripts/all_transcription.txt \
				--language english
				# --metrics "pesq" \
				# --metrics "fpc f0_periodicity_rmse f0rmse v_uv_f1 energy_rmse energy_pc cer wer similarity mcd mstft pesq si_sdr si_snr stoi" \
				# --intelligibility_mode gt_audio \

			wait
			mv ${DATA_DIR}/objective_analysis/result.json ${DATA_DIR}/objective_analysis/result_${SYS}_${ACC}_${SPK}.json 
		done
	done
done
