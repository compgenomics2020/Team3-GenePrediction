#!/usr/bin/env python3

import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", help='input directory path')
args = parser.parse_args()

if(args.input_dir):
    input_dir = args.input_dir


#filename = os.listdir("Python_Scripts/GenomeAssembly/")
from os import popen
filename = popen("ls "+input_dir+" -p . | grep -v /$","r").readlines()
#filename = subprocess.call("ls ./GenomeAssembly/ -p . | grep -v /$",shell=True)
filename = filename[4:]
filename1 = []
for name in filename:
        filename1.append(name[:-1])
#print(filename1)


subprocess.run("mkdir ./ToolOutputs", shell= True)
subprocess.run("mkdir ./ToolOutputs/Prodigal_nucl", shell = True)
subprocess.run("mkdir ./ToolOutputs/Prodigal_pos", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMark_pos1", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMarkProdigalIntersection", shell = True)
subprocess.run("mkdir ./ToolOutputs/GeneMark_Only", shell = True)
subprocess.run("mkdir ./ToolOutputs/Prodigal_Only", shell = True)



#Function for Pulling FASTA

def PullFASTA_prodigal(gff_dir, fasta_dir, outdir):
	gff_files = subprocess.run("ls "+gff_dir, shell = True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

	gff_files2 = []

	for f in gff_files:
    		gff_files2.append(f.split("_")[0])


	for gff_file in gff_files2:
    		nodes = []
   
    		with open(gff_dir+"/"+gff_file+"_pos_prodigal_"+gff_file+"_pos_prodigal", "r") as fh:
        		for line in fh.readlines():
            			line = line.split()
            			nodes.append(line[0])
  
   		 with open(fasta_dir+"/"+gff_file+"_nucl_prodigal", "r") as fh:
        		f2 = open(outdir+"/"+gff_file+"_nucl_genemark_fasta", "w")
        		for line in fh:
           			if line.startswith(">"):
                			line = line.split()
               			        k = line[0][1:].split("_")
                                        j = "_".join(k[:-1])

                                if j in nodes:
                    			f2.write(">"+j+ "\n")
                    			line = next(fh)
                    			while(line.startswith(">") == False):
                        			f2.write(str(line))
                        			try:
                            				line = next(fh)
                        			except:
                            				break

          

def PullFAST_GeneMark(gff_dir, fasta_dir, outdir):
	gff_files = subprocess.run("ls "+gff_dir, shell = True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

        gff_files2 = []
        for f in gff_files:
        	gff_files2.append(f.split("_")[0])

	for gff_file in gff_files2:
    		nodes = []
	        with open(gff_dir+"/"+gff_file+"_pos_genemark_"+gff_file+"_pos_prodigal", "r") as fh:
                for line in fh.readlines():
            		line = line.split()
           	        nodes.append(line[0])
   
    		with open(fasta_dir+"/"+gff_file+"_nucl_genemark", "r") as fh:
        		f2 = open(outdir+"/"+gff_file+"_nucl_genemark_fasta", "w")
        		for line in fh:
           			if line.startswith(">"):
                			line = line.split()
			                if line[1] in nodes:
                       			        f2.write(">"+line[1]+ "\n")
			                        line = next(fh)
                    				while(line.startswith(">") == False):
                        				f2.write(str(line))
                       					 try:
                           					 line = next(fh)
                       					 except:
                           					 break





def concat():






#Running Prodigal and GeneMarkS-2
for files in filename1:
        prefix = files[0:7]
        command = "prodigal -i GenomeAssembly/"+files+" -d ./ToolOutputs/Prodigal_nucl/"+prefix+"_nucl_prodigal -f gff -o ./ToolOutputs/Prodigal_pos/"+prefix+"_pos_prodigal"
        subprocess.call(command,shell=True)
         
        command = "perl gms2.pl --seq ../GenomeAssembly/"+files+" --genome-type bacteria -fnn ../ToolOutputs/GeneMark_nucl/"+prefix+"_nucl_genemark --output ../ToolOutputs/GeneMark_pos1/"+prefix+"_pos_genemark --format gff"
        subprocess.call(command,shell=True)
       


#Running bedtools for intersection
files1 = subprocess.run("ls ./ToolOutputs/GeneMark_pos1/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")
files2 = subprocess.run("ls ./Prodigal_pos/", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip().split("\n")

for i,j in zip(files1, files2):
        subprocess.run("bedtools intersect -f 1,0 -r -a ./ToolOutputs/GeneMark_pos1/"+i+" -b ./ToolOutputs/Prodigal_pos/"+j+" >./GeneMarkProdigalIntersection/"+i+"_"+j, shell = True)
#Running bedtools for remaining part from intersection

        subprocess.run("bedtools intersect -f 1,0 -r -v -a ./ToolOutputs/GeneMark_pos1/"+i+" -b ./ToolOutputs/Prodigal_pos/"+j+" >./GeneMark_Only/"+i+"_"+j, shell = True)
        subprocess.run("bedtools intersect -f 1,0 -r -v -a ./ToolOutputs/Prodigal_pos/"+i+" -b ./ToolOutputs/GeneMark_pos1/"+j+" >./Prodigal_Only/"+i+"_"+j, shell = True)


#Pulling FASTA for GFF obtained from bedtools



                               
