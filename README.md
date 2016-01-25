# Metapipe

*A pipeline for building analysis pipelines.*

[![Build Status](https://travis-ci.org/TorkamaniLab/metapipe.svg)](https://travis-ci.org/TorkamaniLab/metapipe)
[![Coverage Status](https://coveralls.io/repos/github/TorkamaniLab/metapipe/badge.svg?branch=master)](https://coveralls.io/github/TorkamaniLab/metapipe?branch=master)

Metapipe is a simple command line tool for building and running complex analysis pipelines. If you use a PBS/Torque queue for cluster computing, or if you have complex batch processing that you want simplified, matapipe is the tool for you.

Metapipe's goal is to improve **readability**, and **maintainability** when building complex pipelines.
 

## What does it do?

In the bad old days (before metapipe), if you wanted to make an analysis pipeline, you needed to know how to code. **Not anymore!** Metapipe makes it easy to build and run your analysis pipelines! **No more code, just commands!** This makes your pipelines easy to understand and change! 

**Here's a sample!**

Let's say I have a few command-line tools that I want to string together into a pipeline. I used to have to know Python, Perl, Bash, or some other scripting language; now I can use Metapipe!


    [COMMANDS]
    # Trim and cut your sample fastq files.
    # Metapipe will handle naming the output files for you!
    # Metapipe will trim all of the files at once! (see parallel)
    trimmomatic -o {o} {*.fastq.gz||}
    
    # Metapipe will manage your dependencies for you!
    # Take all the outputs of step 1 and feed them to cutadapt.
    cutadapt -o {o} {metapipe.1.*.output||}

    # Next you need to align them.
    htseq <alignment options> -o {o} {metapipe.2.*.output||}

    # Of course, now you'll have some custom code to put all the data together. 
    # That's fine too!
    
    # Oh no! You hardcode the output name? No problem! Just tell metapipe 
    # what the filename is.
    python my_custom_code.py {metapipe.3.*.output,} #{o:hardcoded_output.csv}
    
    # Now you want to compare your results to some controls? Ok!
    # Metapipe wil compare your hardcoded_output to all 3 controls at the same time!
    python my_compare_script.py {hardcoded_output.csv} --compare-to {1||2||3}
    
    # Finally, you want to make some pretty graphs? No problem!
    # But wait! You want R 2.0 for this code? Just create an alias for R!
    Rscript my_cool_graphing_code.r {metapipe.5.*.output} > {o}
    
    [FILES]
    1. controls.1.csv
    2. controls.1.csv
    3. controls.1.csv

    [PATHS]
    Rscript ~/path/to/my/custom/R/version
    
Excluding the comments, this entire analysis pipeline is 13 lines long, and extremely readable! What's even better? If you want to change any steps, its super easy! That's the power of Metapipe!



