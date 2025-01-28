#!/bin/bash
#
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --account=tc062-jzmzhong
#SBATCH --job-name=xtts2_ft
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

# Load the required modules 
source /work/tc062/tc062/jzmzhong/myvenvs/py311torch22cuda118/bin/activate

nvidia-smi --loop=10 --filename=out-nvidia-smi.txt &
srun bash 21_inference_xtts2.sh