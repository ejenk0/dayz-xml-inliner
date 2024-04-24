# DayZ XML inliner

## Installation

- Ensure you have a recent version of Python 3 installed.
- Clone this repository.

## Usage

Use `python3 dayz_xml_inliner.py -h` to see the available options.

- Paths in the `<include>` tags must are expected to be in Windows format (Using `\` not `/`).
- Currently, all included files will be appended to the root (`<Project>` in this case) tag. This means nesting is not supported.
- The inliner will ignore any tags which are not `<include>`.
  - All `<include>` tags will be replaced with the contents of the file they point to.
- Paths in the `<include>` tags must be relative to the input file.
  For example, with the following directory structure:

  ```plaintext
  example_files
  |   input.xml
  |   xml
      |   included.xml
      |   another_included.xml
  ```

  `input.xml` should look like:

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <Project name="DayZ Rising">
      <include>xml\included.xml</include>
      <include>xml\another_included.xml</include>
  </Project>
  ```

### Example usage

`-vbf` means we will see verbose output (`-v`) with benchmark times (`-b`) and if the output file already exists, it will be overwritten (`-f`).

**POSIX (MacOS, Linux)**

```bash
python3 dayz_xml_inliner.py -vbf ./example_files/input_5k.xml ./example_files/output.xml
```

**Windows**

```cmd
python dayz_xml_inliner.py -vbf .\example_files\input_5k.xml .\example_files\output.xml
```

### `--help`

```plaintext
usage: python3 dayz_xml_inliner.py [-h] [-f] [-v] [-s] [-b] input output

Parse an XML file with include tags and emit a new XML file with the included files inlined.

positional arguments:
  input            The input XML file
  output           The output XML file

options:
  -h, --help       show this help message and exit
  -f, --force      Overwrite the output file if it already exists
  -v, --verbose    Print verbose output
  -s, --silent     Suppress all output. WARN: The program fail silently.
  -b, --benchmark  Run the program in benchmark mode.
```
