# Metapipe

*A pipeline for building analysis pipelines.*

Metapipe is a simple command line tool for building and running complex analysis pipelines. If you use a PBS/Torque queue for cluster computing, or if you have complex batch processing that you want simplified, metapipe is the tool for you.

Metapipe's goal is to improve **readability**, and **maintainability** when building complex pipelines.

In addition to helping you generate and maintain complex pipelines, **metapipe also helps you debug them**! How? Well metapipe watches your jobs execute and keeps tabs on them. This means, unlike conventional batch queue systems like PBS/Torque alone, metapipe can give you accurate error information, and even resubmit failing jobs! Metapipe enhances the power of any PBS/Torque queue! 

- What if I [don't use PBS/Torque](#other-queue-systems), or [a queue system at all?](#no-queue-no-problem)


## What does it do?

In the bad old days (before metapipe), if you wanted to make an analysis pipeline, you needed to know how to code. **Not anymore!** Metapipe makes it easy to build and run your analysis pipelines! **No more code, just commands!** This makes your pipelines easy to understand and change! 

A sample metapipe file can be found in [Metapipe Syntax](syntax.html)


## No Queue? No Problem!

Lots of people don't use a PBS/Torque queue system, or a queue system at all, and metapipe can help them as well! Metapipe runs locally and will give you all the same benefits of a batch queue system! It runs jobs in parallel, and provide detailed feedback when jobs go wrong, and automatic job re-running if they fail.

To run metapipe locally, see the app's help menu!

`metapipe --help`


## Other Queue Systems

Metapipe is a very modular tool, and is designed to support any execution backend. Right now we only support PBS, but if you know just a little bit of Python, you can add support for any queue easily! *More information coming soon!*

