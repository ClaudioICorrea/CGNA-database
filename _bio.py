from Bio import SeqIO
import re
import sys
import mysql.connector

zelda = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lukemaster",
    database="cgna_database"
)

link = zelda.cursor()


with open("data/Arabidopsis_thaliana.TAIR10.56.gff3", "r") as ggf_data:
    content_ggf= ggf_data.readlines()
    
Path_chr_fa = "data/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa"

#for index, record in enumerate(SeqIO.parse(Path_chr_fa, "fasta")):
    #print(index,record)
    #print("##########################################################################")

for line in content_ggf:
    ##asignación de Chromosomas###
    result = re.search(r"ID=chromosome:(\w+);",line)
    if result is not None:
        id_chromosome =  result.group(1)
        line_aux=line.split() 
        size_chromosome = line_aux[4] 
        alias=re.search(r"ID=chromosome:"+id_chromosome+";Alias=(.*)",line_aux[8])
        alias_chromosome=alias.group(1) 
        description=re.search(r";",alias_chromosome)
        #print(description)
        if description is not None:
            aux=alias_chromosome.split(";")
            alias_chromosome=aux[0]
        for index, record in enumerate(SeqIO.parse(Path_chr_fa, "fasta")):
            if record.id == id_chromosome:
                chromosome_seq = str(record.seq)
                break
        #id_chromosome = str(id_chromosome)
        #size_chromosome = str(size_chromosome)
        #print("Id_chromosome:",id_chromosome,"size:",size_chromosome,"Alias:",alias_chromosome,"seq:",chromosome_seq)
        link.execute(
            "INSERT INTO chromosomes (id_chromosome, id_specie, number_genes, size, alias,sequence) values (%s, %s,%s,%s,%s,%s)",
            (id_chromosome,1,0,size_chromosome,alias_chromosome,chromosome_seq)
        )
        zelda.commit()
    #asignación de genes     
    result = re.search(r"ID=gene:(\w+);",line) 
    if result is not None:
        id_gene =  result.group(1)
        line_aux=line.split()
        fk_id_chromosome= line_aux[0]
        source_gene = line_aux[1]
        gene_type = line_aux[2]
        start_gene =line_aux[3]
        end_gene =line_aux[4]
        score_gene = line_aux[5]
        size_gene = int(end_gene) - int(start_gene)
        strand_gene= line_aux[6]
        frame_gene = line_aux[7]
        description_gene = line_aux[8]
        if re.search(r"logic_name=",description_gene) is not None:
            aux = re.search(r"logic_name=(\w+)",description_gene) 
            name_gene = aux.group(1)
        else:
            name_gene = None  
        if re.search(r"biotype=",description_gene) is not None:
            aux = re.search(r"biotype=(\w+)",description_gene) 
            bio_type = aux.group(1)
        else:
            bio_type = None        
        link.execute(
            "INSERT INTO genes (id_genes,id_chromosome,gene_type,start,end,score,strand,frame,size,name_gen, bio_type) values (%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s)",
            (id_gene,fk_id_chromosome,gene_type,start_gene,end_gene,score_gene,strand_gene,frame_gene,size_gene,name_gene,bio_type)
        )
        
link.close()
zelda.close()                
        
    
#from BCBio import GFF
# Arabidopsis_thaliana.TAIR10.56.gff3
#data/Arabidopsis_thaliana.TAIR10.cdna.abinitio.fa
#with open("data/Arabidopsis_thaliana.TAIR10.56.gff3", "r") as handle:
#    records = SeqIO.parse(handle, "gff3")


#from Bio import SeqIO

#with open("data/Arabidopsis_thaliana.TAIR10.56.gff3", "r") as handle:
#    records = SeqIO.parse(handle, "gff")

#for record in records:
#    for feature in record.features:
#        print(feature.type)
#        print(feature.location)
#        print(feature.qualifiers)

#in_handle = open("data/Arabidopsis_thaliana.TAIR10.56.gff3")
#for rec in GFF.parse(in_handle):
#    print(rec)
#in_handle.close()

#for index, record in enumerate(SeqIO.parse("data/Arabidopsis_thaliana.TAIR10.cdna.abinitio.fa", "fasta")):
#    print(index, record)
#    print("##########################################################################")