#!/bin/bash


sce=/mnt/data/ejager/Greenland/

mkdir $sce/RUNS2/TAUB

output=$sce/RUNS2/TAUB

files1=$(ls $sce/RUNS2/LH40/ | grep 'PARAM')

echo $files

echo $files1
for f in $files1
do
    echo $f
    num=${f[@]:5:6}
    echo 'num: '$num
    size=${#num}
    echo 'size num: '$size
    if [ $size -eq 1 ]
    then
        echo '1'
        cur_param=$(head -n 3 $sce/RUNS2/LH40/$f/parameter.txt)
        echo $cur_param
        m="${cur_param[@]:85:4}"
        echo "m:"$m
    else
        echo '2'
        cur_param=$(head -n 3 $sce/RUNS2/LH40/$f/parameter.txt)
        echo $cur_param
        m="${cur_param[@]:88:4}"
        echo "m:"$m    
    fi
    sed "s|<m>|"$m"|g;s|<INPUT>|"$sce"RUNS2/LH40/$f/MESH_2|g;s|<OUTPUT>|$output|g;s|<NUM>|$num|g" $sce/postpro/pvpython/taub.py > $output/taub$num.py
    pvpython $output/taub$num.py
    rm $output/taub$num.py
done
