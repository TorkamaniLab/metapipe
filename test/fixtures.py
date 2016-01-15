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
paste *.counts > {o:some.file}

./somescript {1,2,3,4||test/files/*.counts,}

rb somescript.rb -i {test/files/*.counts||}
python somescript.py -i {test/files/*.counts,} > {o:*.bam}

[FILES]
1. test/files/somefile.1
2. test/files/somefile.2
3. test/files/somefile.3
4. test/files/somefile.4
5. test/files/somefile.5
6. test/files/somefile.6

[PATHS]
python /usr/bin/python
bash /usr/bin/bash
rb /usr/bin/ruby
"""


