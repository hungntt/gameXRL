"""
_ Unittest module for: 
_ Number of test function:
_ Number of testcase:
_ Date:
"""
import unittest


class TestModule1(unittest.TestCase):
    """
    Run unittest for function in module_1.
    """
    def setUp(self):
        """
        This function will be execute before any testing.
        """

        pass

    def tearDown(self):
        """
        This function will be execute at the end of testing.
        """

        pass

    def test_function_name(self):
        actual = 1
        expected = 1
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
