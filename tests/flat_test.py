import sqlite3
import unittest
from ..XmlToSqlite import FlatStrategy

# Sample flat XML data
sample_flat_xml = """
<devices>
    <device>
        <name>Device A</name>
        <id>1</id>
        <manufacturer>Company X</manufacturer>
    </device>
    <device>
        <name>Device B</name>
        <id>2</id>
        <manufacturer>Company Y</manufacturer>
    </device>
</devices>
"""

# Unit tests for the FlatStrategy class including database interactions
class TestFlatStrategyDatabase(unittest.TestCase):
    """Unit tests for the FlatStrategy class including database interactions."""
    def test_parse_xml(self):
        """
        Test the parsing of XML data into a structured representation.
        """
        strategy = FlatStrategy()

        # Sample flat XML data
        sample_flat_xml = """
        <devices>
            <device>
                <name>Device A</name>
                <id>1</id>
                <manufacturer>Company X</manufacturer>
            </device>
            <device>
                <name>Device B</name>
                <id>2</id>
                <manufacturer>Company Y</manufacturer>
            </device>
        </devices>
        """

        parsed_structure = strategy.parse_xml(sample_flat_xml)
        # Verify the parsed structure
        expected_structure = [{
            'table': 'device', 
            'columns': {'name': 'Device A', 'manufacturer': 'Company X'},
            'foreign_keys': []
            }, 
            {
            'table': 'device',
            'columns': {
                'name': 'Device B',
                'manufacturer': 'Company Y'
                }, 
            'foreign_keys': []
            },
            {
            'table': 'devices', 
            'columns': {},
            'foreign_keys': ['device']
            }
        ]


        self.assertEqual(parsed_structure, expected_structure, "Parsed structure doesn't match expectations")


    def test_create_database_schema(self):
        """
        Test the creation of a database schema based on parsed flat XML structure.

        """
        strategy = FlatStrategy()
        db_path = './temp_sqlite_db_flat.db'  # Temporary database path for testing
        parsed_structure = strategy.parse_xml(sample_flat_xml)  # Using the previously parsed structure

        strategy.create_database_schema(db_path, parsed_structure)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

        self.assertIn(('device',), tables, "Device table not found in database")
        self.assertIn(('devices',), tables, "Devices table not found in database")

    def test_insert_data_into_database(self):
        """
        Test the insertion of data into the database based on parsed flat XML structure.

        """
        strategy = FlatStrategy()
        db_path = './temp_sqlite_db_flat.db'  # Temporary database path for testing
        parsed_structure = strategy.parse_xml(sample_flat_xml)  # Using the previously parsed structure

        strategy.create_database_schema(db_path, parsed_structure)
        strategy.insert_data_into_database(db_path, parsed_structure)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM device;")
            data = cursor.fetchall()

        self.assertTrue(data, "No data found in device table")

# Running the unit tests for database schema creation and data insertion
if __name__ == '__main__':
    unittest.TextTestRunner().run(
      unittest.TestLoader().loadTestsFromTestCase(TestFlatStrategyDatabase)
    )
    