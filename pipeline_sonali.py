#!/usr/bin/env python3


import subprocess
import argparse
import os
import tp_fp


parser = argparse.ArgumentParser()
parser.add_argument("-i", help='input directory full path')
parser.add_argument("-o", help='output directory full path')
parser.add_argument("-b", help='FASTA CDS of Bacteria being studied')
args = parser.parse_args()

if(args.i):
    input_dir = args.i

if(args.o):
    output_dir = args.o

if(args.b):
    BLAST_cds_FASTA = args.b

filename1 =  subprocess.run("ls "+input_dir+"/*.fasta", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
#print(filename1)



subprocess.run("mkdir ./ToolOutputs", shell= True)
subprocess.run("mkdir ./ToolOutputs/Prodigal_nucl", shell = True)
subprocess.run("mkdir ./ToolOutputs/Prodigal_pos", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMark_pos1", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMark_nucl", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMarkProdigalIntersection", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMark_Only", shell = True)
subprocess.run("mkdir ./ToolOutputs/Prodigal_Only", shell = True)
subprocess.run("mkdir ./ToolOutputs/MergedGFF", shell = True)
subprocess.run("mkdir ./ToolOutputs/MergedFASTA", shell = True)
subprocess.run("mkdir ./ToolOutputs/BLAST_cds_db", shell = True)
subprocess.run("mkdir ./ToolOutputs/MergedBLAST", shell = True)
subprocess.run("mkdir "+output_dir, shell = True)



def main():

    ######################################Running Prodigal and GeneMarkS-2############################################################################################################################################################################
   
    for files in filename1:
            prefix = os.path.basename(files)
            print(prefix)
            command = "prodigal -i "+files+" -d "+"./ToolOutputs/Prodigal_nucl/"+prefix+"_nucl_prodigal -f gff -o "+"./ToolOutputs/Prodigal_pos/"+prefix+"_pos_prodigal"
            subprocess.call(command,shell=True)

            command = "perl ../Python_Scripts/gms2_linux_64/gms2.pl --seq "+files+" --genome-type bacteria -fnn "+"./ToolOutputs/GeneMark_nucl/"+prefix+"_nucl_genemark --output "+"./ToolOutputs/GeneMark_pos1/"+prefix+"_pos_genemark --format gff"
            subprocess.call(command,shell=True)

    
    ######################################Running bedtools for intersection###########################################################################################################################################################################

   
    files1 = subprocess.run("ls ./ToolOutputs/GeneMark_pos1/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    print(files1)
    files2 = subprocess.run("ls ./ToolOutputs/Prodigal_pos/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    #print(files1, files2)
    for i,j in zip(files1, files2):
            subprocess.run("bedtools intersect -f 1,0 -r -a ./ToolOutputs/GeneMark_pos1/"+i+" -b ./ToolOutputs/Prodigal_pos/"+j+" >./ToolOutputs/GeneMarkProdigalIntersection/"+i+"_"+j, shell = True)
    #######################################Running bedtools for remaining part from intersection######################################################################################################################################################
     
            subprocess.run("bedtools intersect -f 1,0 -r -v -a ./ToolOutputs/GeneMark_pos1/"+i+" -b ./ToolOutputs/Prodigal_pos/"+j+" >./ToolOutputs/GeneMark_Only/"+i+"_"+j, shell = True)
            subprocess.run("bedtools intersect -f 1,0 -r -v -a ./ToolOutputs/Prodigal_pos/"+j+" -b ./ToolOutputs/GeneMark_pos1/"+i+" >./ToolOutputs/Prodigal_Only/"+i+"_"+j, shell = True)

    
    ######################################Getting the bed files#######################################################################################################################################################################################
    files3 = subprocess.run("ls ./ToolOutputs/GeneMarkProdigalIntersection/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    files4 = subprocess.run("ls ./ToolOutputs/GeneMark_Only/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    files5 = subprocess.run("ls ./ToolOutputs/Prodigal_Only/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

    ####################################Merging GFF files#############################################################################################################################################################################################
    for i,j,k in zip(files3, files4, files5):
        subprocess.run("cat ./ToolOutputs/GeneMarkProdigalIntersection/"+i+  " ./ToolOutputs/GeneMark_Only/"+j+" ./ToolOutputs/Prodigal_Only/"+k+" >./ToolOutputs/MergedGFF/"+i+"_"+j+"_"+k+"_merged", shell = True)


    files6 = subprocess.run("ls ./ToolOutputs/MergedGFF/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    ####################################Pulling FASTA for GFF obtained from bedtools##################################################################################################################################################################
    files7 = subprocess.run("ls ./"+input_dir+"/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    ###################################Pulling FASTA for GFF obtained from bedtools###################################################################################################################################################################

    for i,j in zip(files7,files6):
        #print(i,j)
        subprocess.run("bedtools getfasta -fi ./"+input_dir+"/"+i+" -bed ./ToolOutputs/MergedGFF/"+j+" >./ToolOutputs/MergedFASTA/"+i, shell = True)

    ###################################Making BLAST database###################################################################################################################################################################
    
    subprocess.run("makeblastdb -in "+BLAST_cds_FASTA+" -parse_seqids -blastdb_version 5 -dbtype nucl -out ./ToolOutputs/blast_cds_db/CDS", shell = True)

    #files = subprocess.run("ls /home/projects/group-c/Team3-GenePrediction/Python_Scripts/MergedFASTA_Ahish", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    files8 = subprocess.run("ls ./ToolOutputs/MergedFASTA/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
    print("files8")
    
    for i in files8:
    	subprocess.run("blastn -db ./ToolOutputs/blast_cds_db/CDS -query ./ToolOutputs/MergedFASTA/"+i+ " -max_hsps 1 -max_target_seqs 1 -num_threads 8 > ./ToolOutputs/MergedBLAST/"+i+".out", shell = True)

   # tp_fp.wrap(output_dir)
subprocess.run("rm ./"+input_dir+"/*.fai", shell = True)    
#subprocess.run("rm -r ./ToolOutputs", shell= True)
     
if __name__ == '__main__':
    if len(filename1) != 0:
        if (os.path.isdir(output_dir) == True):
            main()
    else:
       print("input directory is empty")

