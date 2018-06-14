# UffiziTestSuite - Testing scripts for Uffizi
# Copyright (C) 2018 Jason Ellis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Test script for the ServerCompare.py script in the utilities folder.
"""
   
from unittest import mock
import os, sys, filecmp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uffizi")))

from utilities.ServerCompare import ServerCompare

SOURCE_FILE = "source.txt"
TARGET_FILE = "target.txt"

OUTPUT_ADD = "target_add.txt"
OUTPUT_DEL = "target_del.txt"
OUTPUT_UPD = "target_upd.txt"

OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uffizi", "utilities", "output"))

DATA_PATH = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 
            "data", 
            "TestServerCompare")
            
PATH_SOURCE_FILES = os.path.join(DATA_PATH, "source")
PATH_TARGET_FILES = os.path.join(DATA_PATH, "target")

GOLD_PATH = os.path.join(DATA_PATH, "gold")
GOLD_SOURCE_FILE = os.path.join(GOLD_PATH, "source.txt")
GOLD_TARGET_FILE = os.path.join(GOLD_PATH, "target.txt")
GOLD_OUTPUT_ADD = os.path.join(GOLD_PATH, OUTPUT_ADD)
GOLD_OUTPUT_DEL = os.path.join(GOLD_PATH, OUTPUT_DEL)
GOLD_OUTPUT_UPD = os.path.join(GOLD_PATH, OUTPUT_UPD)

class TestServerCompare(unittest.TestCase):
        
    def setUp(self):
        self.server_comp = ServerCompare()
        self.source = {'/1.txt': 0, '/2.txt': 0, '/4.txt': 9}
        self.target = {'/2.txt': 0, '/3.txt': 0, '/4.txt': 0}
        

    @mock.patch('builtins.input', 
                side_effect=[PATH_SOURCE_FILES, 
                             PATH_SOURCE_FILES, 
                             ""])
    def test_load_path_source(self, mock):
        self.server_comp.load_path_source()
        self.assertEqual(self.server_comp._ServerCompare__source, 
                         self.source)
        
        
    @mock.patch('builtins.input', 
                side_effect=[PATH_TARGET_FILES, 
                             PATH_TARGET_FILES, 
                             ""])
    def test_load_path_target(self, mock):
        self.server_comp.load_path_target()
        self.assertEqual(self.server_comp._ServerCompare__target, 
                         self.target)
                            
                            
    @mock.patch('builtins.input', 
                side_effect=[GOLD_SOURCE_FILE])
    def test_load_file_source(self, mock):
        self.server_comp.load_file_source()
        self.assertEqual(self.server_comp._ServerCompare__source, 
                         self.source)
        
        
    @mock.patch('builtins.input', 
                side_effect=[GOLD_TARGET_FILE])
    def test_load_file_target(self, mock):
        self.server_comp.load_file_target()
        self.assertEqual(self.server_comp._ServerCompare__target, 
                         self.target)
        
    @mock.patch('builtins.input', 
                side_effect=[GOLD_SOURCE_FILE])
    def test_source_populated(self, mock):
        self.server_comp.load_file_source()
        self.assertTrue(self.server_comp.source_populated)
        
    @mock.patch('builtins.input', 
                side_effect=[GOLD_TARGET_FILE])
    def test_target_populated(self, mock):
        self.server_comp.load_file_target()
        self.assertTrue(self.server_comp.target_populated)

        
    @mock.patch('builtins.input', 
                side_effect=[PATH_SOURCE_FILES, 
                             PATH_SOURCE_FILES, 
                             "",
                             SOURCE_FILE])
    def test_write_file_source(self, mock):
        self.server_comp.load_path_source()
        self.server_comp.write_file_source()
        
        output_file = os.path.join(OUTPUT_PATH, SOURCE_FILE)
        self.assertTrue(filecmp.cmp(output_file, GOLD_SOURCE_FILE))
        
        
    @mock.patch('builtins.input', 
                side_effect=[PATH_TARGET_FILES, 
                             PATH_TARGET_FILES, 
                             "",
                             TARGET_FILE])
    def test_write_file_target(self, mock):
        self.server_comp.load_path_target()
        self.server_comp.write_file_target()
        
        output_file = os.path.join(OUTPUT_PATH, TARGET_FILE)
        self.assertTrue(filecmp.cmp(output_file, GOLD_TARGET_FILE))
        
        
    @mock.patch('builtins.input', 
                side_effect=[GOLD_SOURCE_FILE])
    def test_clear_source(self, mock):
        self.server_comp.load_file_source()
        self.server_comp.clear_source()
        self.assertFalse(self.server_comp.source_populated)
        
        
    @mock.patch('builtins.input', 
                side_effect=[GOLD_TARGET_FILE])
    def test_clear_target(self, mock):
        self.server_comp.load_file_target()
        self.server_comp.clear_target()
        self.assertFalse(self.server_comp.target_populated)
        
    
    @mock.patch('builtins.input', 
                side_effect=[GOLD_SOURCE_FILE,
                             GOLD_TARGET_FILE])
    def test_compare_add(self, mock):
        self.server_comp.load_file_source()
        self.server_comp.load_file_target()
        self.server_comp.compare()
        
        output = os.path.join(OUTPUT_PATH, OUTPUT_ADD)
        
        self.assertTrue(filecmp.cmp(output, GOLD_OUTPUT_ADD))


    @mock.patch('builtins.input', 
                side_effect=[GOLD_SOURCE_FILE,
                             GOLD_TARGET_FILE])
    def test_compare_del(self, mock):
        self.server_comp.load_file_source()
        self.server_comp.load_file_target()
        self.server_comp.compare()
        
        output = os.path.join(OUTPUT_PATH, OUTPUT_DEL)
        
        self.assertTrue(filecmp.cmp(output, GOLD_OUTPUT_DEL))


    @mock.patch('builtins.input', 
                side_effect=[GOLD_SOURCE_FILE,
                             GOLD_TARGET_FILE])
    def test_compare_update(self, mock):
        self.server_comp.load_file_source()
        self.server_comp.load_file_target()
        self.server_comp.compare()
        
        output = os.path.join(OUTPUT_PATH, OUTPUT_UPD)
        
        self.assertTrue(filecmp.cmp(output, GOLD_OUTPUT_UPD))
        
    @classmethod
    def tearDownClass(cls):
        source_file = os.path.join(OUTPUT_PATH, SOURCE_FILE)
        target_file = os.path.join(OUTPUT_PATH, TARGET_FILE)
        
        if os.path.isfile(source_file):
            os.remove(source_file)
            
        if os.path.isfile(target_file):
            os.remove(target_file)


if __name__ == '__main__':
    
    unittest.main()

    