#!/bin/bash


## check argument provided
if [ $# -eq 0 ]
then
        echo "No argument supplied"
        echo "provide input and output folders"
        exit 1
fi

input=$1

output=$2

cd $output


mkdir $output/PVTUs
mkdir $output/PVTUs_CTRL
mkdir $output/PVTUs_IMIP
mkdir $output/PVTUs_OPTIM

files=$(ls $input | grep 'PARAM')

for f in $files
do
    cp $input/$f/MESH_2/*.pvtu $output/PVTUs/
    cp $input/$f/MESH_2/*.vtu $output/PVTUs/
done

ls $output/PVTUs/

cp $output/PVTUs/CTRL* $output/PVTUs_CTRL
cp $output/PVTUs/IMIP* $output/PVTUs_IMIP
cp $output/PVTUs/OPTIM* $output/PVTUs_OPTIM

ls $output/PVTUs_CTRL/
ls $output/PVTUs_IMIP/
ls $output/PVTUs_OPTIM/
