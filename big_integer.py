"""BigInteger implementation for representing and manipulating large integers."""


VARIANT = 70
# 70 Кривень Павло ['<=', '<'] ['*', '//'] ['|', '<<']
class BigInteger:
    """BigInteger implementation for representing and manipulating large integers."""

    def __init__(self, init_value: object = None) -> None:
        self._head = None
        self._tail = None
        self.positive = True
        self.is_binary = False
        init_value = init_value or None

        if isinstance(init_value, int):
            init_value = str(init_value)

        if init_value is not None:
            if '-' in init_value:
                self.positive = False
                init_value = init_value.lstrip("-")
            for digit in init_value:
                self._add_digit(int(digit))

    def _add_digit(self, digit: int, right: bool = True) -> None:
        """Add digit in the head of the list

        Args:
            digit (int): Digit to add
            right (bool, optional): Place to inplace digit. Defaults to True.
        """
        if right:
            self._head, self._head.next = DecimalDigitNode(digit), self._head
            if self._head.next is not None:
                self._head.next.previous = self._head
            else:
                self._tail = self._head
        else:
            self._tail, self._tail.previous = DecimalDigitNode(digit), self._tail
            if self._tail.previous is not None:
                self._tail.previous.next = self._tail
            else:
                self._head = self._tail

    def _remove_digit(self) -> None:
        """Remove digit from the head of the list"""
        if self._head is not None:
            self._head = self._head.next
            if self._head is not None:
                self._head.previous = None
            else:
                self._tail = None

    def _digits(self) -> list:
        """Return list of digits

        Returns:
            list: list of digits from tail to head(in default left to right order)
        """
        digits = []
        current = self._tail
        while current is not None:
            digits.append(current.digit)
            current = current.previous
        return digits

    def __str__(self) -> str:
        represent = ''
        current = self._tail
        while current is not None:
            represent +=str(current)
            current = current.previous
        return represent if self.positive else '-'+represent

    def to_string(self):
        """Convert big integer to string

        Returns:
            str: string representation of big integer
        """
        return str(self)

    def dump_integer(self) -> None:
        """Dump integer to the head of the list"""
        while self._tail.digit == 0 and self._tail.previous is not None:
            self._tail = self._tail.previous

    def __add__(self, __o: object) -> object:
        """Add two big integers

        Args:
            __o (BigInteger&quot; | int | str): another integer

        Returns:
            BigInteger: sum of two big integers
        """
        integer_sum = BigInteger()
        sum_carry = 0
        if isinstance(__o, int) or (isinstance(__o, str) and __o.isdigit()):
            __o = BigInteger(str(__o))
        current, another_current = (
            (self._head, __o._head) if __o._abs_lt(self) else (__o._head, self._head)
        )
        while current is not None:
            if another_current is not None:
                if (self.positive and __o.positive) or (
                    not self.positive and not __o.positive
                ):
                    digit_sum, sum_carry = (
                        current.digit + another_current.digit + sum_carry
                    ) % 10, (current.digit + another_current.digit + sum_carry) // 10
                else:
                    digit_sum = (current.digit - another_current.digit + sum_carry) % 10
                    sum_carry = (
                        -1
                        if current.digit - another_current.digit + sum_carry < 0
                        else 0
                    )
                integer_sum._add_digit(digit_sum, False)
                current = current.next
                another_current = another_current.next
            else:
                if (self.positive and __o.positive) or (
                    not self.positive and not __o.positive
                ):
                    integer_sum._add_digit(current.digit + sum_carry, False)
                    sum_carry = 0
                else:
                    integer_sum._add_digit(current.digit + sum_carry, False)
                    sum_carry = -1 if current.digit + sum_carry < 0 else 0
                current = current.next

        integer_sum._add_digit(sum_carry, False)
        integer_sum.dump_integer()
        if (
            (self.positive and __o.positive)
            or (self._abs_lt(__o) and __o.positive)
            or (__o._abs_lt(self) and self.positive)
        ):
            integer_sum.positive = True
        else:
            integer_sum.positive = False
        if integer_sum._digits() == [0]:
            integer_sum.positive = True
        return integer_sum

    def __sub__(self, __o: object) -> object:
        """Subtract two big integers

        Args:
            __o (BigInteger&quot; | int | str): Another integer

        Returns:
            BigInteger: Difference of two big integers
        """
        return self + (__o * -1)

    def __mul__(self, __o: object) -> object:
        """Multiply two big integers

        Args:
            __o (BigInteger&quot; | str | int): Another integer

        Returns:
            BigInteger: Product of two big integers
        """
        if str(self) == "0" or str(__o) == "0":
            return BigInteger("0")
        else:
            product = BigInteger("0")
            if isinstance(__o, int) or (isinstance(__o, str) and __o.isdigit()):
                __o = BigInteger(str(__o))
            times = (
                int(str(self).lstrip("-"))
                if self._abs_lt(__o)
                else int(str(__o).lstrip("-"))
            )
            increment = self if not self._abs_lt(__o) else __o
            for _ in range(times):
                product = product + increment

        if (self.positive and not __o.positive) or (not self.positive and __o.positive):
            product.positive = False
        else:
            product.positive = True
        return product

    def __floordiv__(self, __o: object) -> object:
        """Integer division of two big integers

        Args:
            __o (BigInteger&quot; | int | str): Module

        Raises:
            ZeroDivisionError: Division by zero

        Returns:
            BigInteger: Integer division of two big integers
        """
        if isinstance(__o, int) or (isinstance(__o, str) and __o.isdigit()):
            __o = BigInteger(str(__o))
        first = self.copy()
        second = __o.copy()
        if str(second) == "0":
            raise ZeroDivisionError
        count = 0
        if (first.positive and second.positive) or (
            not first.positive and not second.positive
        ):
            while not first._abs_lt(second):
                first = first - second
                count += 1
        else:
            while not first._abs_lt(second) or first.positive != second.positive:
                first = first + second
                count -= 1
        result = BigInteger(str(count))
        return result

    def __mod__(self, __o: object) -> object:
        """Modulo of two big integers

        Args:
            __o (BigInteger&quot; | str | int): Another integer

        Raises:
            ZeroDivisionError: Division by zero

        Returns:
            BigInteger: Remainder of two big integers
        """
        if isinstance(__o, int) or (isinstance(__o, str) and __o.isdigit()):
            __o = BigInteger(str(__o))
        __o.dump_integer()
        if str(__o) == "0":
            raise ZeroDivisionError
        result = (
            self - ((self // __o) * __o).abs()
            if self.positive
            else self + ((self // __o) * __o).abs()
        )
        if result < 0:
            result = result + __o.abs()
        return result

    def __or__(self, __o: object) -> object:
        """Bitwise OR of two big integers

        Args:
            __o (BigInteger): Another big integer

        Returns:
            BigInteger: Bitwise OR of two big integers
        """
        first = self.to_bin() if not self.is_binary else self.abs()
        second = __o.to_bin() if not __o.is_binary else __o.abs()
        first_current = first._head
        second_current = second._head
        or_bin_integer = BigInteger()
        while first_current is not None or second_current is not None:
            if first_current is None:
                or_bin_integer._add_digit(second_current.digit, False)
                second_current = second_current.next
            elif second_current is None:
                or_bin_integer._add_digit(first_current.digit, False)
                first_current = first_current.next
            else:
                or_bin_integer._add_digit(
                    first_current.digit | second_current.digit, False
                )
                first_current = first_current.next
                second_current = second_current.next
        or_bin_integer.is_binary = True
        return or_bin_integer

    def __lshift__(self, shift: object) -> object:
        """Left bit shift of big integer

        Args:
            shift (int|BigInteger): Shift amount

        Returns:
            BigInteger: Bitwise left shift of big integer
        """
        converted = self.copy()
        if not self.is_binary:
            converted = self.to_bin()
        if isinstance(shift, BigInteger):
            shift = int(str(shift))
        if shift < 0:
            return self >> -shift
        for _ in range(shift):
            converted._add_digit(0)
        converted.dump_integer()
        return converted

    def __rshift__(self, shift: int) -> object:
        """Right bit shift of big integer

        Args:
            shift (int): Shift amount

        Returns:
            BigInteger: Right bit shift of big integer
        """
        converted = self.copy()
        if not self.is_binary:
            converted = self.to_bin()
        if shift < 0:
            return self << -shift
        for _ in range(shift):
            converted._remove_digit()
        converted.dump_integer()
        return converted

    def __lt__(self, __o: object) -> bool:
        """Less than comparison of two big integers

        Args:
            __o (BigInteger&quot; | str | int): Another integer

        Returns:
            bool: Less than comparison of two big integers
        """
        if isinstance(__o, int) or (isinstance(__o, str) and __o.isdigit()):
            __o = BigInteger(str(__o))

        if not self.positive and __o.positive:
            return True
        elif self.positive and not __o.positive:
            return False
        elif self._abs_lt(__o) and self.positive:
            return True
        else:
            return False

    def copy(self) -> object:
        """Copy of big integer

        Returns:
            BigInteger: Copy of big integer
        """
        return BigInteger(str(self))

    def abs(self) -> object:
        """Absolute value of big integer

        Returns:
            BigInteger: Big integer with absolute value
        """
        if self.positive:
            return BigInteger(str(self))
        else:
            return BigInteger(str(self).lstrip("-"))

    def _abs_lt(self, __o: object) -> bool:
        """Less than comparison of absolute values of two big integers

        Args:
            __o (BigInteger): Another big integer

        Returns:
            bool: Less than comparison of absolute values of two big integers
        """
        if len(self._digits()) < len(__o._digits()):
            return True
        elif len(self._digits()) > len(__o._digits()):
            return False
        else:
            current = self._tail
            other_current = __o._tail
            while current is not None:
                if current.digit < other_current.digit:
                    return True
                elif current.digit > other_current.digit:
                    return False
                else:
                    current = current.previous
                    other_current = other_current.previous
            return False

    def __le__(self, __o: object) -> bool:
        """Less than or equal comparison of two big integers

        Args:
            __o (_type_): Another big integer

        Returns:
            bool: Comparison of two big integers
        """
        if self < __o or self._digits() == __o._digits():
            return True
        return False

    def to_bin(self) -> object:
        """Convert big integer to binary big integer

        Returns:
            BigInteger: Binary big integer
        """
        binary = ""
        if self.is_binary:
            return self

        current = self.copy()
        current.dump_integer()
        if str(current) == "0":
            bin_integer = BigInteger("0")
            bin_integer.is_binary = True
            return bin_integer

        while current.abs() > BigInteger("0"):
            binary += str(current % 2)
            current = current // 2
        bin_integer = BigInteger(binary[::-1])
        bin_integer.is_binary = True
        return bin_integer

    def from_bin(self) -> object:
        """Convert binary big integer to big integer

        Returns:
            BigInteger: Big integer from binary big integer
        """
        if not self.is_binary:
            return self
        dec_integer = BigInteger("0")
        current = self._head
        count = 0
        while current is not None:
            dec_integer = dec_integer + current.digit * (2**count)
            count += 1
            current = current.next
        return dec_integer


class DecimalDigitNode:
    """Node of decimal digit list"""

    def __init__(self, digit: int) -> None:
        self.digit = digit
        self.next = None
        self.previous = None

    def __str__(self) -> str:
        return str(self.digit)


if __name__ == "__main__":
    a = BigInteger("0")
    print(a)
