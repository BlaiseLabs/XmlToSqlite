# XmlToSqlite

XmlToSqlite is a Python package for parsing XML data and storing it in a SQLite database. It supports both hierarchical and flat XML structures.

## Features

- Parse hierarchical and flat XML structures.
- Create SQLite database schemas based on XML structure.
- Insert parsed XML data into SQLite database.

## Installation

To use XmlToSqlite, clone this repository and install the required packages:

```bash
git clone https://github.com/your-username/XmlToSqlite.git
cd XmlToSqlite
pip install -r requirements.txt
```

## Usage

### Hierarchical XML Parsing

```python
from xmltosqlite.hierarchical_strategy import HierarchicalStrategy

strategy = HierarchicalStrategy()
parsed_structure = strategy.parse_xml(xml_string)
strategy.create_database_schema(db_path, parsed_structure)
strategy.insert_data_into_database(db_path, parsed_structure)
```

### Flat XML Parsing

```python
from xmltosqlite.flat_strategy import FlatStrategy

strategy = FlatStrategy()
parsed_structure = strategy.parse_xml(xml_string)
strategy.create_database_schema(db_path, parsed_structure)
strategy.insert_data_into_database(db_path, parsed_structure)
```

## Running Tests

To run unit tests, navigate to the root directory of the project and execute:

```bash
python -m unittest discover
```

## Contributing

Contributions to XmlToSqlite are welcome. Please ensure your pull requests are well-documented and include unit tests for new functionality.

## License

[MIT License](LICENSE)
Copyright (c) 2023 Blaiselabs

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.