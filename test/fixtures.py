from metapipe.models import *

# Snippets

basic_cmd = {
    'text': """python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh \
 somefile.txt
""",
    'template_parts': [
        'python', 'somescript.py', '-i',
        [[Input('1'), Input('2'), Input('3')],
        [Input('4'), Input('5'), Input('6')]],
        '-o', Output('1.1'), '-fgh'
    ],
    'command_parts': [
        ['python', 'somescript.py', '-i',
            [Input('1'), Input('2'), Input('3')],
            '-o', Output('1.1'), '-fgh'],
        ['python', 'somescript', '-i',
            [Input('4'), Input('5'), Input('6')],
            '-o', Output('1.1'), '-fgh']
    ]
}

magic_cmd = {
    'text': """python somescript.py {*.counts||} > someout
""",
    'template_parts': [
        ['python', 'somescript.py', '-i',
            [Input('*.counts', and_or='||'), 'someout'],
        ]
    ]

}

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

cmd_comment = """# Some comment
#Some other comment
bash somescript {1,2,3} > {o.gz}
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
# Some top comment
# Another top comment
# A third top comment
# Woo!

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
 #THIS IS A COMMENT
4. somefile.4
5. somefile.5
6. somefile.6

[PATHS]
python /usr/bin/python
# THIS IS also A COMMENT
bash /usr/bin/bash
rb /usr/bin/ruby
cat2 module load cat2; cat2

[JOB_OPTIONS]
#PBS_O_WORKDIR=~/someuser
set -e;
module load python
# do something

[OPTIONS]
module load python;
set -e
"""


overall_cmd_templates = [
    CommandTemplate('1', [
        PathToken('python', '/usr/bin/python'),
        'somescript.py',
        '-i',
        [[
            Input('1', filename='somefile.1'),
            Input('2', filename='somefile.2'),
            Input('3', filename='somefile.3'),
        ],
        [
            Input('4', filename='somefile.4'),
            Input('5', filename='somefile.5'),
            Input('6', filename='somefile.6'),
        ]],
        '-o',
        Output('1'),
        '-fgh',
        'somefile.txt',
        ]),
]


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

multiple_input_vals = ['bash', 'somescript',
    [[Input('1', 'somefile.1')], [Input('2', 'somefile.2')],
        [Input('3', 'somefile.3')]], '--conf',
    [[Input('4', 'somefile.4')], [Input('5', 'somefile.5')],
        [Input('6', 'somefile.6')]],
    '>', Output('1', 'metapipe.1.output')]



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

multiple_output_vals = ['bash', 'somescript',
    [[Input('1', 'somefile.1')], [Input('2', 'somefile.2')],
        [Input('3', 'somefile.3')]], '--log',
    Output('1', 'metapipe.1.output'), '-r',
    Output('1', 'metapipe.1.output')]



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
cutadapt --cut 7 -o {o} {2.*||}

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

one_step_pipeline = """
[COMMANDS]
cut somefile > anotherfile
"""

concurrent = """
[COMMANDS]
# Each one has 10
cat {1||2||3||4||1||2||3||4||1||2} > {o}
cat {1||2||3||4||1||2||3||4||1||2} > {o}
cat {1||2||3||4||1||2||3||4||1||2} > {o}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4
"""


magical_glob = """
[COMMANDS]
split -o breakdown {1} #{o:breakdown/*}
cat {1.*} > {o}
diff {2.*} {1}

[FILES]
1. somefile.1
2. somefile.2
"""

magical_glob2 = """
[COMMANDS]
split -o breakdown {1} #{o:breakdown/*}
cat {1.*||} > {o}
diff {2.*} {1}

[FILES]
1. somefile.1
2. somefile.2
"""


# Job Fixtures

pbs_job_qstat_queued = ("""Job id           Name             User             Time Use S Queue
---------------- ---------------- ---------------- -------- - -----
4807             scatter          user01           12:56:34 Q batch
""", None)

pbs_job_qstat_running = ("""Job id           Name             User             Time Use S Queue
---------------- ---------------- ---------------- -------- - -----
4807             scatter          user01           12:56:34 R batch
""", None)

pbs_job_qsub = ("""9974279.garibaldi01-adm.cluster.net""", None)



sge_job_qstat_queued = ("""job-ID prior name user state submit/start at queue slots ja-task-ID
-------------------------------------------------------------------
1 0.00000 hostname sgeadmin qw 09/09/2009 14:58:00 1
""", None)

sge_job_qstat_running = ("""job-ID prior name user state submit/start at queue slots ja-task-ID
-------------------------------------------------------------------
6 0.55500 jobscript. sgeadmin r 09/09/2009 16:18:57 all.q@node001.c 1
""", None)

sge_job_qsub = ("""Your job 1 ("hostname") has been submitted""", None)
