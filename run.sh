#! /bin/bash

#SBATCH -c 64
#SBATCH --time=30:00
#SBATCH --gres=gpu:L40s:1

source .venv/bin/activate

echo "RUNNING"
#python3 -m scripts.evaluate_rag --config "./configs/counterfactual_rag_eval_config.yaml"
#python3 -m scripts.evaluate_rag --config "./configs/medical_rag_eval_config.yaml"
python3 -m scripts.correct_results
echo "DONE"