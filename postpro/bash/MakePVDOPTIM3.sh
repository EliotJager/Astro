#!/bin/bash

pvdfile="OPTIM3.pvd"

echo "<?xml version=\"1.0\"?>" > $pvdfile
echo "<VTKFile type=\"Collection\" version=\"0.1\"" >> $pvdfile
echo "        byte_order=\"LittleEndian\" " >> $pvdfile
echo "        compressor=\"vtkZLibDataCompressor\">" >> $pvdfile
echo "  <Collection>" >> $pvdfile

OPTIMs=($(ls LatinHyper40/PVTUs_OPTIM/*3.pvtu))

c=0
for i in ${OPTIMs[@]}
do
    c=$(($c+1))
    filename=$i
    time=$c
    echo "   <DataSet timestep=\""$time"\" group=\"\" part=\"0\" " >> $pvdfile
    echo "     file=\"$filename\"/>" >> $pvdfile
done


OPTIM1s=($(ls LatinHyper40/m1_fine/PVTUs_OPTIM/*3.pvtu))


for i in ${OPTIM1s[@]}
do
    c=$(($c+1))
    filename=$i
    time=$c
    echo "   <DataSet timestep=\""$time"\" group=\"\" part=\"0\" " >> $pvdfile
    echo "     file=\"$filename\"/>" >> $pvdfile
done


echo "  </Collection>" >> $pvdfile
echo "</VTKFile>" >> $pvdfile
