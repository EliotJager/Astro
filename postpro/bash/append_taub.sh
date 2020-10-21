#!/bin/bash


sce=/mnt/data/ejager/Greenland

mkdir /mnt/data/ejager/Greenland/data/TAUB

output=/mnt/data/ejager/Greenland/data/TAUB

files1=$(ls $sce/data/LatinHyper40/ | grep 'PARAM')

echo $files

c=0

cur_param=$(head -n 3 $sce/data/LatinHyper40/test_PARAM0/paramater.txt)
echo $cur_param
m="${cur_param[@]:(-1)}"
echo "m:"$m
sed "s|<m>|"$m"|g;s|<INPUT>|"$sce"/data/LatinHyper40/test_PARAM0/MESH_2|g;s|<OUTPUT>|/mnt/data/ejager/Greenland/data/TAUB|g;s|<NUM>|0|g" $sce/postpro/pvpython/taub.py > $output/taub0.py
pvpython $output/taub0.py
rm $output/taub0.py
c=$(($c+1)) # pour generaliser : supprimer les 2 lignes


echo $files1
for f in $files1
do
    echo $f
    num=${f[@]:5:6}
    echo 'num: '$num
    cur_param=$(head -n 3 $sce/data/LatinHyper40/$f/paramater.txt)
    echo $cur_param
    m="${cur_param[@]:(-1)}"
    echo "m:"$m
    sed "s|<m>|"$m"|g;s|<INPUT>|"$sce"/data/LatinHyper40/$f/MESH_2|g;s|<OUTPUT>|/mnt/data/ejager/Greenland/data/TAUB|g;s|<NUM>|$num|g" $sce/postpro/pvpython/taub.py > $output/taub$num.py
    pvpython $output/taub$num.py
    rm $output/taub$num.py
    c=$(($c+1))
done


files2=$(ls $sce/data/LatinHyper40/m1_fine/ | grep 'PARAM')

for f in $files2
do
    echo $f
    num=${f[@]:5:6}
    echo 'num: '$num
    cur_param=$(head -n 3 $sce/data/LatinHyper40/m1_fine/$f/paramater.txt)
    echo $cur_param
    m="${cur_param[@]:(-1)}"
    echo "m:"$m
    sed "s|<m>|"$m"|g;s|<INPUT>|"$sce"/data/LatinHyper40/m1_fine/$f/MESH_2|g;s|<OUTPUT>|/mnt/data/ejager/Greenland/data/TAUB|g;s|<NUM>|$num|g" $sce/postpro/pvpython/taub.py > $output/taub$num.py
    pvpython $output/taub$num.py
    rm $output/taub$num.py
    c=$(($c+1))
done
