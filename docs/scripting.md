# Scripting Metapipe

In addition to being a command line tool, metapipe is also a Python module. You can use this module to extend, or script metapipe to fit your specific uses. This section will discuss scripting metapipe, and building/running jobs using Python. For information on how to extend metapipe's builtin job types or queue system, see [Extending Metapipe](extending.html).


## The Run Interface

The first, and easiest way to script Metapipe is by invoking it via the Python interface.


```python
from metapipe import run

config_text = get_config_text()
run(config_text)
```

For detailed information, see the [run method's docstring](https://github.com/TorkamaniLab/metapipe/blob/master/metapipe/app.py#L90).

