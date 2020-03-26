# Team3-GenePrediction
Team3 Gene Prediction

## Summary 
This pipeline is designed to predict genes from assembled genomes using a number of assembly programs and techniques (ab initio and homology based). 
###### For predicting the coding genes it uses the following programs:
* Prodigal
* GeneMarkS-2
* BLAST

###### For predicting the non-coding genes it uses the following programs:
<fill-in>

### Pipeling Requirements

#### Script Execution

######   geneprediction_pipeline.py -h {Help}
######   geneprediction_pipeline.py -in <Genome Assembly Input Directory> -o <Output Directory> -b <CDS FNA file>


##### OPTIONS
######         -in     dir             Directory with fq.gz
######         -o      dir             output folder
######         -R      file    Reference genome file
######         --steps list    Comma separated list of steps to run
######                                         Valid steps: abyss, velvet, spades

### Output files

