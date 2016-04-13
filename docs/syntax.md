# Metapipe Syntax

The syntax for Pipeline Config files is as follows.


## Section Definitions

In each Metapipe file, there are a number of different sections you can specify. Each has their own purpose and function. Each section is denoted with a header in brackets at the top of the section.

All sections support comments, and in most sections, they are not parsed as input.


### Commands

The commands section is the only required Metapipe config section. Specified by the `[COMMANDS]` header, this is where the various steps of the pipeline are specified. Commands are very similar to normal shell commands, and most shell commands are valid. The only difference is in the input/output of each command. For these sections, use Metapipe's command syntax to indicate the location and desired input and output.

**Example:**

```bash
[COMMANDS]
# Here we cat a hardcoded input file into sed
# and redirect the output to a metapipe output token.
cat somefile.txt | sed 's/replace me/with me' > {o}
```

Metapipe automatically creates a filename for the given output token and assigns that file an alias. The alias structure is `command_number.command_iteration-output_number`, where the output number is optional.

**Important:** Commands are *NOT* run sequentially. As commands are parsed, they are evaluated based on what inputs they take in and what outputs they generate. For more information: see [Command Structure](#command-structure). Commands are run as soon as they are deemed ready and any command that does not specify inputs via Metapipe's input patterns will be run immediately.


### Paths

The paths section allows users to simplify their commands by creating aliases or short names to binaries. Paths are structured as a single word alias followed by a space and the rest of the line is considered the path. The paths section is denoted by the `[PATHS]` header.

```bash
[COMMANDS]
# Here we've aliased Python. When the script is generated,
# the hardcoded path will be substituted in.
python2 my_script.py

# Here we're using the builtin python and using paths
# to simplify the arguments.
python my_script.py somefile

[PATHS]
python2 /usr/local/bin/python2.7.4
somefile /a/long/file/path
```

Paths can also be used to create pseudo-variables for long configuration options. When doing this, it's recommended to use a bash-variable-like syntax because it reminds the reader that the variable is not a literal in the command.

**Reminder**: Paths are substituted in after the inputs have been processed. This means that `{}` characters are treated as literals and not as input markers.

```bash
[COMMANDS]
# Here, the braces represent an output token,
# but the $OPTIONS variable will be evaluated
# as a literal {}
python my_script.py -o {o} $OPTIONS

[PATHS]
$OPTIONS -rfg --do-something --no-save --get --no-get -I {}
```


### Files

For a given pipeline, there is usually a set of input or auxiliary files. These files go through the analysis and other steps require the output of one command as the input for another. This is where most of the power of Metapipe's syntax comes into play. The files section is denoted as `[FILES]`.

Files are specified using a number followed by a period, and then the path to the given file. The number is the file's alias, and once that alias is assigned, it can be used in commands.

```bash
[COMMANDS]
cat {1} | sed 's/replace me/with me' > {o}
cat {2} | cut -f 1 | sort | uniq > {o}

[FILES]
1. somefile.1
2. /path/to/somefile.2

```

In this example, we use the aliases of files 1 and 2 to perform different analysis on each file. Then, when the input files need to change, they can be changed in the `[FILES]` section and the pipeline remains the same.


### Job Options

The job options section, denoted by `[JOB_OPTIONS]`, is a section that allows the user to specify a global set of options for all jobs. This helps reduce pipeline redundancy.

```bash
# Each of the commands in this pipeline need to
# be working in a scratch directory.
[COMMANDS]
cat somefile.1.txt | sed 's/replace me/with me' > {o}
cat somefile.2.txt | sed 's/replace me/with you' > {o}
cat somefile.3.txt | sed 's/replace you/with me' > {o}

[JOB_OPTIONS]
set -e
cd /var/my_project/

# This config will result in the following:
# ------- Job 1 ---------
set -e
cd /var/my_project/
cat somefile.1.txt | sed 's/replace me/with me' > {o}
```

The set of commands in Job Options will be carried over to every job in the pipeline. This can be extremely useful when setting configuration comments for a queue system.

```bash
# Each of the commands needs 4GB of RAM
[COMMANDS]
cat somefile.1.txt | sed 's/replace me/with me' > {o}
cat somefile.2.txt | sed 's/replace me/with you' > {o}
cat somefile.3.txt | sed 's/replace you/with me' > {o}

[JOB_OPTIONS]
#PBS -l mem=4096mb
```

Job Options allow users to make their pipelines more clear and less redundant by allowing them to follow the [DRY][dry] principle.

[dry]: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself


## Command Structure

Now that all of the concepts and supported sections have been explained, it's time to take a look at the command structure and how to take advantage of Metapipe's advanced features.


### Input Patterns

Consider the following command:

```bash
[COMMANDS]
python somescript {1||2||3}

[FILES]
1. some_file1.txt
2. some_file2.txt
3. some_file3.txt
```

This command will run the python script 3 times in parallel, once with each
file specified. The output will look something like this:

```bash
# Output
# ------

python somescript some_file1.txt
python somescript some_file2.txt
python somescript some_file3.txt
```

#### Running a script with multiple inputs

Let's say that you have a script with takes multiple files as input. In this
case the syntax becomes:

```bash
[COMMANDS]
python somescript {1,2,3}

[FILES]
1. some_file1.txt
2. some_file2.txt
3. some_file3.txt

# Output
# ------

python somescript some_file1.txt some_file2.txt some_file3.txt
```


### Output Patterns

Whenever a script would take an explicit output filename you can use the output
pattern syntax to tell metapipe where/what it should use.

```bash
[COMMANDS]
python somescript -o {o} {1||2||3}

[FILES]
1. some_file1.txt
2. some_file2.txt
3. some_file3.txt

# Output
# ------

python somescript -o mp.1.1.output some_file1.txt
python somescript -o mp.1.2.output some_file2.txt
python somescript -o mp.1.3.output some_file3.txt
```

Metapipe will generate the filename with the command's alias inside. An upcoming feature will provide more useful output names.


#### Implicit or Hardcoded output

In a case where the script or command you want to use generates an output that
is not passed through the command, but you need to use for another step in the
pipeline, you can use output patterns to tell metapipe what to look for.

Consider this:

```bash
[COMMANDS]
# This command doesn't provide an output filename
# so metapipe can't automatically track it.
./do_count {1||2}
./analyze.sh {1.*}

[FILES]
1. foo.txt
2. bar.txt
```

This set of commands is invalid because the second command (`./analyze.sh`)
doesn't know what the output of command 1 is because it isn't specified.
The split command generates output based on the input filenames it is given.

Since we wrote the `./do_count` script, we know that it generates files with a
`.counts` extension. But since we don't explicitly specify the files, in
this case Metapipe cannot assume the file names generated by step 1 and this
config file is invalid.

We can tell metapipe what the output should look like by using an output pattern.

```bash
[COMMANDS]
# We've now told Metapipe what the output file name
# will look like. It can now track the file as normal.
./do_counts {1||2} #{o:*.counts}
./analyze.sh {2.*}

[FILES]
1. foo.txt
2. bar.txt
```

The above example tells metapipe that the output of command 1, which is
hardcoded in the script will have an output that ends in `.counts`. Now that
the output of command 1 is known, command 2 will wait until command 1 finishes.

When the output marker has the form `{o}`, then metapipe will insert a
pregenerated filename to the command. The output marker `{o:<pattern>}` means
that the output of the script is *not* determined by the input of the script,
but it *will* match given pattern. This means that later commands will be able
to reference the files by name.


### Multiple Inputs and Outputs

Often times a given shell command will either take multiple dynamic files as input, or generate multiple files as output. In either case, metapipe provides a way to manage and track these files.

For multiple inputs, metapipe expects the number of inputs per command to be the same, and will iterate over them in order.

**Example:**

```bash
# Given the following:
[COMMANDS]
bash somescript {1||2||3} --conf {4||5||6}  > {o}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3

# Metapipe will return this:
bash somescript somefile.1 --conf somefile.4  > mp.1.1.output
bash somescript somefile.2 --conf somefile.5  > mp.1.2.output
bash somescript somefile.3 --conf somefile.6  > mp.1.3.output
```

Metapipe will name the multiple output files as follows (in order from left to right):

`mp.{command_number}.{sub_command_number}-{output_number}`

**Example:**

```bash
# Given an input like the one below:
[COMMANDS]
bash somescript {1||2||3} --log {o} -r {o}

[FILES]
1. somefile.1
2. somefile.2
3. somefile.3

# metapipe will generate the following:
bash somescript somefile.1 --log mp.1.1-1.output -r mp.1.1-2.output
bash somescript somefile.2 --log mp.1.2-1.output -r mp.1.2-2.output
bash somescript somefile.3 --log mp.1.3-1.output -r mp.1.3-2.output
```



## Sample config.mp file

```bash
[COMMANDS]
# Here we run our analysis script on every gzipped file
# in the current directory and output the results to a file.
python my_custom_script.py -o {o} {*.gz||}

# Take all the outputs of step 1 and feed them to cut.
cut -f 1 {1.*||} > {o}

# Oh no! You hardcode the output name? No problem! Just tell metapipe
# what the filename is.
python my_other_custom_code.py {2.*} #{o:hardcoded_output.csv}

# Now you want to compare your results to some controls? Ok!
# Metapipe wil compare your hardcoded_output to all 3
# controls at the same time!
python my_compare_script.py -o {o} $OPTIONS --compare {1||2||3} {3.1}

# Finally, you want to make some pretty graphs? No problem!
# But wait! You want R 2.0 for this code? Just create an alias for R!
Rscript my_cool_graphing_code.r {4.*} > {o}

[FILES]
1. controls.1.csv
2. controls.2.csv
3. controls.3.csv

[PATHS]
Rscript ~/path/to/my/custom/R/version
$OPTIONS -rne --get --no-get -v --V --log-level 1
```
