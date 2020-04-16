# Team3-Gene Prediction
Team3 Gene Prediction Team:<br />
* Sonali Gupta <br/>
* Ahish Melkote Sujay <br/>
* Pallavi Misra <br/>
* Cheng Shen-Yi <br/>
* Jie Zhou <br/>

## Summary:

This pipeline is designed to predict genes from assembled genomes using a number of assembly programs and techniques (*ab-initio* and homology based).

#### For predicting the coding genes it uses the following programs:
* [Prodigal](https://github.com/hyattpd/Prodigal): *Ab-initio* gene prediction  
* [GeneMarkS-2](http://exon.gatech.edu/GeneMark/license_download.cgi): *Ab-initio* gene prediction
* [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download): To validate *ab-initio* coding results
* [BEDTools](https://bedtools.readthedocs.io/en/latest/content/installation.html): Tools to merge *ab-initio* coding results

#### For predicting the non-coding genes it uses the following programs:
* [ARAGORN](http://130.235.244.92/ARAGORN/Downloads/):
* [BARRNAP](https://github.com/tseemann/barrnap):
* [RNAmmer](https://services.healthtech.dtu.dk/cgi-bin/sw_request):
* [Infernal](http://eddylab.org/infernal/):

## Pipeline Requirements

## Script Execution:
`geneprediction_pipeline.py -h {Help}`<br />
`geneprediction_pipeline.py -i <Genome Assembly Input Directory> -o <Output Directory> -b <CDS FNA file>` <br />

##### Options
`        -i     dir             Directory with fq.gz` <br />
`        -o      dir             output folder `<br />
`        -b      file    Reference genome file`


## Output files:
