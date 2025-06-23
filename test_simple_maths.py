import unittest
from simple_maths import SimpleMath

class TestSimpleMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(SimpleMath.addition(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
