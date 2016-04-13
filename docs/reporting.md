# Measuring Pipeline Progress

While Metapipe runs your pipeline, it writes updates to `stdout`. These can be helpful, but most times it can be more helpful to get additional information in a more helpful format.

Metapipe provides a few different methods of visualizing the progress of your pipeline. These options are specified by the `--report-type` option.


## Text based reporting

```
--report-type text
```

This option is the default. Metapipe will write to `stdout` and this can be redirected to a file.


## HTML based reporting

```
--report-type html
```

Using this option, Metapipe will generate an HTML report of the pipeline as it runs. This static report represents the current state of the pipeline and what steps have already been completed. The report also includes a progress bar that reports a visualization of the rough progress of the pipeline.

**Important:** This progress indicator is based on the number of overall steps to be completed and represents the number of steps remaining. This has no correlation with the amount of time remaining, as that depends on the length of time each step takes.
