#!/bin/bash

#SBATCH --time=72:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores per sub-job(i.e. tasks)
#SBATCH --mem-per-cpu=1G  # memory per CPU core
#SBATCH -J '38 turbs 36 dir. alg: ps. wec method: d. # job name'
#SBATCH --mail-user=jaredthomas68@gmail.com   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --array=0-3     # job array of size 200

echo ${SLURM_ARRAY_TASK_ID}

model_number=1
op_alg_number=2
wec_method_number=1
maxwec=3
nsteps=6

python3 opt_mstart.py ${SLURM_ARRAY_TASK_ID} $wec_method_number $model_number $op_alg_number $maxwec $nsteps