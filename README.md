# Team3-GenePrediction
Team3 Gene Prediction Team:<br />
Sonali Gupta <br />
Ahish Sujay <br />
Pallavi Misra <br />
Cheng Shen-Yi <br />
Jie Zhou <br />

## Summary 
This pipeline is designed to predict genes from assembled genomes using a number of assembly programs and techniques (ab initio and homology based). 
##### For predicting the coding genes it uses the following programs:
* Prodigal
* GeneMarkS-2
* BLAST

##### For predicting the non-coding genes it uses the following programs:
<fill-in>

### Pipeling Requirements

### Script Execution

`geneprediction_pipeline.py -h {Help}`<br />
`geneprediction_pipeline.py -i <Genome Assembly Input Directory> -o <Output Directory> -b <CDS FNA file>` <br />


##### Options
`        -i     dir             Directory with fq.gz` <br />
`        -o      dir             output folder `<br />
`        -b      file    Reference genome file`


### Output files

