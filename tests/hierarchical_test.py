
import unittest
import sqlite3
from ..XmlToSqlite import HierarchicalStrategy

sample_xml = """
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

# Unit tests for the HierarchicalStrategy class including database interactions
class TestHierarchicalStrategyDatabase(unittest.TestCase):
    """Unit tests for the HierarchicalStrategy class including database interactions."""
    def test_create_database_schema(self):
        """
        Test the creation of a database schema based on parsed XML structure.

        """
        strategy = HierarchicalStrategy()
        db_path = './temp_sqlite_db.db'  # Temporary database path for testing
        parsed_structure = strategy.parse_xml(sample_xml)  # Using the previously parsed structure

        strategy.create_database_schema(db_path, parsed_structure)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

        self.assertIn(('device',), tables, "Device table not found in database")
        self.assertIn(('devices',), tables, "Devices table not found in database")

    def test_insert_data_into_database(self):
        """
        Test the insertion of data into the database based on parsed XML structure.

        """
        strategy = HierarchicalStrategy()
        db_path = './temp_sqlite_db.db'  # Temporary database path for testing
        parsed_structure = strategy.parse_xml(sample_xml)  # Using the previously parsed structure

        strategy.create_database_schema(db_path, parsed_structure)
        strategy.insert_data_into_database(db_path, parsed_structure)

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM device;")
            data = cursor.fetchall()

        self.assertTrue(data, "No data found in device table")

if __name__ == '__main__':
  
  # Running the unit tests for database schema creation and data insertion
  unittest.TextTestRunner().run(
    unittest.TestLoader().loadTestsFromTestCase(TestHierarchicalStrategyDatabase)
  )