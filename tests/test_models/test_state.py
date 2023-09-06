#!/usr/bin/python3
"""test for state"""
import os
import unittest

import pep8

from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):
    """this will test the State class"""
    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.state = State()
        cls.state.name = "CA"

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.state

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_review(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        pep = style.check_files(['models/state.py'])
        self.assertEqual(pep.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_state(self):
        """checking for docstrings"""
        self.assertIsNotNone(State.__doc__)

    def test_attributes_state(self):
        """chekcing if State have attributes"""
        self.assertTrue('id' in self.state.__dict__)
        self.assertTrue('created_at' in self.state.__dict__)
        self.assertTrue('updated_at' in self.state.__dict__)
        self.assertTrue('name' in self.state.__dict__)

    def test_is_subclass_state(self):
        """test if State is subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)

    def test_attribute_types_state(self):
        """test attribute type for State"""
        self.assertEqual(type(self.state.name), str)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "This test only work in Filestorage")
    def test_save_state(self):
        """test if the save works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_state(self):
        """test if dictionary works"""
        self.assertEqual('to_dict' in dir(self.state), True)


if __name__ == "__main__":
    unittest.main()
