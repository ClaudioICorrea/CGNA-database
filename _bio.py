from Bio import SeqIO
import re
import sys
import mysql.connector
import time


def barra(part,tol):
    cadena = '-'*100
    caracter = '#'
    i = int((part/tol)*100)
    x= list(cadena)
    for j in range(0,i) :
        x[j] = caracter
    cadena = "".join(x)
    print(f'[{cadena}]{i}%',end='\r')
 
zelda = mysql.connector.connect(
    host="localhost",
    user="root",
    password="lukemaster",
    database="cgna_database"
)

link = zelda.cursor()

# file gff3
with open("data/Arabidopsis_thaliana.TAIR10.56.gff3", "r") as ggf_data:
    content_ggf= ggf_data.readlines()
    
#file fasta

Path_chromosome = "data/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa"
Path_transcript  = "data/Arabidopsis_thaliana.TAIR10.cds.all.fa"

### Inicializacion ####
print('downloading gg3: ')
start_time = time.time()
for i,line in enumerate(content_ggf):
    barra(i,len(content_ggf)-1)
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
        link.execute(
            "INSERT INTO chromosomes (id_chromosome, id_specie, number_genes, size, alias) values (%s, %s,%s,%s,%s)",
            (id_chromosome,1,0,size_chromosome,alias_chromosome)
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
        zelda.commit()
    result = re.search(r"ID=transcript:([A-Za-z0-9.]+);",line)
    if result is not None:
        id_transcript =  result.group(1).upper()
        aux = id_transcript.split(".")
        #print(aux)
        #print(line)
        fk_id_gene = aux[0]
        try: 
            num_transcript =  aux[1]
        except :
            id_transcript=id_transcript+".1"
        line_aux=line.split()
        fk_id_chromosome= line_aux[0]
        source_gene = line_aux[1]
        _type = line_aux[2]
        start =line_aux[3]
        end =line_aux[4]
        score = line_aux[5]
        size = int(end_gene) - int(start_gene)
        strand= line_aux[6]
        frame = line_aux[7]
        description_gene = line_aux[8]
        
        
        
        try:
            link.execute(
                "INSERT INTO transcripts (id_transcript, id_genes, id_chromosome, transcript_type, start, end, score, strand, frame, size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (id_transcript, fk_id_gene, fk_id_chromosome, _type, start, end, score, strand, frame, size)
            )
        except mysql.connector.IntegrityError as e:
                print("Error al insertar en la tabla transcripts:",id_transcript)
                print(line)
        zelda.commit()
                
# contamos el numero de transcript por genes  SELECT id_genes from genes;
print('\ncount transcripts for gen..')
link.execute("SELECT id_genes from genes;")
ids_genes = link.fetchall()     
len_fasta_genes= len(ids_genes)-1
for index,id_ in enumerate(ids_genes):
    barra(index,len_fasta_genes)
    link.execute("SELECT COUNT(*) AS total_filas FROM  transcripts  WHERE id_genes= %s;",(id_[0],))
    number_transcripts = link.fetchall()[0][0]
    #print(id_transcript, transcripts_seq )
    link.execute("UPDATE genes SET number_transcript = %s WHERE id_genes = %s;",
                     (number_transcripts,id_[0]))    

print('\ndownloading FASTA 1/2: ')   
 
len_fasta_chromosome=sum(1 for _ in SeqIO.parse(Path_chromosome, "fasta"))-1
for index, record in enumerate(SeqIO.parse(Path_chromosome, "fasta")):
    barra(index,len_fasta_chromosome)
    id_chromosome = record.id
    chromosome_seq = str(record.seq)
    link.execute("SELECT COUNT(*) AS total_filas FROM genes WHERE id_chromosome= %s;",
                     (id_chromosome,))    
    number_genes = link.fetchall()[0][0]
    #print(id_transcript, transcripts_seq )
    link.execute("UPDATE chromosomes SET sequence = %s, number_genes = %s WHERE id_chromosome = %s;",
                     (chromosome_seq,number_genes,id_chromosome))    
     
print('\ndownloading FASTA 2/2: ')    
len_fasta_transcripts=sum(1 for _ in SeqIO.parse(Path_transcript, "fasta"))-1
for index, record in enumerate(SeqIO.parse(Path_transcript, "fasta")):
    barra(index,len_fasta_transcripts)
    id_transcript = record.id
    transcripts_seq = str(record.seq)
    #print(id_transcript, transcripts_seq )
    link.execute("UPDATE transcripts SET sequence = %s WHERE id_transcript = %s;",
                     (transcripts_seq,id_transcript))
    
    #print("Error al insertar en la tabla transcripts:",id_transcript)

zelda.commit()
link.close()
zelda.close()                
end_time=time.time()
total_time = end_time-start_time
print('\nDone in {:.2f}s'.format(total_time))
    
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