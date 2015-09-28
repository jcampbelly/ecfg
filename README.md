# ecfg

[![Build Status](https://travis-ci.org/jcampbelly/ecfg.svg)](https://travis-ci.org/jcampbelly/ecfg)

An Enlightenment config parser.

See: http://wiki.openmoko.org/wiki/Enlightenment_.cfg

Requires pyparsing: https://pyparsing.wikispaces.com/.

# Installation

```
python setup.py install
```

# Usage from CLI

Help text for the `ecfg` command.

```
usage: ecfg [-h] [--format {text,xml,json}] filename

Parse e.cfg files

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  --format {text,xml,json}
                        Output format
```

Example usage:

```bash
ecfg e.cfg --format xml
```

# Usage as a Library

```python
import ecfg

# parse the current config
with open('tests/sample.cfg') as f:
    text = f.read()

result = ecfg.ECfg(text)

# manipualte the config
for value in result.root.values:
    if value.name == 'struct_value':
        value.data = 'new_value'

# save the new config
with open('e2.cfg', 'w') as f:
    f.write(result.text())
```

The `ecfg` module exposes some classes.

- `ECfg` The main interface for interacting with a config file. Pass the
  raw text of a config to the constructor and use the `root` property to work
  with the config data.
- `ECfgParser` A parser class, exposing a single class method: `parse(text)`,
  which must return a pyparsing `ParseResults` object.
- `Struct`
    - `name` Struct name.
    - `lists` List of List objects in this Struct.
    - `values` List of Value objects in this Struct.
    - `dict()` Return the Struct as an OrderedDict.
    - `text()` Return the Struct as a config text block.
- `List`
    - `name` List name.
    - `items` List of Struct objects in this List.
    - `values` List of Value objects in this List.
    - `dict()` Return the List as an OrderedDict.
    - `text()` Return the List as a config text block.
- `Value`
    - `name` Value name.
    - `type` Value type: uchar, uint, int, float, double, string.
    - `data` The string data as represented in the e.cfg text block.
    - `dict()` Return the Value as an OrderedDict.
    - `text()` Return the Value as a config text block.
    - `value` A getter which returns the Value data as its actual Python data
      type. Uses the following mapping for each type:
          - "uchar", "uint", "int" -> ``int``
          - "float", "double" -> ``decimal.Decimal``.
          - "string" -> ``str``.

An `ECfg` instance exposes some properties and methods:

- `root` The root `Struct` parsed from the config.
- `text()` Return the Enlightenment config text.
- `xml()` Return the XML representation of the config.
- `json()` Return the JSON representation of the config.

# Testing

This library is tested with Python 2.7, 3.2, 3.3, 3.4, 3.5, and 3.5-dev.

To install test requirements, use:

```
pip install -r requirements.txt -r test_requirements.txt
```

Use the provided test script to see flake8 and coverage reports as well.

```
./test.sh
```

# Author

Jimmy Campbell <jcampbelly@gmail.com>
