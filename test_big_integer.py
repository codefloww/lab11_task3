"""Unittest module for big_integer module."""
import unittest
from big_integer import BigInteger


class TestBigInteger(unittest.TestCase):
    def setUp(self) -> None:
        self.empty = BigInteger()
        self.zero = BigInteger("0")
        self.one = BigInteger("1")
        self.ten = BigInteger("10")
        self.minus_one = BigInteger("-1")
        self.minus_two = BigInteger("-2")
        self.minus_ten = BigInteger("-10")
        self.large = BigInteger("123456789012345678901234567890")
        self.integ = BigInteger(10)
        self.zeros = BigInteger("000001")
        self.binary = BigInteger("10101")
        self.binary.is_binary = True
        self.an_binary = BigInteger("1110")
        self.an_binary.is_binary = True

    def test_init(self):
        self.assertEqual(str(self.empty), "")
        self.assertEqual(str(self.zero), "0")
        self.assertEqual(str(self.one), "1")
        self.assertEqual(str(self.ten), "10")
        self.assertEqual(str(self.minus_one), "-1")
        self.assertEqual(str(self.large), "123456789012345678901234567890")
        self.assertEqual(str(self.integ), "10")
        self.assertTrue(self.zero.positive)
        self.assertFalse(self.minus_one.positive)

    def test_add_digit(self):
        self.empty._add_digit(0)
        self.assertEqual(str(self.empty), "0")
        self.empty._add_digit(1)
        self.assertEqual(str(self.empty), "01")
        self.empty._add_digit(2, False)
        self.assertEqual(str(self.empty), "201")
        self.empty._add_digit(3, True)
        self.assertEqual(str(self.empty), "2013")
        self.minus_two._add_digit(1)
        self.assertEqual(str(self.minus_two), "-21")
        self.minus_two._add_digit(2, False)
        self.assertEqual(str(self.minus_two), "-221")

    def test_remove_digit(self):
        self.large._remove_digit()
        self.assertEqual(str(self.large), "12345678901234567890123456789")
        self.large._remove_digit()
        self.assertEqual(str(self.large), "1234567890123456789012345678")
        self.minus_ten._remove_digit()
        self.assertEqual(str(self.minus_ten), "-1")

    def test_digits(self):
        self.assertEqual(self.empty._digits(), [])
        self.assertEqual(self.zero._digits(), [0])
        self.assertEqual(self.one._digits(), [1])
        self.assertEqual(self.ten._digits(), [1, 0])
        self.assertEqual(self.minus_one._digits(), [1])
        self.assertEqual(self.minus_ten._digits(), [1, 0])

    def test_dump_integer(self):
        self.zeros.dump_integer()
        self.assertEqual(str(self.zeros), "1")

    def test_abs(self):
        self.assertEqual(str(self.zero.abs()), "0")
        self.assertEqual(str(self.one.abs()), "1")
        self.assertEqual(str(self.ten.abs()), "10")
        self.assertEqual(str(self.large.abs()), "123456789012345678901234567890")
        self.assertEqual(str(self.minus_one.abs()), "1")
        self.assertEqual(str(self.minus_two.abs()), "2")
        self.assertEqual(str(self.minus_ten.abs()), "10")

    def test_copy(self):
        self.assertEqual(str(self.zero.copy()), "0")
        self.assertNotEqual(self.zero, self.zero.copy())

    def test_add(self):
        self.assertEqual(str(self.zero + self.zero), "0")
        self.assertEqual(str(self.zero + self.one), "1")
        self.assertEqual(str(self.one + self.zero), "1")
        self.assertEqual(str(self.one + self.one), "2")
        self.assertEqual(str(self.one + self.ten), "11")
        self.assertEqual(str(self.ten + self.one), "11")
        self.assertEqual(str(self.ten + self.ten), "20")
        self.assertEqual(str(self.minus_one + self.minus_one), "-2")
        self.assertEqual(str(self.minus_one + self.one), "0")
        self.assertEqual(str(self.minus_one + self.ten), "9")
        self.assertEqual(str(self.integ + 10), "20")

    def test_sub(self):
        self.assertEqual(str(self.zero - self.zero), "0")
        self.assertEqual(str(self.zero - self.one), "-1")
        self.assertEqual(str(self.one - self.zero), "1")
        self.assertEqual(str(self.one - self.one), "0")
        self.assertEqual(str(self.one - self.ten), "-9")
        self.assertEqual(str(self.ten - self.one), "9")
        self.assertEqual(str(self.ten - self.ten), "0")
        self.assertEqual(str(self.minus_one - self.minus_one), "0")
        self.assertEqual(str(self.minus_one - self.one), "-2")
        self.assertEqual(str(self.minus_one - self.ten), "-11")
        self.assertEqual(str(self.integ - 10), "0")

    def test_mult(self):
        self.assertEqual(str(self.zero * self.zero), "0")
        self.assertEqual(str(self.zero * self.one), "0")
        self.assertEqual(str(self.one * self.zero), "0")
        self.assertEqual(str(self.one * self.one), "1")
        self.assertEqual(str(self.one * self.ten), "10")
        self.assertEqual(str(self.ten * self.one), "10")
        self.assertEqual(str(self.ten * self.ten), "100")
        self.assertEqual(str(self.minus_one * self.minus_one), "1")
        self.assertEqual(str(self.minus_one * self.one), "-1")
        self.assertEqual(str(self.minus_one * self.ten), "-10")
        self.assertEqual(str(self.integ * 10), "100")

    def test_floordiv(self):
        self.assertRaises(ZeroDivisionError, lambda: self.zero // self.zero)
        self.assertRaises(ZeroDivisionError, lambda: self.one // self.zero)
        self.assertEqual(str(self.zero // self.one), "0")
        self.assertEqual(str(self.one // self.one), "1")
        self.assertEqual(str(self.one // self.ten), "0")
        self.assertEqual(str(self.ten // self.one), "10")
        self.assertEqual(str(self.ten // self.ten), "1")
        self.assertEqual(str(self.minus_one // self.minus_one), "1")
        self.assertEqual(str(self.minus_one // self.one), "1")
        self.assertEqual(str(self.minus_one // self.ten), "0")
        self.assertEqual(str(self.integ // 10), "1")

    def test_mod(self):
        self.assertRaises(ZeroDivisionError, lambda: self.zero % self.zero)
        self.assertRaises(ZeroDivisionError, lambda: self.one % self.zero)
        self.assertEqual(str(self.zero % self.one), "0")
        self.assertEqual(str(self.one % self.one), "0")
        self.assertEqual(str(self.one % self.ten), "1")
        self.assertEqual(str(self.ten % self.one), "0")
        self.assertEqual(str(self.ten % self.ten), "0")
        self.assertEqual(str(self.minus_one % self.minus_one), "0")
        self.assertEqual(str(self.minus_one % self.one), "0")
        self.assertEqual(str(self.minus_one % self.ten), "9")
        self.assertEqual(str(self.integ % 10), "0")

    def test_abs_lt(self):
        self.assertTrue(self.zero._abs_lt(self.one))
        self.assertTrue(self.one._abs_lt(self.ten))
        self.assertTrue(self.ten._abs_lt(self.large))
        self.assertFalse(self.large._abs_lt(self.minus_one))
        self.assertFalse(self.minus_one._abs_lt(self.zero))

    def test_lt(self):
        self.assertTrue(self.zero < self.one)
        self.assertTrue(self.one < self.ten)
        self.assertTrue(self.ten < self.large)
        self.assertFalse(self.large < self.minus_one)
        self.assertTrue(self.minus_one < self.zero)
        self.assertTrue(self.minus_one < self.one)
        self.assertTrue(self.minus_one < self.ten)
        self.assertTrue(self.minus_one < self.large)

    def test_to_bin(self):
        self.assertEqual(str(self.zero.to_bin()), "0")
        self.assertEqual(str(self.one.to_bin()), "1")
        self.assertEqual(str(self.ten.to_bin()), "1010")
        self.assertEqual(str(self.binary), "10101")

    def test_from_bin(self):
        self.assertEqual(str(self.zero.from_bin()), "0")
        self.assertEqual(str(self.one.from_bin()), "1")
        self.assertEqual(str(self.binary.from_bin()), "21")
        self.assertEqual(str(self.ten.from_bin()), "10")

    def test_logic_or(self):
        self.assertEqual(str(self.zero | self.zero), "0")
        self.assertEqual(str(self.zero | self.one), "1")
        self.assertEqual(str(self.one | self.zero), "1")
        self.assertEqual(str(self.one | self.one), "1")
        self.assertEqual(str(self.one | self.ten), "1011")
        self.assertEqual(str(self.ten | self.one), "1011")
        self.assertEqual(str(self.ten | self.ten), "1010")
        self.assertEqual(str(self.binary | self.binary), "10101")
        self.assertEqual(str(self.binary | self.an_binary), "11111")

    def test_lshift(self):
        self.assertEqual(str(self.binary << 2), "1010100")
        self.assertEqual(str(self.binary << 0), "10101")
        self.assertEqual(str(self.binary << -1), "1010")
        self.assertEqual(str(self.binary << -2), "101")
        self.assertEqual(str(self.an_binary << -3), "1")

    def test_rshift(self):
        self.assertEqual(str(self.binary >> 2), "101")
        self.assertEqual(str(self.binary >> 0), "10101")
        self.assertEqual(str(self.binary >> -1), "101010")


if __name__ == "__main__":
    unittest.main()
