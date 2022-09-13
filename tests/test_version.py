import unittest


class TestIn(unittest.TestCase):
    def test_in_string(self):
        self.assertNotIn('3.11', open("/tests/output").read())
        
        
if __name__ == '__main__':
    unittest.main()
       
