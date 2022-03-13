import unittest
import taginfo

class Tests(unittest.TestCase):
    def test_basic_math(self):
        self.assertEqual(2-2, 0)

    def test_example_code(self):
        self.assertEqual(2-2, 0)
        print(taginfo.lorem_ipsum.text())

if __name__ == '__main__':
    unittest.main()
