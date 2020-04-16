#!/bin/sh
while getopts “f:o:s:h” option
do
        case $option in
                f) file_dict=$OPTARG;;
                o) output=$OPTARG;;
                h) echo help
        esac
done

for filename in $file_dict/*fasta; do
        echo $filename  
        echo $output/$(basename $filename .fasta).gff
	 barrnap --quiet $filename > $output/$(basename $filename .fasta).gff
done
