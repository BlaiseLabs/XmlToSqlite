from bs4 import BeautifulSoup
import sqlite3
from .utils import quote_name, sanitize_name

def quote_name(name):
    """
    Ensure the SQL name is properly quoted to handle reserved keywords.

    Args:
        name (str): The name to be quoted.

    Returns:
        str: The quoted name.
    """
    return f'"{name}"'

def sanitize_name(name):
    """
    Sanitize a name to handle reserved SQL keywords.

    Args:
        name (str): The name to be sanitized.

    Returns:
        str: The sanitized name.
    """
    name = name.strip("[]")
    reserved_words = {"table", "select", "insert", "update", "delete", "where"}
    return f'_{name}_' if name.lower() in reserved_words else name    

# Correcting indentation and re-implementing the HierarchicalStrategy class
class Strategy:
    """Base class for XML parsing and database operations strategy."""
    def parse_xml(self, xml_string):
        """
        Parse XML data and return a structured representation.

        Args:
            xml_string (str): The XML data as a string.

        Returns:
            list: A list of dictionaries representing the parsed structure.
        """
        raise NotImplementedError

    def create_database_schema(self, db_path, parsed_structure):
        """
        Create a database schema based on the parsed structure.

        Args:
            db_path (str): The path to the SQLite database.
            parsed_structure (list): A list of dictionaries representing the parsed structure.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        raise NotImplementedError

    def insert_data_into_database(self, db_path, parsed_structure):
        """
        Insert data into the database based on the parsed structure.

        Args:
            db_path (str): The path to the SQLite database.
            parsed_structure (list): A list of dictionaries representing the parsed structure.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        raise NotImplementedError


class HierarchicalStrategy(Strategy):
    """Strategy for hierarchical XML parsing and database operations."""
    def parse_xml(self, xml_string):
        """
        Parse hierarchical XML data and return a structured representation.

        Args:
            xml_string (str): The hierarchical XML data as a string.

        Returns:
            list: A list of dictionaries representing the parsed structure.
        """
        soup = BeautifulSoup(xml_string, 'xml')
        root = soup.find()  # Get the root element

        def extract_structure(element, parent=None):
            tag = sanitize_name(element.name)
            structure = {'table': tag, 'columns': {}, 'foreign_keys': set(), 'parent': parent}

            for child in element.find_all(recursive=False):
                child_name = sanitize_name(child.name)
                if child.find_all(recursive=False):
                    structure['foreign_keys'].add(child_name)
                    yield from extract_structure(child, parent=tag)
                else:
                    if child_name != 'id':
                        structure['columns'][child_name] = child.get_text(strip=True)

            structure['foreign_keys'] = list(structure['foreign_keys'])  # Convert set back to list
            yield structure

        return list(extract_structure(root))

    def create_database_schema(self, db_path, parsed_structure):
        """
        Create a database schema based on the parsed structure.

        Args:
            db_path (str): The path to the SQLite database.
            parsed_structure (list): A list of dictionaries representing the parsed structure.

        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            for element in parsed_structure:
                table_name = quote_name(element['table'])
                columns = [quote_name('id') + " INTEGER PRIMARY KEY AUTOINCREMENT"]
                for attribute in element['columns']:
                    columns.append(quote_name(attribute) + " TEXT")
                for fk in element['foreign_keys']:
                    fk_column_name = quote_name(fk + "_id")
                    columns.append(f"{fk_column_name} INTEGER REFERENCES {quote_name(fk)}(id)")

                table_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
                cursor.execute(table_statement)

    def insert_data_into_database(self, db_path, parsed_structure):
        """
        Insert data into the database based on the parsed structure.

        Args:
            db_path (str): The path to the SQLite database.
            parsed_structure (list): A list of dictionaries representing the parsed structure.

        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            for element in parsed_structure:
                table_name = quote_name(element['table'])
                columns = element['columns']
                if columns:
                    column_names = [quote_name(col) for col in columns.keys()]
                    placeholders = [":" + col for col in columns.keys()]
                    insert_statement = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(placeholders)});"
                    cursor.execute(insert_statement, columns)






class FlatStrategy(Strategy):
  """Strategy for flat XML parsing and database operations."""

  def parse_xml(self, xml_string):
      """
      Parse flat XML data and return a structured representation.

      Args:
          xml_string (str): The flat XML data as a string.

      Returns:
          list: A list of dictionaries representing the parsed structure.
      """
      soup = BeautifulSoup(xml_string, 'xml')
      root = soup.find()  # Get the root element

      def extract_structure(element):
          tag = sanitize_name(element.name)
          structure = {'table': tag, 'columns': {}, 'foreign_keys': set()}

          for child in element.find_all(recursive=False):
              child_name = sanitize_name(child.name)
              if child.find_all(recursive=False):
                  structure['foreign_keys'].add(child_name)
                  yield from extract_structure(child)
              else:
                  if child_name != 'id':
                      structure['columns'][child_name] = child.get_text(strip=True)

          structure['foreign_keys'] = list(structure['foreign_keys'])  # Convert set back to list
          yield structure

      return list(extract_structure(root))

  def create_database_schema(self, db_path, parsed_structure):
      """
      Create a database schema based on the parsed structure.

      Args:
          db_path (str): The path to the SQLite database.
          parsed_structure (list): A list of dictionaries representing the parsed structure.

      """
      with sqlite3.connect(db_path) as conn:
          cursor = conn.cursor()

          for element in parsed_structure:
              table_name = quote_name(element['table'])
              columns = [quote_name('id') + " INTEGER PRIMARY KEY AUTOINCREMENT"]
              for attribute in element['columns']:
                  columns.append(quote_name(attribute) + " TEXT")
              for fk in element['foreign_keys']:
                  fk_column_name = quote_name(fk + "_id")
                  columns.append(f"{fk_column_name} INTEGER REFERENCES {quote_name(fk)}(id)")

              table_statement = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
              cursor.execute(table_statement)

  def insert_data_into_database(self, db_path, parsed_structure):
      """
      Insert data into the database based on the parsed structure.

      Args:
          db_path (str): The path to the SQLite database.
          parsed_structure (list): A list of dictionaries representing the parsed structure.

      """
      with sqlite3.connect(db_path) as conn:
          cursor = conn.cursor()

          for element in parsed_structure:
              table_name = quote_name(element['table'])
              columns = element['columns']
              if columns:
                  column_names = [quote_name(col) for col in columns.keys()]
                  placeholders = [":" + col for col in columns.keys()]
                  insert_statement = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(placeholders)});"
                  cursor.execute(insert_statement, columns)