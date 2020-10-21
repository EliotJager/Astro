#!/bin/bash

pvdfile="m1.pvd"

mkdir LatinHyper40/m1_fine/PVTUs
mkdir LatinHyper40/m1_fine/PVTUs_CTRL
mkdir LatinHyper40/m1_fine/PVTUs_IMIP
mkdir LatinHyper40/m1_fine/PVTUs_OPTIM

ls LatinHyper40/m1_fine/

for f in $(ls LatinHyper40/m1_fine/)
do
    cp LatinHyper40/m1_fine/$f/MESH_2/*.pvtu LatinHyper40/m1_fine/PVTUs/
    cp LatinHyper40/m1_fine/$f/MESH_2/*.vtu LatinHyper40/m1_fine/PVTUs/
done

ls LatinHyper40/m1_fine/PVTUs/

cp LatinHyper40/m1_fine/PVTUs/CTRL* LatinHyper40/m1_fine/PVTUs_CTRL
cp LatinHyper40/m1_fine/PVTUs/IMIP* LatinHyper40/m1_fine/PVTUs_IMIP
cp LatinHyper40/m1_fine/PVTUs/OPTIM* LatinHyper40/m1_fine/PVTUs_OPTIM

ls LatinHyper40/m1_fine/PVTUs_CTRL/
ls LatinHyper40/m1_fine/PVTUs_IMIP/
ls LatinHyper40/m1_fine/PVTUs_OPTIM/
