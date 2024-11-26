#!/bin/bash
#
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --account=tc062-jzmzhong
#SBATCH --job-name=
#SBATCH --time=4:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

# Load the required modules 
source /work/tc062/tc062/jzmzhong/myvenvs/py310torch23cu118/bin/activate

export TORCH_HOME=/work/tc062/tc062/jzmzhong/.cache
export HF_HOME=/work/tc062/tc062/jzmzhong/.cache

srun python -m inference_vallex

