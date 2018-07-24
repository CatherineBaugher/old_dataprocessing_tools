#!/bin/bash
#PBS -N "occurrence_scatterplot"
#PBS -l walltime=20:00:00
#PBS -l nodes=1:ppn=8
#PBS -j oe
#PBS -l mem=4GB

python3 /fs/project/PHS0293/cancerproj/coadread/visualization/makescatter.py
