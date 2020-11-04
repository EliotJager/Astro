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

pvdfile="OPTIM3.pvd"

echo "<?xml version=\"1.0\"?>" > $pvdfile
echo "<VTKFile type=\"Collection\" version=\"0.1\"" >> $pvdfile
echo "        byte_order=\"LittleEndian\" " >> $pvdfile
echo "        compressor=\"vtkZLibDataCompressor\">" >> $pvdfile
echo "  <Collection>" >> $pvdfile

OPTIMs=($(ls $input*.vtu))

c=0
for i in ${OPTIMs[@]}
do
    c=$(($c+1))
    filename=$i
    time=$c
    echo "   <DataSet timestep=\""$time"\" group=\"\" part=\"0\" " >> $pvdfile
    echo "     file=\"$filename\"/>" >> $pvdfile
done


echo "  </Collection>" >> $pvdfile
echo "</VTKFile>" >> $pvdfile
