sbatch --partition=PGR-Standard --time=24:00:00 --mem=30000 --cpus-per-task=4 --gres=gpu:a40:1 41_objective_metrics.sh
sbatch --partition=PGR-Standard --time=96:00:00 --mem=30000 --cpus-per-task=4 --gres=gpu:a40:1 41_objective_metrics_2.sh
sbatch --partition=PGR-Standard --time=24:00:00 --mem=30000 --cpus-per-task=4 --gres=gpu:a40:1 41_objective_metrics_3.sh