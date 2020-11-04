#! /bin/bash
#################
#################
## Script to plot L curve from OPTIM folders
#################
#################

## check argument provided
if [ $# -eq 0 ]
then
	echo "No argument supplied"
	echo "provide day number"
	exit 1
fi

input=$1

output=$2

cd $input

if [ -d Lcurve ]; then
	rm -r Lcurve
	echo "new one"
fi

folder=$(ls -d *)

echo $folder


mkdir $output/Lcurve/
mkdir $output/Lcurve/CostU/
mkdir $output/Lcurve/CostReg/
mkdir $output/Lcurve/CostDiv/

for f in $folder
do
	cp $f/Cost_O* $output/Lcurve/CostU/
	cp $f/CostReg* $output/Lcurve/CostReg/
	cp $f/Cost_dHdt* $output/Lcurve/CostDiv/ 
done

mkdir $output/Lcurve/CSV

for U in $(ls $output/Lcurve/CostU/)
do
	tail -n 1 $output/Lcurve/CostU/$U >> $output/Lcurve/CSV/CostU.csv
done

for reg in $(ls $output/Lcurve/CostReg/)
do
	tail -n 1 $output/Lcurve/CostReg/$reg >> $output/Lcurve/CSV/CostReg.csv
done

for U in $(ls $output/Lcurve/CostDiv/)
do
        tail -n 1 $output/Lcurve/CostDiv/$U >> $output/Lcurve/CSV/CostDiv.csv
done

cd $output/Lcurve/CSV

echo $(cat CostReg.csv)

echo $(cat CostU.csv)

echo $(cat CostDiv.csv)

