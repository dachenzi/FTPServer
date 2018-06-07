import unittest
from lib import MixInClass

class TestBale(unittest.TestCase):

    def setUp(self):  # 测试前执行
        print('Start')

    def tearDown(self):  # 测试后执行
        print('End')

    def test_bytes(self):  # 所有以test_开头的方法会被执行
        d = MixInClass.BaleMixIn()
        self.assertTrue(isinstance(d._struct('123'),bytes))


if __name__ == '__main__':
    unittest.main()   # 运行