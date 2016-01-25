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

file = """1. somedir/somefile.ext"""

path = """python /usr/bin/python"""

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


