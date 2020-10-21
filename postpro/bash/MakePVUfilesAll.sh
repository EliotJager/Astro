#!/bin/bash

pvdfile="m1.pvd"

mkdir LatinHyper40/PVTUs
mkdir LatinHyper40/PVTUs_CTRL
mkdir LatinHyper40/PVTUs_IMIP
mkdir LatinHyper40/PVTUs_OPTIM

files=$(ls LatinHyper40/ | grep 'PARAM')

for f in $files
do
    cp LatinHyper40/$f/MESH_2/*.pvtu LatinHyper40/PVTUs/
    cp LatinHyper40/$f/MESH_2/*.vtu LatinHyper40/PVTUs/
done

ls LatinHyper40/PVTUs/

cp LatinHyper40/PVTUs/CTRL* LatinHyper40/PVTUs_CTRL
cp LatinHyper40/PVTUs/IMIP* LatinHyper40/PVTUs_IMIP
cp LatinHyper40/PVTUs/OPTIM* LatinHyper40/PVTUs_OPTIM

ls LatinHyper40/PVTUs_CTRL/
ls LatinHyper40/PVTUs_IMIP/
ls LatinHyper40/PVTUs_OPTIM/
