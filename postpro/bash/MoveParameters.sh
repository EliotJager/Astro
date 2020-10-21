#!/bin/bash

files=$(ls LatinHyper40/ | grep 'PARAM')

echo $files

c=0

cp LatinHyper40/test_PARAM0/paramater.txt output/parameter_$c.txt
c=$(($c+1)) # pour generaliser : supprimer les 2 lignes

for f in $files
do
    cond=$(grep ${f:4:3} OPTIM3.pvd)
    echo $cond
    if [ -n "$cond" ]
    then
        cp LatinHyper40/$f/paramater.txt output/parameter_$c.txt
        c=$(($c+1))
	echo 2
	echo $f
    fi
done


files=$(ls LatinHyper40/m1_fine/ | grep 'PARAM')

for f in $files
do
    cp LatinHyper40/m1_fine/$f/paramater.txt output/parameter_$c.txt
    c=$(($c+1))
done
