# !/bin/sh

#PBS -N FopJob
#PBS -t 87-96
#PBS -l select=1
#PBS -l walltime=120:01:00
#PBS -l pmem=25000mb
#PBS -o FopJob.stdout
#PBS -e FopJob.stderr
cd $PBS_O_WORKDIR

python address-divide-intersize.py fop-trace-no-repeat fop-result1.$PBS_ARRAYID 1.$PBS_ARRAYID