cmd = """python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh \
 somefile.txt
"""

file = """1. somedir/somefile.ext"""

path = """python /usr/bin/python"""

overall = """
# Somethng
[COMMANDS]
python somescript.py -i {1,2,3||4,5,6} -o {o} -fgh somefile.txt
bash somescript.sh -i {1.2,2.2,3.2||4.2,5.2,6.2} -o {o} -fgh \
somefile.txt
rb somescript.rb -i {1.1,2.1,3.1||4.1,5.1,6.1||1.2, 1.1} >> somefile
# Somethng
rb somescript.rb -i {*.counts||}
python somescript.py -i {*.counts,} > {o:*.bam}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3
4. somefile.4

[PATHS]
python /usr/bin/python
bash /usr/bin/bash
rb /usr/bin/ruby
"""


