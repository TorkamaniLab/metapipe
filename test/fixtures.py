# Snippets

cmd = """python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh \
 somefile.txt
"""

cmd_magic1 = """python somescript.py {*.counts||} > someout
"""

cmd_magic2 = """python somescript.py {*.counts,} > someout
"""

cmd_compound1 = """./somescript {1,2,3,4||test/files/*.counts||}
"""

cmd_compound2 = """./somescript {1,2,3,4||test/files/*.counts,}
"""

cmd_multiple_inputs = """bash somescript {1,2,3} --conf {4,5,6}  > {o}
"""

cmd_suggest_output = """bash somescript {1,2,3} > {o.gz}
"""

cmd_multiple_close_inputs = """
java -jar trimmomatic PE {*R1_001.fastq.gz||} {*R2_001.fastq.gz||} \
    {o} {o} {o} {o} \
    ILLUMINACLIP:Trimmomatic-0.35/adapters/TruSeq3-PE.fa:2:30:10:2:true \
    LEADING:3 TRAILING:3
"""

cmd_using_multiple_out = """
gzip --stdout -d {1.1-1||1.1-3} > {o}
"""

file = """1. somedir/somefile.ext"""

path = """python /usr/bin/python"""


# Full input files.


overall = """
[COMMANDS]
python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh somefile.txt
bash somescript.sh -i {1.1||1.2} -o {o} -fgh somefile.txt
rb somescript.rb -i {2.1||2.2||1.1,1.2} >> somefile
cut -f *.counts > something.file
paste *.counts > some.file #{o:some.file}

./somescript {1,2,3,4||*.counts,}

rb somescript.rb -i {*.counts||}
python somescript.py -i {*.counts,}  #{o:*.bam}
cat {*.bam,}

cat {2.1} > something.my_output #{o:*.my_output}
cat {*.my_output,}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6

[PATHS]
python /usr/bin/python
bash /usr/bin/bash
rb /usr/bin/ruby
"""


no_paths = """
[COMMANDS]
python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh somefile.txt
bash somescript.sh -i {1.1||1.2} -o {o} -fgh somefile.txt
rb somescript.rb -i {2.1||2.2||1.1,1.2} >> somefile
cut -f *.counts > something.file
paste *.counts > some.file #{o:some.file}

./somescript {1,2,3,4||*.counts,}

rb somescript.rb -i {*.counts||}
python somescript.py -i {*.counts,}  #{o:*.bam}
cat {*.bam,}

cat {2.1} > something.my_output #{o:*.my_output}
cat {*.my_output,}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6
"""


no_files = """
[COMMANDS]
python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh somefile.txt
bash somescript.sh -i {1.1||1.2} -o {o} -fgh somefile.txt
rb somescript.rb -i {2.1||2.2||1.1,1.2} >> somefile
cut -f *.counts > something.file
paste *.counts > some.file #{o:some.file}

./somescript {1,2,3,4||*.counts,}

rb somescript.rb -i {*.counts||}
python somescript.py -i {*.counts,}  #{o:*.bam}
cat {*.bam,}

cat {2.1} > something.my_output #{o:*.my_output}
cat {*.my_output,}

[PATHS]
python /usr/bin/python
bash /usr/bin/bash
rb /usr/bin/ruby
"""


no_cmds = """
[PATHS]
python /usr/bin/python
bash /usr/bin/bash
rb /usr/bin/ruby
"""

multiple_inputs = """
[COMMANDS]
bash somescript {1||2||3} --conf {4||5||6}  > {o}
python somescript.py {1,2,3} --conf {4,5,6}  > {o}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6
"""


multiple_outputs = """
[COMMANDS]
bash somescript {1||2||3} --log {o} -r {o}
python somescript.py {4,5,6} --log {o} -r {o} --output {o}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6
"""


magic_inputs = """
[COMMANDS]
bash somescript {*.counts||}  > {o}
bash togetherness {*.counts}  > {o}
python somescript.py {*.counts||} --conf {*.counts||}  > {o}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6
"""

full_sample_pipeline = """
[COMMANDS]
# Trimmomatic
java -jar trimmomatic PE {*R1_001.fastq.gz} {*R2_001.fastq.gz} \
    {o} {o} {o} {o} illuminaclip LEADING:3 TRAILING:3

# Unzip the outputs from trimmomatic
gzip --stdout -d {*.1.*-2.output||} > {o}
gzip --stdout -d {*.1.*-4.output||} > {o}

# Cutadapt
# cutadapt needs unzipped fastq files
cutadapt --cut 7 -o {o} {*.2.output||}
cutadapt --cut 7 -o {o} {*.3.output||}

# BowTie
module load bowtie/2.2.3; \
bowtie2 --very-sensitive -N 1 -p 8 -x HG_19 -q -1 {*.4.*.output||} -2 \
{*.5.*.output||} -S {o}

# HTSeq
module load python; \
htseq-count {*.7.*.output||} gene_list > {o}

# Summary
head --lines -5 {*.8.*.output} > {o}

[PATHS]
trimmomatic Trimmomatic-0.35/trimmomatic-0.35.jar
cutadapt ~/.local/bin/cutadapt
illuminaclip ILLUMINACLIP:/gpfs/home/bhuvan/Programs/Trimmomatic-0.32/adapters/TruSeq3-PE.fa:2:30:10:2:true
HG_19 /gpfs/group/stsi/data/bschrader/hg19/hg19_ucsc
gene_list /gpfs/home/atorkama/iGenomes/Homo_sapiens/UCSC/hg19/Annotation/Archives/archive-2011-08-30-21-45-18/Genes/genes.gtf
"""

another_sample = """
[COMMANDS]
# Trimmomatic
java -jar trimmomatic PE {1} {2} {o} {o} {o} {o} ILLUMINACLIP:Trimmomatic-0.35/adapters/TruSeq3-PE.fa:2:30:10:2:true LEADING:3 TRAILING:3

# Unzip the outputs from trimmomatic
gzip --stdout -d {1.1-1||1.1-3} > {o}

# Cutadapt
# cutadapt needs unzipped fastq files
cutadapt --cut 7 -o {o} {2.1||2.2}

# BowTie
bowtie2 --very-sensitive -N 1 -p 8 -x HG_19 -q -1 {3.1} -2 {3.2} -S {o}

# HTSeq
htseq-count {4.1} gene_list > {o}

# Summary
head --lines -5 {5.1} > {o}

[PATHS]
trimmomatic Trimmomatic-0.35/trimmomatic-0.35.jar
cutadapt ~/.local/bin/cutadapt
HG_19 hg19_ucsc.1.bt2
gene_list genes.gtf


[FILES]
1. somefile.1
2. somefile.2
"""

long_running = """
[COMMANDS]
cat {1||2||3||4} > {o} && sleep 1
cat {1.1||1.2} && sleep 1

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6
"""

full_output_file_name = """
[COMMANDS]
gzip --stdout {1} > {o.gz}
cat {1.1} > {o.gz}
cat {2.1} > {o.gz}
cat {2.1} > {o.gz}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
5. somefile.5
6. somefile.6
"""
