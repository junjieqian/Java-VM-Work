#!/bin/sh
#SBATCH --ntasks=1               # 1 cores
#SBATCH --time=240:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=20480       # Minimum memory required per CPU (in megabytes)
#SBATCH --job-name=fop
#SBATCH --partition=guest
#SBATCH --error=/work/jiang/jqian/fop/address-divide-intersize/job.fop.err
#SBATCH --output=/work/jiang/jqian/fop/address-divide-intersize/job.fop.out

#./fop.sh &
module load python

python address-divide-intersize.py ../fop-trace-no-repeat fop-result1.$TASK_ID 1.$TASK_ID