"""
this package contain:
| * Functions for most operation and comparison and collision detection.
| * Math functions.
| * Classes of All Vectors, Matrix and Colors having all of those functions
| as methods.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#### Enable Feature Python
from __future__ import division

__author__ = "azzayou (azzayou9@gmail.com)"  # it's ME :D
__copyright__ = "Copyright (c) 2026 azzayou"
__licence__ = "MIT"
__version__ = "0.1.0"

#### Import Python Library
import copy  # for: copy, deepcopy
import re  # for: match

#### Import Files
try:  # in case it imported directly
    from pyvmc.pyvmc_functions import *  # here also imported Sequence, Iterable
except ModuleNotFoundError:  # in case it installed
    from .pyvmc_functions import *  # here also imported Sequence, Iterable

# no functions.
# classes.

MATRIX_START_LETTER_ATTRIB = "a"
MATRIX_PATTERN_ATTRIB = r"%s\d+_\d+" % MATRIX_START_LETTER_ATTRIB

## ``EM`` stand for ``Error Message``
EM_UNSUPPORTED_TYPE_OPERATION = "Unsupported %s operation `%s` with `%s`"
EM_NO_ATTRIBUTE = "`%s` object has no attribute `%s`"
EM_WRONG_MATRIX_PATTERN_ATTRIB = (
        ("Matrix pattern should be like `%s`," % MATRIX_PATTERN_ATTRIB)
        + " got: `%s`")


class FixList(Sequence):
    """FixList is Custom Sequence class/type.
     for handling Fixed length of Sequence.

    Example:

    >>> test = FixList(map(lambda i: i**2, range(10)))  # accept any iterable :D
    >>> test
    [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    >>> lst = FixList([1,2,3,4])
    >>> lst
    [1, 2, 3, 4]
    >>> lst[1]
    2
    >>> lst[2:]
    [3, 4]
    >>> lst[3] = "I am CHANGED"
    >>> lst
    [1, 2, 3, 'I am CHANGED']
    >>> try:
    ...     lst[4] = 1
    ... except IndexError as error:
    ...     print(error)
    list assignment index out of range
    >>> lst.index("I am CHANGED")
    3
    >>> lst.change_data(("a", "b", "c"))  # change multiple at once
    >>> lst
    ['a', 'b', 'c', 'I am CHANGED']
    >>> lst.change_data((2, 3, 4), offset_index=1)  # change multiple at once
    >>> lst
    ['a', 2, 3, 4]
    >>> try:
    ...     lst.change_data(("too", "many", "new", "data", ":D"))
    ... except IndexError as error:
    ...     print("index out of range :C.")
    index out of range :C.
    >>> try:
    ...     del lst[2]
    ... except NotImplementedError as error:
    ...     print(error)
    Can't Delete item from FixList Or any subclasses like: `FixList`.
    """

    def __new__(cls, *args, **kwargs):
        return Sequence.__new__(cls)

    def __init__(self, iterable, *args, **kwargs):
        """Create Instance of FixList."""
        self._data = list(iterable)
        self.__first_length = len(self._data)
        """length of data in first initialization of class/type ``__init__``"""

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, new_value):
        self._data[index] = new_value

    def __delitem__(self, key):
        """WARNING: NOT IMPLEMENTED."""
        message = "Can't Delete item from FixList Or any subclasses like: `%s`."
        raise NotImplementedError(message % self.__class__.__name__)

    def __iter__(self):
        return iter(self._data)

    def __reversed__(self):
        return reversed(self._data)

    def __copy__(self):
        return self.__class__(copy.copy(self._data))

    def __deepcopy__(self, memo=None):
        return self.__class__(copy.deepcopy(self._data, memo=memo))

    ########## Methods
    def strict_length(self, expect_length):
        """Raise ValueError if length of data don't match with expect length."""
        if len(self) != expect_length:
            message = EM_WRONG_LENGTH % (expect_length, len(self), str(self))
            raise ValueError(message)

    def change_data(self, new_data, offset_index=0, strict=False):
        """change values of data from an iterable.

        Note: ``offset_index`` (by default is 0) it's offset index for changing
         data to new data.

        Note: ``strict`` (by default is False)
        | * if it's False. if the length of ``new_data`` Must be Less Than Or
        | Equal To length of data. Or it will raise ValueError.
        | * if it's True. if the length of ``new_data`` Must be Equal To length
        | of data. Or it will raise ValueError.
        """
        new_length = 0
        for index, new_value in enumerate(new_data):
            new_length += 1
            self._data[index + offset_index] = new_value
        ##### check
        if strict and new_length != self.__first_length:
            message = EM_WRONG_LENGTH % (self.__first_length, new_length,
                                         str(new_data))
            raise ValueError(message)
        ##### end check

    def copy(self):
        """Return copy of data as same class of self."""
        return self.__copy__()

    def copy_tuple(self):
        """Return copy of data as a tuple."""
        return tuple(self.copy())

    def copy_list(self):
        """Return copy of data as a list."""
        return list(self.copy())

    def deepcopy(self, memo=None):
        """Return deep copy of data as same class of self.

        Warning: this function will COST Memory Be CAREFUL.
        """
        return self.__deepcopy__(memo=memo)

    def deepcopy_tuple(self, memo=None):
        """Return deep copy of data as a tuple.

        Warning: this function will COST Memory Be CAREFUL.
        """
        return tuple(self.deepcopy(memo=memo))

    def deepcopy_list(self, memo=None):
        """Return deep copy of data as a list.

        Warning: this function will COST Memory Be CAREFUL.
        """
        return list(self.deepcopy(memo=memo))


class Color(FixList):
    """Color RGBA (Red, Green, Blue, Alpha (opacity)).
     all color value of RGBA Should use any integer with in range [0, 255].

    Examples:

    >>> blank = Color()  # by default, it's Blank
    >>> blank
    [Red=0, Green=0, Blue=0, Alpha=0]
    >>> color1 = Color((200, 155, 1, 255))
    >>> color1
    [Red=200, Green=155, Blue=1, Alpha=255]
    >>> print(color1)
    [r=200, g=155, b=1, a=255]
    >>> print(color1.r, color1.g, color1.b, color1.a)
    200 155 1 255
    >>> color1.a -= 50  # you can modify any color value.
    >>> color1.a
    205
    >>> color1.a += 100000  # WARNING: color value always between [0, 255]
    >>> color1.a
    255
    >>> color1.a = 1/2  # WARNING: color value always be integer
    >>> color1.a  # in case new value is float it will cut off the float number.
    0
    >>> print(color1.to_hex_str)
    #c89b0100
    >>> print(color1.to_hex_tuple)
    ('c8', '9b', '01', '00')
    >>> color1.color_normalize
    (0.7843137254901961, 0.6078431372549019, 0.00392156862745098, 0.0)
    >>> color1.rgb
    (200, 155, 1)
    >>> color1.rgb_normalize
    (0.7843137254901961, 0.6078431372549019, 0.00392156862745098)
    >>> try:
    ...     Color((300, 10, 2, 255))
    ... except ValueError as error:
    ...     print(error)
    Expect color value be in range [0, 255], got: `[r=300, g=10, b=2, a=255]`
    """
    COLOR_SPECIAL_STR = "[r=%s, g=%s, b=%s, a=%s]"
    COLOR_SPECIAL_REPR = "[Red=%s, Green=%s, Blue=%s, Alpha=%s]"

    def __init__(self, red_green_blue_alpha=None, *args, **kwargs):
        """Create Instance of Color.

        Warning: red_green_blue_alpha Must be tuple/Sequence of 4 integer
         between [0, 255]. Or it will raise ValueError.
        """
        specific_length = 4
        if red_green_blue_alpha:
            super(Color, self).__init__(red_green_blue_alpha)
            ##### check
            self.strict_length(specific_length)
            if any(map(lambda x: not (0 <= x <= 255), red_green_blue_alpha)):
                message = EM_NOT_EXPECTED % (
                    "color value be integer between [0, 255]", str(self))
                raise ValueError(message)
            ##### end check
        else:
            super(Color, self).__init__(vector_zero(specific_length))

    def __str__(self):
        return self.COLOR_SPECIAL_STR % tuple(self)

    def __repr__(self):
        return self.COLOR_SPECIAL_REPR % tuple(self)

    def __format__(self, format_spec):
        return self.COLOR_SPECIAL_STR % tuple(
            map(lambda c: format(c, format_spec), self))

    ########## Properties
    @property
    def r(self):
        """Color Red."""
        return self[0]

    @r.setter
    def r(self, value):
        self[0] = int(max(0, min(value, 255)))

    @property
    def r_hex(self):
        """Return Color Red value as string of hex code.

        Note: it will NOT include ``0x`` (Read Only).
        """
        return "%02.x" % self.r

    @property
    def r_bytes(self):
        """Return Color Red value as bytes (Read Only)."""
        return b"%02x" % self.r

    @property
    def g(self):
        """Color Green"""
        return self[1]

    @g.setter
    def g(self, value):
        self[1] = int(max(0, min(value, 255)))

    @property
    def g_hex(self):
        """Return Color Green value as string of hex code.

        Note: it will NOT include ``0x`` (Read Only).
        """
        return "%02.x" % self.g

    @property
    def g_bytes(self):
        """Return Color Green value as bytes (Read Only)."""
        return b"%02x" % self.g

    @property
    def b(self):
        """Color Blue."""
        return self[2]

    @b.setter
    def b(self, value):
        self[2] = int(max(0, min(value, 255)))

    @property
    def b_hex(self):
        """Return Color Blue value as string of hex code.

        Note: it will NOT include ``0x`` (Read Only).
        """
        return "%02x" % self.b

    @property
    def b_bytes(self):
        """Return Color Blue value as bytes (Read Only)."""
        return b"%02x" % self.b

    @property
    def a(self):
        """Color Alpha (a.k.a. opacity)."""
        return self[3]

    @a.setter
    def a(self, value):
        self[3] = int(max(0, min(value, 255)))

    @property
    def a_hex(self):
        """Return Color Alpha (a.k.a. opacity) value as string of hex code.

        Note: it will not include ``0x`` (Read Only).
        """
        return "%02x" % self.a

    @property
    def a_bytes(self):
        """Return Color Alpha (a.k.a. opacity) value as bytes (Read Only)."""
        return b"%02x" % self.a

    @property
    def to_hex_tuple(self):
        """return color value as a tuple of strings all hex numbers."""
        return self.r_hex, self.g_hex, self.b_hex, self.a_hex

    @property
    def to_hex_str(self):
        """return color value as a single string of hex numbers (with ``#``)."""
        return "#%s%s%s%s" % self.to_hex_tuple

    @property
    def to_bytes_tuple(self):
        """return color value as a tuple of bytes."""
        return self.r_bytes, self.g_bytes, self.b_bytes, self.a_bytes

    @property
    def to_bytes(self):
        """return color value as a single bytes of all color value together."""
        return b"%s%s%s%s" % self.to_bytes_tuple

    @property
    def color_normalize(self):
        """
        return tuple of normalized color values (float number in range [0, 1]).
        """
        return self.r / 255, self.g / 255, self.b / 255, self.a / 255

    @property
    def rgb(self):
        """return tuple of color rgb values (Red, Green, Blue)."""
        return self.r, self.g, self.b

    @property
    def rgb_normalize(self):
        """Same as ``color_normalize`` But only return RGB colors."""
        return self.r / 255, self.g / 255, self.b / 255

    ########## Methods
    def from_str_or_bytes(self, str_or_bytes, base):
        """Change Color value based on hex code in a single bytes Or string and
         ``base``.

        Warning: ``bytes_or_str`` Must bytes or str of 4 hex code.
         Or it will raise ValueError.

        Examples:

        >>> color = Color((255, 255, 255, 255))
        >>> print(color)
        [r=255, g=255, b=255, a=255]
        >>> color.from_str_or_bytes("0xaaffddff", base=16)
        >>> print(color)
        [r=170, g=255, b=221, a=255]
        >>> color.from_str_or_bytes("#505040ee", base=16)
        >>> print(color)
        [r=80, g=80, b=64, a=238]
        >>> color.from_str_or_bytes("881100ff", base=16)
        >>> print(color)
        [r=136, g=17, b=0, a=255]
        >>> color.from_str_or_bytes(b"0x11223344", base=16)
        >>> print(color)
        [r=17, g=34, b=51, a=68]
        >>> color.from_str_or_bytes(b"#ff9922ff", base=16)
        >>> print(color)
        [r=255, g=153, b=34, a=255]
        >>> color.from_str_or_bytes(b"ffffffff", base=16)
        >>> print(color)
        [r=255, g=255, b=255, a=255]
        >>> # color.from_str_or_bytes(b"\x01\x01\x01\x01", base=16)
        >>> # color = [r=1, g=1, b=1, a=1]
        >>> try:
        ...     color.from_str_or_bytes("not valid", base=16)
        ... except ValueError:
        ...     print("NOT VALID format.")
        NOT VALID format.
        """
        is_str = isinstance(str_or_bytes, str)
        is_bytes = isinstance(str_or_bytes, bytes)
        valid_length = 8
        is_valid = (len(str_or_bytes) == 4 or (
                valid_length <= len(str_or_bytes) <= 10))
        ##### check
        if is_str and not is_valid:
            message = (
                    "either 8 or 9 (start with \"#\") or 10 (start with \"0x\")"
                    + (" string of number base %i" % base))
            raise ValueError(EM_NOT_EXPECTED % (message, str_or_bytes))
        if is_bytes and not is_valid:
            message = ("either 4 bytes of hex code"
                       " Or 8 or 9 (start with \"#\") or 10 (start with \"0x\")"
                       + (" bytes of number base %i" % base))
            raise ValueError(EM_NOT_EXPECTED % (message, str_or_bytes))
        ##### end check
        the_0x = "0x" if is_str else b"0x"
        hashtag = "#" if is_str else b"#"
        if str_or_bytes.startswith(hashtag):
            str_or_bytes = str_or_bytes[1:]
        if str_or_bytes.startswith(the_0x):
            str_or_bytes = str_or_bytes[2:]
        func_converter = lambda index: int_from_str_or_bytes(
            str_or_bytes[index:index + 2], base=base)
        self.change_data(map(func_converter, range(0, valid_length, 2)))

    def from_tuple(self, t_4str_or_4bytes, base):
        """change Color value based on tuple of 4 bytes/str and the ``base``.

        Warning: ``tuple_4_s_or_b`` Must tuple of 4 all string or all bytes.
         Or it will raise ValueError.

        Examples:

        >>> color = Color((200, 200, 200, 255))
        >>> print(color)
        [r=200, g=200, b=200, a=255]
        >>> color.from_tuple(("0xff", "0xff", "0xff", "0xff"), base=16)
        >>> print(color)
        [r=255, g=255, b=255, a=255]
        >>> color.from_tuple(("50", "50", "40", "ee"), base=16)
        >>> print(color)
        [r=80, g=80, b=64, a=238]
        >>> color.from_tuple((b"ee", b"f0", b"0f", b"ff"), base=16)
        >>> print(color)
        [r=238, g=240, b=15, a=255]
        >>> color.from_tuple((b"0x00", b"0x00", b"0x00", b"0x00"), base=16)
        >>> print(color)
        [r=0, g=0, b=0, a=0]
        >>> color.from_tuple((b"\x01", b"\x01", b"\x01", b"\x01"), base=16)
        >>> print(color)
        [r=1, g=1, b=1, a=1]
        >>> try:
        ...     color.from_tuple(("01", b"\x01", b"\x01", b"\x01"), base=16)
        ... except ValueError:
        ...     print("NO MIXING PLEASE.")
        NO MIXING PLEASE.
        """
        str_only = is_contain_only(t_4str_or_4bytes, str)
        bytes_only = is_contain_only(t_4str_or_4bytes, bytes)
        ##### check
        if xor(bytes_only, str_only) and not isinstance(b"", str):
            ## in Python 2 ``bytes`` are also ``str``. So Error will Not raise
            message = "Expect tuple of 4 string Or 4 bytes, got: %s"
            raise ValueError(message % str(t_4str_or_4bytes))
        ##### end check
        func_converter = lambda str_or_bytes: int_from_str_or_bytes(
            str_or_bytes, base=base)
        self.change_data(map(func_converter, t_4str_or_4bytes))


## Note: all those are from Raylib in:
# https://www.raylib.com/cheatsheet/cheatsheet.html#colors
## with some tiny modification of values. THANKS TO RAYLIB :D
LIGHTGRAY = Color((200, 200, 200, 255))
GRAY = Color((130, 130, 130, 255))
DARKGRAY = Color((80, 80, 80, 255))
YELLOW = Color((255, 255, 0, 255))
GOLD = Color((255, 200, 0, 255))
ORANGE = Color((255, 160, 0, 255))
PINK = Color((255, 110, 195, 255))
RED = Color((255, 0, 0, 255))
MAROON = Color((190, 35, 55, 255))
GREEN = Color((0, 255, 0, 255))
LIME = Color((0, 160, 50, 255))
DARKGREEN = Color((0, 120, 45, 255))
SKYBLUE = Color((100, 190, 255, 255))
BLUE = Color((0, 0, 255, 255))
DARKBLUE = Color((0, 0, 175, 255))
PURPLE = Color((200, 120, 255, 255))
VIOLET = Color((135, 60, 190, 255))
DARKPURPLE = Color((110, 30, 125, 255))
BEIGE = Color((210, 175, 130, 255))
BROWN = Color((125, 105, 80, 255))
DARKBROWN = Color((75, 65, 45, 255))
WHITE = Color((255, 255, 255, 255))
BLACK = Color((0, 0, 0, 255))
BLANK = Color((0, 0, 0, 0))
MAGENTA = Color((255, 0, 255, 255))
RAYWHITE = Color((245, 245, 245, 255))
##
ALL_COLORS = [LIGHTGRAY, GRAY, DARKGRAY, YELLOW, GOLD, ORANGE, RED, MAROON,
              PINK, MAGENTA, PURPLE, VIOLET, DARKPURPLE, SKYBLUE, BLUE,
              DARKBLUE, GREEN, LIME, DARKGREEN, BEIGE, BROWN, DARKBROWN, WHITE,
              RAYWHITE, BLACK, BLANK]


class Vector(FixList):
    """Any length of a Vector to handle Sequence of Numbers (float or int).

    Examples:

    >>> v1 = Vector([1,2,3])
    >>> v2 = Vector([1,2,10])
    >>> v3 = Vector([-1,2,10])
    >>> v4 = Vector([-1,1,2])
    >>> v1, v2, v3, v4
    ([1, 2, 3], [1, 2, 10], [-1, 2, 10], [-1, 1, 2])
    >>> print(v1, v2, v3, v4)
    [1, 2, 3] [1, 2, 10] [-1, 2, 10] [-1, 1, 2]
    >>> print(len(v1), len(v2), len(v3), len(v4))
    3 3 3 3
    >>> v1 > v2
    False
    >>> v1 > v3  # it must all comparison match to return True
    False
    >>> v1 > v4
    True
    >>> v1 == v2
    False
    >>> v1 != v2  # it must all comparison match to return True
    False
    >>> v1 > 1  # you can also compare with number with all value in vector
    False
    >>> v1 >= 1
    True
    >>> v1 + v2
    [2, 4, 13]
    >>> v2 - v4
    [2, 1, 8]
    >>> v3 * v1
    [-1, 4, 30]
    >>> v2 / v4
    [-1.0, 2.0, 5.0]
    >>> v2 // v4 # floor division
    [-1, 2, 5]
    >>> v4 % v2
    [0, 1, 2]
    >>> v1 ** v2
    [1, 4, 59049]
    >>> pow(v1, v3, mod=10)  # mod is like ``%`` operation
    [1, 4, 9]
    >>> result = v1 + v2
    >>> print(result, type(result).__name__)
    [2, 4, 13] Vector
    >>> result1 = v1 + (-10, 84, 2)  # any Sequence with same length
    >>> print(result1, type(result1).__name__)
    [-9, 86, 5] Vector
    >>> result2 = (-10, 84, 2) + v1
    >>> print(result2, type(result2).__name__)
    [-9, 86, 5] Vector
    >>> V = Vector([1, 210, -1])
    >>> V.dot_product(v1, v2, v3)
    1379
    >>> V.magnitude
    210.0047618507733
    >>> V.normalize
    [0.004761796785877586, 0.9999773250342929, -0.004761796785877586]
    >>> V  # untouch
    [1, 210, -1]
    >>> V.normalize_it()  # now it normalized
    >>> V  # now it changed !!
    [0.004761796785877586, 0.9999773250342929, -0.004761796785877586]
    >>> V = Vector((1, 2.6, -3.1))  # new one :D
    >>> -V
    [-1, -2.6, 3.1]
    >>> r_abs = abs(V)
    >>> print(r_abs, type(r_abs).__name__)
    [1, 2.6, 3.1] Vector
    >>> r_round = round(V)
    >>> print(r_round, type(r_round).__name__)
    [1, 3, -3] Vector
    >>> from math import ceil
    >>> r_ceil = ceil(V)
    >>> print(r_ceil, type(r_ceil).__name__)
    [1, 3, -3] Vector
    >>> from math import floor
    >>> r_floor = floor(V)
    >>> print(r_floor, type(r_floor).__name__)
    [1, 2, -4] Vector
    >>> r_pow = pow(V, -1)
    >>> print(r_pow, type(r_pow).__name__)
    [1.0, 0.3846153846153846, -0.3225806451612903] Vector
    >>> r_divmod = divmod(V, 5)
    >>> print(r_divmod, type(r_divmod).__name__)
    [(0, 1), (0.0, 2.6), (-1.0, 1.9)] list
    >>> V = Vector([0.999999999, 0.999999999, 0.999999999])
    >>> V.is_close_value(1)
    True
    >>> V * float("nan")
    [nan, nan, nan]
    >>> V * float("inf")
    [inf, inf, inf]
    >>> V * float("-inf")
    [-inf, -inf, -inf]
    """

    def __format__(self, format_spec):
        return string_format_vector(self._data, format_spec)

    ########## Operation
    def method_add(self, other):
        """Addition between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.
        """
        if is_number(other):
            return self.__class__(vector_add_values(self, other))
        elif is_vector(other):
            return self.__class__(vector_add_vectors(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Addition", self.__class__.__name__, type(other)))

    def method_sub(self, other):
        """Subtraction between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.
        """
        if is_number(other):
            return self.__class__(vector_sub_values(self, other))
        elif is_vector(other):
            return self.__class__(vector_sub_vectors(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Subtraction", self.__class__.__name__, type(other)))

    def method_mul(self, other):
        """Multiplication between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.
        """
        if is_number(other):
            return self.__class__(vector_mul_values(self, other))
        elif is_vector(other):
            return self.__class__(vector_mul_vectors(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Multiplication", self.__class__.__name__, type(other)))

    def method_truediv(self, other, reverse=False):
        """True Division between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be (vector / other).
        | * if it's True the operation order will be (other / vector).
        """
        if is_number(other):
            return self.__class__(
                vector_truediv_value(self, other, reverse=reverse))
        elif is_vector(other):
            if reverse:
                return self.__class__(vector_truediv_vector(other, self))
            return self.__class__(vector_truediv_vector(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "True Division", self.__class__.__name__, type(other)))

    def method_floordiv(self, other, reverse=False):
        """Floor Division between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be (vector // other).
        | * if it's True the operation order will be (other // vector).
        """
        if is_number(other):
            return self.__class__(
                vector_floordiv_value(self, other, reverse=reverse))
        elif is_vector(other):
            if reverse:
                return self.__class__(vector_floordiv_vector(other, self))
            return self.__class__(vector_floordiv_vector(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Floor Division", self.__class__.__name__, type(other)))

    def method_mod(self, other, reverse=False):
        """Mod between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be (vector % other).
        | * if it's True the operation order will be (other % vector).
        """
        if is_number(other):
            return self.__class__(
                vector_mod_value(self, other, reverse=reverse))
        elif is_vector(other):
            if reverse:
                return self.__class__(vector_mod_vector(other, self))
            return self.__class__(vector_mod_vector(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Mod", self.__class__.__name__, type(other)))

    def method_pow(self, power, mod=None, reverse=False):
        """Power between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.

        Note: ``mod`` is same as parameter `mod` from builtins function `pow`.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be (vector ** power).
        | * if it's True the operation order will be (power ** vector).
        """
        if is_number(power):
            return self.__class__(
                vector_pow_value(self, power, mod=mod, reverse=reverse))
        elif is_vector(power):
            if reverse:
                return self.__class__(vector_pow_vector(power, self, mod=mod))
            return self.__class__(vector_pow_vector(self, power, mod=mod))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Power", self.__class__.__name__, type(power)))

    def method_divmod(self, other, reverse=False):
        """Divmod between a Vector and other.

        Warning: ``other`` Must be either Number (float or int) or another
         Vector (Sequence of Numbers) both Must have same length.
         in case if it wrong type it will raise TypeError.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be divmod(vector, power).
        | * if it's True the operation order will be divmod(power, vector).
        """
        if is_number(other):
            return list(vector_divmod_value(self, other, reverse=reverse))
        elif is_vector(other):
            if reverse:
                return list(vector_divmod_vector(other, self))
            return list(vector_divmod_vector(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Divmod", self.__class__.__name__, type(other)))

    def method_round(self, ndigits=None):
        """Return Vector after round all Numbers (float or integer)."""
        return self.__class__(vector_round(self, ndigits=ndigits))

    def method_ceil(self):
        """Return Vector after ceil all Numbers (float or integer)."""
        return self.__class__(vector_ceil(self))

    def method_floor(self):
        """Return Vector after floor all Numbers (float or integer)."""
        return self.__class__(vector_floor(self))

    def __add__(self, other):
        try:
            return self.method_add(other)
        except TypeError:
            return NotImplemented

    __radd__ = method_add

    def __sub__(self, other):
        try:
            return self.method_sub(other)
        except TypeError:
            return NotImplemented

    __rsub__ = method_sub

    def __mul__(self, other):
        try:
            return self.method_mul(other)
        except TypeError:
            return NotImplemented

    __rmul__ = method_mul

    def __truediv__(self, other):
        try:
            return self.method_truediv(other)
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, other):
        return self.method_truediv(other, reverse=True)

    def __floordiv__(self, other):
        try:
            return self.method_floordiv(other)
        except TypeError:
            return NotImplemented

    def __rfloordiv__(self, other):
        return self.method_floordiv(other, reverse=True)

    def __mod__(self, other):
        try:
            return self.method_mod(other)
        except TypeError:
            return NotImplemented

    def __rmod__(self, other):
        return self.method_mod(other, reverse=True)

    def __pow__(self, power, modulo=None):
        try:
            return self.method_pow(power, mod=modulo)
        except TypeError:
            return NotImplemented

    def __rpow__(self, power, modulo=None):
        return self.method_pow(power, mod=modulo, reverse=True)

    def __divmod__(self, other):
        try:
            return self.method_divmod(other)
        except TypeError:
            return NotImplemented

    def __rdivmod__(self, other):
        return self.method_divmod(other, reverse=True)

    __round__ = method_round
    __ceil__ = method_ceil
    __floor__ = method_floor

    def __lt__(self, other):
        if is_number(other):
            return is_vector_lt_value(self, other)
        elif isinstance(other, Sequence):
            return is_vector_lt_vector(self, other)
        else:
            return False

    def __le__(self, other):
        if is_number(other):
            return is_vector_le_value(self, other)
        elif isinstance(other, Sequence):
            return is_vector_le_vector(self, other)
        else:
            return False

    def __eq__(self, other):
        if is_number(other):
            return is_vector_eq_value(self, other)
        elif isinstance(other, Sequence):
            return is_vector_eq_vector(self, other)
        else:
            return False

    def __ne__(self, other):
        if is_number(other):
            return is_vector_ne_value(self, other)
        elif isinstance(other, Sequence):
            return is_vector_ne_vector(self, other)
        else:
            return False

    def __gt__(self, other):
        if is_number(other):
            return is_vector_gt_value(self, other)
        elif isinstance(other, Sequence):
            return is_vector_gt_vector(self, other)
        else:
            return False

    def __ge__(self, other):
        if is_number(other):
            return is_vector_ge_value(self, other)
        elif isinstance(other, Sequence):
            return is_vector_ge_vector(self, other)
        else:
            return False

    def __abs__(self):
        return self.__class__(vector_abs(self))

    def __neg__(self):
        return self.__class__(vector_negative(self))

    def __pos__(self):
        return self.copy()

    ########## Properties
    @property
    def magnitude(self):
        """return Euclidean norm (or magnitude)."""
        return magnitude_vector(self)

    @property
    def magnitude_sq(self):
        """return Square of Euclidean norm (or magnitude)."""
        return magnitude_vector_sq(self)

    @property
    def normalize(self):
        """return a normalized."""
        return self.__class__(vector_normalize(self))

    @property
    def is_normalized(self):
        """Return True if vector is normalized, otherwise False."""
        return is_vector_normalized(self)

    ########## Methods
    def to_vector(self):
        """Convert to Vector.

        Note: this methods for child classes (subclasses).
        """
        return Vector(self.copy())

    def to_vector2(self):
        """Convert to Vector2.

        Warning: length of Vector Must be 2. Or it will raise ValueError.
        """
        return Vector2(self.copy())

    def to_vector3(self):
        """Convert to Vector3.

        Warning: length of Vector Must be 3. Or it will raise ValueError.
        """
        return Vector3(self.copy())

    def to_vector4(self):
        """Convert to Vector4.

        Warning: length of Vector Must be 4. Or it will raise ValueError.
        """
        return Vector4(self.copy())

    def to_matrix(self, size):
        """Convert Vector to Matrix of size specified. Then Return it."""
        return Matrix(matrix_from_vector(self, size))

    def normalize_it(self):
        """Normalizing Vector."""
        self.change_data(vector_normalize(self))

    def midpoint_between(self, vector):
        """Return Midpoint between 2 Vectors (Must have same length).

        Warning: in case vector doesn't have same length.
         it will raise IndexError.
        """
        return self.__class__(vector_midpoint(self, vector))

    ## those just are alias for functions
    dot_product = dot_product_vectors
    dot_product.__doc__ = (
        """Return Dot Product between Vectors (Must have same length).

        Examples:

        >>> v1 = Vector([7, 9])
        >>> v2 = Vector([0.5, 2])
        >>> print(v1.dot_product_with(v2))
        21.5
        >>> print(v2.dot_product_with(v1))
        21.5
        >>> print(v1.dot_product_with([-2, 0.5]))  # can work with any sequence
        -9.5
        >>> print(v1.dot_product_with(range(2)))  # yap range are Sequence :]
        9
        """)

    distance_to = distance_vectors
    distance_to.__doc__ = (
        """Return Distance between 2 Vectors (Must have same length).

        Examples:

        >>> v1 = Vector([1, 1])
        >>> v2 = Vector([-10, -10])
        >>> print(v1.distance_to(v2))
        15.556349186104045
        >>> print(v2.distance_to(v1))
        15.556349186104045
        >>> print(v1.distance_to((10, 10)))  # can work with any sequence
        12.727922061357855
        >>> print(v1.distance_to([-1, 1]))  # this just to make sure :]
        2.0
        """)

    is_close_vector = is_vector_close_vector

    is_close_value = is_vector_close_value

    is_nan_or_inf = is_inf_or_nan = is_vector_nan_or_inf

    is_nan = is_vector_nan

    is_inf = is_vector_inf


class Vector2(Vector):
    """Vector For 2D (x, y).

    Examples:
    >>> V2 = Vector2([10, 20])
    >>> V2
    [x=10, y=20]
    >>> V = Vector([-2, 9.7])
    >>> V
    [-2, 9.7]
    >>> result1 = V + V2
    >>> print(result1, type(result1).__name__)  # ALWAYS SAME CLASS OF LEFT
    [8, 29.7] Vector
    >>> result2 = V2 + V
    >>> print(result2, type(result2).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=8, y=29.7] Vector2
    >>> result3 = V2 + V2 + V
    >>> print(result3, type(result3).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=18, y=49.7] Vector2
    >>> result4 = V2 + V + V2
    >>> print(result4, type(result4).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=18, y=49.7] Vector2
    >>> result5 = V + V2 + V2
    >>> print(result5, type(result5).__name__)
    [18, 49.7] Vector
    """
    VECTOR2_SPECIAL_STR = "[x=%s, y=%s]"

    # VECTOR2_SPECIAL_REPR  # not used

    def __init__(self, any_vector2=None, *args, **kwargs):
        """Create Instance of Vector2.

        Warning: ``any_vector2`` Must be Iterable of 2 Numbers (float or
         integer). Or it will raise ValueError.

        Note: ``any_vector2`` (by default None)
        | * if it's None or not specified Create Empty Vector2 (full of zero)
        | * if it's specified Create Vector2 from it.
        """
        specific_length = 2
        if any_vector2:
            super(Vector2, self).__init__(any_vector2)
            #### check
            self.strict_length(specific_length)
            #### end check
        else:
            super(Vector2, self).__init__(vector_zero(specific_length))

    def __str__(self):
        return self.VECTOR2_SPECIAL_STR % tuple(self)

    __repr__ = __str__

    def __format__(self, format_spec):
        return self.VECTOR2_SPECIAL_STR % tuple(
            map(lambda value: format(value, format_spec), self))

    ########## Properties
    @property
    def x(self):
        """position Vector2 in X-axis."""
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def x_int(self):
        """return position Vector2 in X-axis as an integer."""
        return int(self.x)

    @property
    def y(self):
        """position Vector2 in Y-axis."""
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def y_int(self):
        """return position Vector2 in Y-axis as an integer."""
        return int(self.y)

    ########## Methods
    angle = angle_v2
    angle.__doc__ = (
        """Return Angle (in radians range in [-pi, pi]) Between 2 Vector2 (x, y)
         based on ``center``.

        Warning: ``center`` Must not Equal To any ``v1`` or ``v2``.
         Or it will raise ValueError.

        Note: ``center`` (by default None)
        | * if it's None or not specified. center will be [x=0, y=0].
        | * if it's specified use it (it should be any Vector2 (x, y)) :D.

        Note: output will return angle in radius between [-pi, pi].

        Examples:

        >>> v1 = Vector2((0, 1))
        >>> v2 = Vector2((1, 0))
        >>> c = Vector2((0.5, 0.5))
        >>> print(v1.angle(v2))
        -1.5707963267948966
        >>> print(v1.angle((10 ,10)))  # work with any sequence
        -0.7853981633974483
        >>> print(v2.angle(v1))
        1.5707963267948966
        >>> print(v1.angle(v2, center=c))
        3.141592653589793
        >>> print(v1.angle(v2, center=(-1, -1)))  # work with any sequence
        -0.6435011087932844
        >>> print(v2.angle(v1, center=c))
        3.141592653589793
        """)

    def cross_product(self, vector2):
        """Cross Product Between 2 Vector2 (x, y).
         Return a Vector3 (First 2 Numbers are always zero 0).
        """
        return Vector3(cross_product_v2(self, vector2))


Point2D = Vector2


class Vector3(Vector):
    """Vector For 3D (x, y, z).

    Examples:

    >>> V3 = Vector3([10, 20, 30])
    >>> V3
    [x=10, y=20, z=30]
    >>> V = Vector([-2, 9.7, 0.2])
    >>> V
    [-2, 9.7, 0.2]
    >>> result1 = V - V3
    >>> print(result1, type(result1).__name__)  # ALWAYS SAME CLASS OF LEFT
    [-12, -10.3, -29.8] Vector
    >>> result2 = V3 - V
    >>> print(result2, type(result2).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=12, y=10.3, z=29.8] Vector3
    >>> result3 = V3 - V3 - V
    >>> print(result3, type(result3).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=2, y=-9.7, z=-0.2] Vector3
    >>> result4 = V3 - V - V3
    >>> print(result4, type(result4).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=2, y=-9.7, z=-0.1999999999999993] Vector3
    >>> result5 = V - V3 - V3
    >>> print(result5, type(result5).__name__)
    [-22, -30.3, -59.8] Vector
    """
    VECTOR3_SPECIAL_STR = "[x=%s, y=%s, z=%s]"

    # VECTOR3_SPECIAL_REPR  # not used

    def __init__(self, any_vector3=None, *args, **kwargs):
        """Create Instance of Vector3.

        Warning: ``any_vector3`` Must be Iterable of 3 Numbers (float or
         integer). Or it will raise ValueError.

        Note: ``any_vector3`` (by default None)
        | * if it's None or not specified Create Empty Vector3 (full of zero)
        | * if it's specified Create Vector3 from it.
        """
        specific_length = 3
        if any_vector3:
            super(Vector3, self).__init__(any_vector3)
            #### check
            self.strict_length(specific_length)
            #### end check
        else:
            super(Vector3, self).__init__(vector_zero(specific_length))

    def __str__(self):
        return self.VECTOR3_SPECIAL_STR % tuple(self)

    __repr__ = __str__

    def __format__(self, format_spec):
        return self.VECTOR3_SPECIAL_STR % tuple(
            map(lambda value: format(value, format_spec), self))

    ########## Properties
    @property
    def x(self):
        """position Vector3 in X-axis."""
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def x_int(self):
        """return position Vector3 in X-axis as an integer."""
        return int(self.x)

    @property
    def y(self):
        """position Vector3 in Y-axis."""
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def y_int(self):
        """return position Vector3 in Y-axis as an integer."""
        return int(self.y)

    @property
    def z(self):
        """position Vector3 in Z-axis."""
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    @property
    def z_int(self):
        """return position Vector3 in Z-axis as an integer."""
        return int(self.z)

    ########## Methods
    angle = angle_v3
    angle.__doc__ = (
        """Return Angle Between 2 Vector3 (x, y, z) based on center.

        Warning: ``center`` Must not Equal To any ``v1`` or ``v2``.
         Or it will Raise ValueError.

        Note: ``center`` (by default None)
        | * if it's None or not specified. center will be [x=0, y=0, z=0].
        | * if it's specified use it (it should be any Vector2 (x, y, z)).

        Note: output will return angle in radius between [-pi, pi].

        Examples:

        >>> v1 = Vector2((0, 1))
        >>> v2 = Vector2((1, 0))
        >>> c = Vector2((0.5, 0.5))
        >>> print(v1.angle(v2))
        -1.5707963267948966
        >>> print(v1.angle((10 ,10)))  # work with any sequence
        -0.7853981633974483
        >>> print(v2.angle(v1))
        1.5707963267948966
        >>> print(v1.angle(v2, center=c))
        3.141592653589793
        >>> print(v1.angle(v2, center=(-1, -1)))  # work with any sequence
        -0.6435011087932844
        >>> print(v2.angle(v1, center=c))
        3.141592653589793
        """)

    def cross_product(self, vector3):
        """Cross Product Between 2 Vector3 (x, y, z). Return a Vector3."""
        return Vector3(cross_product_v3(self, vector3))


Point3D = Vector3


class Euler(Vector):
    """Euler Angles (yaw, pitch, roll) (all in radians).

    Note: this use Tait–Bryan Angles Only (no repeat axis).
    """
    EULER_SPECIAL_STR = "[yaw=%s, pitch=%s, roll=%s]"
    EULER_SPECIAL_REPR = "Euler(yaw=%s, pitch=%s, roll=%s, order=\"%s\")"

    def __init__(self, yaw_pitch_roll, order, *args, **kwargs):
        """Create Instance of Euler.

        Warning: ``yaw_pitch_roll`` Must be Iterable of 3 Numbers (float or
         integer) all in radians. Or it will raise ValueError.

        Warning: ``order`` must be string for order axis rotation for
         Euler Angles (a.k.a. Tait–Bryan angles) either uppercase or lowercase
         or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
         Or it will raise ValueError.
        """
        specific_length = 3
        if yaw_pitch_roll:
            super(Euler, self).__init__(yaw_pitch_roll)
            #### check
            self.strict_length(specific_length)
            #### end check
        else:
            super(Euler, self).__init__(vector_zero(specific_length))
        order = order.upper()
        #### check
        if order not in EulerAnglesOrders:
            raise ValueError(EM_UNSUPPORTED_ORDER_EULER % order)
        #### end check
        self.__order = order

    def __str__(self):
        return self.EULER_SPECIAL_STR % tuple(self)

    def __repr__(self):
        return self.EULER_SPECIAL_REPR % (self.yaw, self.pitch, self.roll,
                                          self.order)

    def __format__(self, format_spec):
        return self.EULER_SPECIAL_STR % tuple(
            map(lambda value: format(value, format_spec), self))

    ########## Properties
    @property
    def order(self):
        """Order of axis rotation of Euler angles (Read Only) (Upper case)."""
        return self.__order

    @property
    def yaw(self):
        """Yaw in radians."""
        return self[0]

    @yaw.setter
    def yaw(self, value):
        self[0] = value

    @property
    def yaw_degrees(self):
        """Yaw in degrees (Read Only)."""
        return degrees(self.yaw)

    @property
    def pitch(self):
        """Pitch in radians."""
        return self[1]

    @pitch.setter
    def pitch(self, value):
        self[1] = value

    @property
    def pitch_degrees(self):
        """Pitch in degrees (Read Only)."""
        return degrees(self.pitch)

    @property
    def roll(self):
        """Roll in radians."""
        return self[2]

    @roll.setter
    def roll(self, value):
        self[2] = value

    @property
    def roll_degrees(self):
        """Roll in degrees (Read Only)."""
        return degrees(self.roll)

    ########## Methods
    def change_order(self, new_order):
        """this will change Order of Euler angles (Tait–Bryan angles).

        Warning: ``new_order`` must be string for order axis rotation for
         Euler Angles (a.k.a. Tait–Bryan angles) either  uppercase or lowercase
         or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
         Or it will raise ValueError.
        """
        self.yaw, self.pitch, self.roll = euler_from_euler(self.yaw, self.pitch,
                                                           self.roll,
                                                           self.order,
                                                           new_order)
        self.__order = new_order.upper()

    def to_matrix_3x3(self):
        """Convert Euler Angles to Matrix 3x3.

        Warning: Be Careful about Gimbal Lock.
        """
        return Matrix_3x3(
            matrix_3x3_from_euler(self.yaw, self.pitch, self.roll, self.order))

    def to_quaternion(self):
        """Convert Euler Angles to Quaternion (a.k.a. Vector4)."""
        return Vector4(
            quaternion_from_euler(self.yaw, self.pitch, self.roll, self.order))

    def to_axis_angle(self):
        """Convert Euler Angles to Axis (Vector3) and angle in a Tuple.

        Warning: Be Careful about Gimbal Lock.
        """
        v, angle = axis_angle_from_euler(self.yaw, self.pitch, self.roll,
                                         self.order)
        return Vector3(v), angle

    def from_matrix_3x3(self, matrix_3x3):
        """Convert Any Matrix (3x3) To Euler Angles (yaw, pitch, roll).

        Note: ``matrix_3x3`` is Not normalized in function.

        Note: ``yaw`` and ``roll`` will be between [-pi, pi],
         and ``pitch`` will be between [-pi/2, pi/2].
        """
        self.yaw, self.pitch, self.roll = euler_from_matrix_3x3(matrix_3x3,
                                                                self.order)

    def from_quaternion(self, quaternion):
        """Convert Quaternion (a.k.a. Vector4 (x, y, z, w)) To Euler angles.

        Warning: be Careful about ZeroDivision if ``quaternion`` Equal To 0.

        Note: ``quaternion`` is normalized in function (if it's not normalized).

        Note: both of ``yaw`` and ``roll`` will be between [-pi, pi],
         and ``pitch`` will be between [-pi/2, pi/2].
        """
        self.yaw, self.pitch, self.roll = euler_from_quaternion(quaternion,
                                                                self.order)

    def from_axis_angle(self, axis, angle):
        """Convert Axis (x, y, z) and angle (in radians) To Euler angles.

        Warning: be Careful about ZeroDivision in case ``axis`` Equal To 0.

        Note: ``axis`` is normalized in function.

        Note: both of ``yaw`` and ``roll`` will be between [-pi, pi],
         and ``pitch`` will be between [-pi/2, pi/2].
        """
        self.yaw, self.pitch, self.roll = euler_from_axis_angle(axis, angle,
                                                                self.order)

    def from_euler(self, yaw, pitch, roll, input_order):
        """Convert Euler Angles from Euler Angles with specific order.

        Warning: all of input ``yaw`` and ``pitch`` and ``roll`` all in radians.
         also be Careful about Gimbal Lock.

        Warning: ``input_order`` must be string for order axis rotation for
         Euler Angles (a.k.a. Tait–Bryan angles) either uppercase or lowercase
         or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX','zyx', 'Zyx', etc...).
         Or it will raise ValueError.
        """
        self.yaw, self.pitch, self.roll = euler_from_euler(yaw, pitch, roll,
                                                           input_order,
                                                           self.order)


class Vector4(Vector):
    """Vector For 4D Also known as Quaternion (x, y, z, w).

    Examples:

    >>> V4 = Vector4([10, 20, 30, 40])
    >>> V4
    [x=10, y=20, z=30, w=40]
    >>> V = Vector([-2, 0.7, 0.2, -0.8])
    >>> V
    [-2, 0.7, 0.2, -0.8]
    >>> result1 = V * V4
    >>> print(result1, type(result1).__name__)  # ALWAYS SAME CLASS OF LEFT
    [-20, 14.0, 6.0, -32.0] Vector
    >>> result2 = V4 * V
    >>> print(result2, type(result2).__name__)  # ALWAYS SAME CLASS OF LEFT
    [x=-20, y=14.0, z=6.0, w=-32.0] Vector4
    >>> result3 = V4 * V4
    >>> print(result3, type(result3).__name__)
    [x=100, y=400, z=900, w=1600] Vector4
    """
    VECTOR4_SPECIAL_STR = "[x=%s, y=%s, z=%s, w=%s]"

    # VECTOR4_SPECIAL_REPR  # not used

    def __init__(self, any_vector4=None):
        """Create Instance of Vector4.

        Warning: ``any_vector4`` Must be Iterable of 4 Numbers (float or
         integer). Or it will raise ValueError.

        Note: ``any_vector4`` (by default None)
        | * if it's None or not specified Create Empty Vector4 (full of zero)
        | * if it's specified Create Vector4 from it.
        """
        specific_length = 4
        if any_vector4:
            super(Vector4, self).__init__(any_vector4)
            #### check
            self.strict_length(specific_length)
            #### end check
        else:
            super(Vector4, self).__init__(vector_zero(specific_length))

    def __str__(self):
        return self.VECTOR4_SPECIAL_STR % tuple(self)

    __repr__ = __str__

    def __format__(self, format_spec):
        return self.VECTOR4_SPECIAL_STR % tuple(
            map(lambda value: format(value, format_spec), self))

    ########## Main Info
    @property
    def x(self):
        """position Vector4 in X-axis."""
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value

    @property
    def x_int(self):
        """return position Vector4 in X-axis as an integer."""
        return int(self.x)

    @property
    def y(self):
        """position Vector4 in Y-axis."""
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def y_int(self):
        """return position Vector4 in Y-axis as an integer."""
        return int(self.y)

    @property
    def z(self):
        """position Vector4 in Z-axis."""
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    @property
    def z_int(self):
        """return position Vector4 in Z-axis as an integer."""
        return int(self.z)

    @property
    def w(self):
        """position Vector4 in W-axis."""
        return self[3]

    @w.setter
    def w(self, value):
        self[3] = value

    @property
    def w_int(self):
        """return position Vector4 in W-axis as an integer."""
        return int(self.w)

    ########## Properties
    @classmethod
    @property
    def identity(cls):
        """Return Identity of Quaternion (Vector4)."""
        return Vector4(quaternion_identity())

    @property
    def opposite(self):
        """Return opposite rotation of Quaternion/Vector4 (-x, -y, -z, w)."""
        return Vector4(quaternion_opposite(self))

    ########## Methods
    def identity_it(self):
        """Identity the Quaternion (Vector4)."""
        self.x, self.y, self.z, self.w = quaternion_identity()

    def opposite_it(self):
        """opposite rotation of Quaternion/Vector4 (-x, -y, -z, w)."""
        self.x, self.y, self.z, self.w = quaternion_opposite(self)

    def mul_quaterion(self, other):
        """Return result of Multiplication between 2 Quaternion (Vector4)."""
        return Vector4(quaternion_multiply(self, other))

    def mul_quaterion_it(self, other):
        """Multiplication between 2 Quaternion (Vector4)."""
        self.x, self.y, self.z, self.w = quaternion_multiply(self, other)

    def to_axis_angle(self):
        """Convert Quaternion to axis (Vector3) and angle (in radians[0, 2*pi]).

        Note: ``quaterion`` are normalized in function
         (only if not (-1 >= w >= 1)).
        """
        v, angle = axis_angle_from_quaternion(self)
        return Vector3(v), angle

    def to_euler(self, order):
        """Convert Quaternion (a.k.a. Vector4 (x, y, z, w)) To Euler angles.

        Warning: be Careful about ZeroDivision in case Quaternion Equal To 0.

        Warning: ``order`` must be string for order axis rotation for
         Euler angles (a.k.a. Tait–Bryan angles) either uppercase or
         lowercase or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx',
         etc...). or it will raise ValueError.

        Note: Quaternion is normalized in function.

        Note: in the output both of ``yaw`` and ``roll`` are between [-pi, pi],
         and ``pitch`` is between [-pi/2, pi/2].
        """
        return Euler(euler_from_quaternion(self, order), order)

    def to_matrix_3x3(self):
        """Convert a Quaternion (x, y, z, w) To Matrix (3x3).

        Warning: Be CAREFUL with ZeroDivision (in case Quaternion Equal To 0).

        Note: ``quaternion`` is normalized in function.

        Info: http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
        """
        return Matrix_3x3(matrix_3x3_from_quaternion(self))

    def from_axis_angle(self, axis, angle):
        """Convert axis (x, y, z) and angle (in radians) To Quaternion.

        Note: ``axis`` is normalized in function.
        """
        self.x, self.y, self.z, self.w = quaternion_from_axis_angle(axis, angle)

    def from_euler(self, yaw, pitch, roll, order):
        """Convert Euler angles (yaw, pitch, roll) (all in radians) To
         Quaternion.

        Warning: ``yaw`` and ``pitch`` and ``roll`` all Must be in radians.

        Warning: ``order`` must be string for order axis rotation for
         Euler angles (a.k.a. Tait–Bryan angles) either uppercase or lowercase
         or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
         Or it will raise ValueError.
        """
        self.x, self.y, self.z, self.w = quaternion_from_euler(yaw, pitch, roll,
                                                               order)

    def from_matrix_3x3(self, matrix_3x3):
        """Convert a Matrix (3x3) To Quaternion.

        Note: ``matrix_3x3`` is Not normalized in function.
        """
        self.x, self.y, self.z, self.w = quaternion_from_matrix_3x3(matrix_3x3)


Quaternion = Point4D = Vector4


class Matrix(FixList):
    """Any Matrix NxM (rows x columns).
    Matrix should be like: [[a0_0, a0_1, ..., a0_M], ..., [aN_0, ...,aN_M]]
    """

    def __init__(self, iterable_vectors, *args, **kwargs):
        super(Matrix, self).__init__(map(lambda v: list(v), iterable_vectors))

    def __str__(self):
        return string_matrix(self._data)

    __repr__ = __str__

    def __format__(self, format_spec):
        return string_format_matrix(self._data, format_spec)

    def __getitem__(self, index):
        item = matrix_getitem(self._data, index)
        if is_number(item):
            return item
        elif isinstance(item, Iterable):
            if is_all_numbers(item):
                return Vector(item)
            else:
                return Matrix(item)
        raise IndexError(EM_NOT_EXPECTED % (
            "index (int or slice) or tuple of 2 index", index))

    def __setitem__(self, index, new_value):
        self.change_data(matrix_setitem(self._data, index, new_value))

    def __getattr__(self, name):
        if re.match(MATRIX_PATTERN_ATTRIB, name):
            length_letter = len(MATRIX_START_LETTER_ATTRIB)
            underscore_index = name.find("_", length_letter)
            if underscore_index != -1:
                first_index = int(name[length_letter:underscore_index])
                second_index = int(name[underscore_index + 1:])  # +1 for `_`
                return self._data[first_index][second_index]
            raise AttributeError(EM_WRONG_MATRIX_PATTERN_ATTRIB % name)
        raise AttributeError(EM_NO_ATTRIBUTE % (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if re.match(MATRIX_PATTERN_ATTRIB, name):
            length_letter = len(MATRIX_START_LETTER_ATTRIB)
            underscore_index = name.find("_", length_letter)
            if underscore_index != -1:
                first_index = int(name[length_letter:underscore_index])
                second_index = int(name[underscore_index + 1:])  # +1 for `_`
                self._data[first_index][second_index] = value
                return None
            raise AttributeError(EM_WRONG_MATRIX_PATTERN_ATTRIB % name)
        return super(Matrix, self).__setattr__(name, value)

    ########## Operation
    def method_add(self, other):
        """Addition between 2 Matrices. (all must have same sizes).

        Info: https://www.mathsisfun.com/algebra/matrix-introduction.html
        """
        if is_matrix(other):
            return self.__class__(matrix_add_matrices(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Addition", self.__class__.__name__, type(other)))

    def method_sub(self, other):
        """Subtraction between 2 Matrices. (all must have same sizes).

        Info: https://www.mathsisfun.com/algebra/matrix-introduction.html
        """
        if is_matrix(other):
            return self.__class__(matrix_sub_matrices(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Subtraction", self.__class__.__name__, type(other)))

    def method_mul(self, other, reverse=False):
        """Multiplication between Matrix and Other.

        Warning: ``other`` Must be either Number (float or integer) Or Vector
         (Sequence of Numbers) Or Matrix (Sequence of Vectors).
         in case if it wrong type it will raise TypeError.

        Warning: ``other`` in case if it's Number or Vector YOU CAN'T reverse
         operation order. Or it will raise NotImplementedError.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be (matrix * other).
        | * if it's True the operation order will be (other * matrix).

        Info: https://www.mathsisfun.com/algebra/matrix-introduction.html
        """
        if is_number(other):
            if reverse:
                raise NotImplementedError("NOT IMPLEMENTED for matrix * value")
            return self.__class__(matrix_mul_value(other, self))
        elif is_vector(other):
            if reverse:
                raise NotImplementedError("NOT IMPLEMENTED for matrix * vector")
            return Vector(matrix_mul_vector(other, self))
        elif is_matrix(other):
            if reverse:
                return self.__class__(matrix_mul_matrix(other, self))
            return self.__class__(matrix_mul_matrix(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "Multiplication", self.__class__.__name__, type(other)))

    def method_truediv(self, other, reverse=False):
        """True Division between 2 Matrices.

        Note: ``reverse`` (by default False)
        | * if it's False the operation order will be (matrix / other).
        | * if it's True the operation order will be (other / matrix).

        Info: https://www.mathsisfun.com/algebra/matrix-introduction.html
        """
        if is_matrix(other):
            if reverse:
                return self.__class__(matrix_truediv_matrix(other, self))
            return self.__class__(matrix_truediv_matrix(self, other))
        raise TypeError(EM_UNSUPPORTED_TYPE_OPERATION % (
            "True Division", self.__class__.__name__, type(other)))

    def method_round(self, ndigits=None):
        """Return Matrix after round all Numbers (float or integer)."""
        return self.__class__(matrix_round(self, ndigits=ndigits))

    def method_ceil(self):
        """Return Matrix after ceil all Numbers (float or integer)."""
        return self.__class__(matrix_ceil(self))

    def method_floor(self):
        """Return Matrix after floor all Numbers (float or integer)."""
        return self.__class__(matrix_floor(self))

    def __add__(self, other):
        try:
            return self.method_add(other)
        except TypeError:
            return NotImplemented

    __radd__ = method_add

    def __sub__(self, other):
        try:
            return self.method_sub(other)
        except TypeError:
            return NotImplemented

    __rsub__ = method_sub

    def __mul__(self, other):
        try:
            return self.method_mul(other)
        except TypeError:
            return NotImplemented

    def __rmul__(self, other):
        return self.method_mul(other, reverse=True)

    def __truediv__(self, other):
        try:
            return self.method_truediv(other)
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, other):
        return self.method_truediv(other, reverse=True)

    __round__ = method_round
    __ceil__ = method_ceil
    __floor__ = method_floor

    ########## Property
    @property
    def num_rows(self):
        """Return integer Number of number rows (Read Only)."""
        return len(self)

    @property
    def num_columns(self):
        """Return integer Number of number columns (Read Only)."""
        return len(self._data[0])

    @property
    def size(self):
        """Return Size of Matrix NxM (rows x columns) (Read Only)."""
        return self.num_rows, self.num_columns

    @property
    def is_size_square(self):
        """Return True if number of row Equal To number of columns.
         otherwise False
        """
        return self.num_rows == self.num_columns

    @property
    def transpose(self):
        """Return transposed Matrix.
         The "transpose" a Matrix is swap the rows with columns.
        """
        return self.__class__(matrix_transpose(self))

    @property
    def trace(self):
        """Return trace of any Matrix.
        The "trace" in linear algebra is sum of the values diagonally on Matrix.
         (like: a0_0 + a1_1 + a2_2 + ...)

        Info: https://en.wikipedia.org/wiki/Trace_(linear_algebra)
        """
        return trace_matrix(self)

    @property
    def determinant(self):
        """Return determinant of any square Matrix NxN (Rows x Columns).

        Warning: if Matrix is NOT a Square Matrix NxN. it will raise ValueError.

        Info: Using Cofactor expansion formula (recursive).

        Info: https://en.wikipedia.org/wiki/Determinant
        """
        return determinant_matrix(self)

    @property
    def adjugate(self):
        """Return adjugate of any square Matrix NxN (Rows x Columns) as a List.

        Warning: if Matrix is NOT a Square Matrix NxN. it will raise ValueError.

        Info: https://en.wikipedia.org/wiki/Adjugate_matrix
        """
        return self.__class__(matrix_adjugate(self))

    @property
    def inv(self):
        """Return inverse of Square Matrix NxN (Rows x Columns).

        Warning: if matrix is singular (don't have inverse) that is case its
         determinant Equal To 0. it will raise ValueError.
        """
        return self.__class__(matrix_inv(self))

    ########## Methods
    def strict_size(self, expect_size):
        """Raise ValueError if Matrix size don't match with expect size."""
        expect_num_row, expect_num_column = expect_size
        if (self.num_rows != expect_num_row
                or self.num_columns != expect_num_column):
            raise ValueError(EM_WRONG_MATRIX_SIZE % (
                expect_num_row, expect_num_column, self.num_rows,
                self.num_columns, self._data))

    def to_vector(self):
        """Return Vector after Convert Matrix to Vector."""
        return Vector(vector_from_matrix(self))

    def to_matrix(self):
        """Convert to Matrix.

        Note: this methods for child classes (subclasses).

        Note: this function will COST Memory Be CAREFUL.
        """
        return Matrix(self.deepcopy())

    def to_matrix_2x2(self):
        """Convert to Matrix 2x2.

        Warning: size of Matrix Must be (2x2). Or it will raise ValueError.
        """
        return Matrix_2x2(self.deepcopy())

    def to_matrix_3x3(self):
        """Convert to Matrix 3x3.

        Warning: size of Matrix Must be (3x3). Or it will raise ValueError.
        """
        return Matrix_3x3(self.deepcopy())

    def to_matrix_4x4(self):
        """Convert to Matrix 4x4.

        Warning: size of Matrix Must be (4x4). Or it will raise ValueError.
        """
        return Matrix_4x4(self.deepcopy())

    @classmethod
    def identity(cls, n):
        """Return identity of Matrix NxN (square of n).

        Warning: n Must be an integer (>0), or it will raise ValueError.
        """
        if n == 4:
            return Matrix_4x4(matrix_identity(n))
        elif n == 3:
            return Matrix_3x3(matrix_identity(n))
        elif n == 2:
            return Matrix_2x2(matrix_identity(n))
        return Matrix(matrix_identity(n))

    def identity_it(self):
        """identity the Square Matrix NxN (Rows x Columns).

        Warning: Matrix size Must be NxN (rows x columns) Or it will raise
         ValueError.
        """
        ##### check
        if not self.is_size_square:
            raise ValueError(EM_NOT_SQUARE_MATRIX % self.size)
        ##### end check
        self.change_data(matrix_identity(self.num_rows))

    def adjugate_it(self):
        """adjugate The square Matrix NxN (Rows x Columns).

        Warning: if Matrix is NOT a Square Matrix NxN. it will raise ValueError.

        Info: https://en.wikipedia.org/wiki/Adjugate_matrix
        """
        self.change_data(matrix_adjugate(self))

    def inv_it(self):
        """inverse The square Matrix NxN (Rows x Columns).

        Warning: if matrix is singular (don't have inverse) that is case its
         determinant Equal To 0. it will raise ValueError.
        """
        self.change_data(matrix_inv(self))


class Matrix_2x2(Matrix):
    """Any Matrix (2x2) (Rows x Columns).
    Matrix should be like: [[a0_0, a0_1], [a1_0, a1_1]]
    """

    def __init__(self, any_matrix_2x2=None, *args, **kwargs):
        """Create Instance of Matrix_2x2.

        Warning: size of ``any_matrix_2x2`` Must be (2x2).
         Or it will raise ValueError.

        Note: ``any_matrix_2x2`` (by default None)
        | * if it's None or not specified Create Empty Matrix 2x2 (full of zero)
        | * if it's specified Create Matrix 2x2 from it.
        """
        specific_size = (2, 2)
        if any_matrix_2x2:
            super(Matrix_2x2, self).__init__(any_matrix_2x2)
            ##### check
            self.strict_size(specific_size)
            ##### end check
        else:
            super(Matrix_2x2, self).__init__(
                matrix_zero(specific_size))


class Matrix_3x3(Matrix):
    """Any Matrix (3x3) (Rows x Columns).
    Matrix should be like:
    [[a0_0, a0_1, a0_2],
    [a1_0, a1_1, a1_2],
    [a2_0, a2_1, a2_2]]
    """

    def __init__(self, any_matrix_3x3=None, *args, **kwargs):
        """Create Instance of Matrix_3x3.

        Warning: size of ``any_matrix_3x3`` Must be (3x3).
         Or it will raise ValueError.

        Note: ``any_matrix_3x3`` (by default None)
        | * if it's None or not specified Create Empty Matrix 3x3 (full of zero)
        | * if it's specified Create Matrix 3x3 from it.
        """
        specific_size = (3, 3)
        if any_matrix_3x3:
            super(Matrix_3x3, self).__init__(any_matrix_3x3)
            ##### check
            self.strict_size(specific_size)
            ##### end check
        else:
            super(Matrix_3x3, self).__init__(
                matrix_zero(specific_size))

    ########## Methods
    def from_x_rotation(self, angle, transpose=False):
        """Creates a Matrix with the specified rotation about the X-axis.

        Note: ``angle`` is angle of rotation (in radians) in X-axis.

        Note: ``transpose`` (by default False)
        | * if it's False, the result of Matrix (3x3) will be:
        | [[1, 0, 0],
        | [0, cos_angle, -sin_angle],
        | [0, sin_angle, cos_angle]]
        | * If it's True, the result of Matrix (3x3) will be:
        | [[1, 0, 0],
        | [0, cos_angle, sin_angle],
        | [0, -sin_angle, cos_angle]]
        """
        self.change_data(matrix_3x3_from_x_rotation(angle, transpose=transpose))

    def from_y_rotation(self, angle, transpose=False):
        """Creates a Matrix with the specified rotation about the Y-axis.

        Note: ``angle`` is angle of rotation (in radians) in Y-axis.

        Note: ``transpose`` (by default False)
        | * if it's False, the result Matrix (3x3) will be:
        | [[ cos_angle, 0, sin_angle],
        | [ 0, 1, 0],
        | [-sin_angle, 0, cos_angle]]
        | * if it's True, the result Matrix (3x3) will be:
        | [[cos_angle, 0, -sin_angle],
        | [ 0, 1, 0],
        | [sin_angle, 0, cos_angle]]
        """
        self.change_data(matrix_3x3_from_y_rotation(angle, transpose=transpose))

    def from_z_rotation(self, angle, transpose=False):
        """Creates a Matrix with the specified rotation about the Z-axis.

        Note: ``angle`` is angle of rotation (in radians) in Z-axis.

        Note: ``transpose`` (by default False)
        | * if it's False, the result Matrix (3x3) will be:
        | [[cos_angle, -sin_angle, 0],
        | [sin_angle, cos_angle, 0],
        | [ 0, 0, 1]]
        | * if it's True, the result Matrix (3x3) will be:
        | [[ cos_angle, sin_angle, 0],
        | [-sin_angle, cos_angle, 0],
        | [ 0, 0, 1]]
        """
        self.change_data(matrix_3x3_from_z_rotation(angle, transpose=transpose))

    def from_euler(self, yaw, pitch, roll, order):
        """Convert Euler Angles (yaw, pitch, roll) To Matrix (3x3).

        Warning: ``yaw`` and ``pitch`` and ``roll`` all in radians.
        also be Careful about Gimbal Lock.

        Warning: ``order`` must be string for order axis rotation for
         Euler angles (a.k.a. Tait–Bryan angles) either uppercase or lowercase
         or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
         Or it will raise ValueError.
        """
        self.change_data(matrix_3x3_from_euler(yaw, pitch, roll, order))

    def from_axis_angle(self, axis, angle):
        """Convert Axis (x, y, z) and Angle (in radians) To a Matrix (3x3).

        Note: ``axis`` is normalized in function.
        """
        self.change_data(matrix_3x3_from_axis_angle(axis, angle))

    def from_quaternion(self, quaternion):
        """Convert a Quaternion (x, y, z, w) To Matrix (3x3).

        Warning: Be CAREFUL with ZeroDivision (in case Quaternion Equal To 0).

        Note: ``quaternion`` is normalized in function.

        Info: http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
        """
        self.change_data(matrix_3x3_from_quaternion(quaternion))

    def from_scale(self, scale_v3):
        """Creates an identity Matrix with the scale (x, y, z) set."""
        self.change_data(matrix_3x3_from_scale(scale_v3))

    def from_direction_scale(self, direction_v3, scale):
        """Creates a Matrix which can apply a directional scaling to vectors.

        Warning: ``direction_v3`` Must be any Vector3 (x, y, z).
        """
        self.change_data(matrix_3x3_from_direction_scale(direction_v3, scale))


class Matrix_4x4(Matrix):
    """Any Matrix (4x4) (Rows x Columns).
    Matrix should be like:
    [[a0_0, a0_1, a0_2, a0_3],
    [a1_0, a1_1, a1_2, a1_3],
    [a2_0, a2_1, a2_2, a2_3],
    [a3_0, a3_1, a3_2, a3_3]]
    """

    def __init__(self, any_matrix_4x4=None, *args, **kwargs):
        """Create Instance of Matrix_4x4.

        Warning: size of ``any_matrix_4x4`` Must be (4x4).
         Or it will raise ValueError.

        Note: ``any_matrix_4x4`` (by default None)
        | * if it's None or not specified Create Empty Matrix 4x4 (full of zero)
        | * if it's specified Create Matrix 4x4 from it.
        """
        specific_size = (4, 4)
        if any_matrix_4x4:
            super(Matrix_4x4, self).__init__(any_matrix_4x4)
            ##### check
            self.strict_size(specific_size)
            ##### end check
        else:
            super(Matrix_4x4, self).__init__(
                matrix_zero(specific_size))

    ########## Methods
    def create_look_at(self, eye, target, up, transpose=False):
        """Creates a look at matrix according to OpenGL standards.

        Warning: ``eye`` and ``target`` and ``up`` Must be any Vector3(x, y, z).

        Note: ``transpose`` (by default False).
        | * if it's False, Return Matrix according to OpenGL standards.
        | * if it's True, Return transpose of it.
        """
        self.change_data(
            matrix_4x4_look_at(eye, target, up, transpose=transpose))

    def perspective_projection_bounds(self, left, right, bottom, top, near, far,
                                      transpose=False):
        """Creates perspective projection Matrix using the specified bounds.

        Note: ``transpose`` (by default False)
        | * if it's False, result Matrix (4x4) will be:
        | [[A, 0, 0, 0], # A = 2*near/(right-left)
        | [0, B, 0, 0], # B = 2*near/(top-bottom); C = (right+left)/(right-left)
        | [C, D, E, -1], # D = (top+bottom)/(top-bottom)
        | [0, 0, F, 0]] # E = -(far+near)/(far-near); F = -2*far*near/(far-near)
        | * if it's True, result Matrix (4x4) will be (just transpose it :D):
        | [[A, 0, C, 0],
        | [0, B, D, 0],
        | [0, 0, E, F],
        | [0, 0, -1, 0]]
        """
        self.change_data(
            matrix_4x4_perspective_projection_bounds(left, right, bottom, top,
                                                     near, far,
                                                     transpose=transpose))

    def perspective_projection(self, angle, aspect, near, far, transpose=False):
        """Creates perspective projection Matrix.

        Warning: ``angle`` Must be in radians.

        Warning: all of ``aspect`` and ``near`` and ``far`` Must be Positive
        Numbers (float or integer) (>0). also``near`` Must be Less Than ``far``.
        Or it will raise ValueError.

        Note: ``transpose`` (by default False)
        | * if it's False, result Matrix (4x4) will be:
        | [[A, 0, 0, 0], # A = 1 / (tan(angle/2) * aspect)
        | [0, B, 0, 0], # B = 1/tan(angle/2); C = 1/(2*near*tan(angle/2)*aspect)
        | [C, D, E, -1], # D = 1 / (2 * near * tan(angle / 2))
        | [0, 0, F, 0]] # E = -(far+near)/(far-near); F = -2*far*near/(far-near)
        | * if it's True, result Matrix (4x4) will be (just transpose it):
        | [[A, 0, C, 0],
        | [0, B, D, 0],
        | [0, 0, E, F],
        | [0, 0, -1, 0]]
        """
        self.change_data(
            matrix_4x4_perspective_projection(angle, aspect, near, far,
                                              transpose=transpose))

    def from_translation(self, vector3, transpose=False):
        """Creates an identity Matrix with the translation.

        Note: ``transpose`` (by default False)
        | * if it's False, result Matrix (4x4) will be:
        | [[1, 0, 0, 0],
        | [0, 1, 0, 0],
        | [0, 0, 1, 0],
        | [translation[0], translation[1], translation[2], 1]]
        | * if it's True, result Matrix (4x4) will be (just transpose it):
        | [[1, 0, 0, translation[0]],
        | [0, 1, 0, translation[1]],
        | [0, 0, 1, translation[2]],
        | [0, 0, 0, 1]]
        """
        self.change_data(
            matrix_4x4_from_translation(vector3, transpose=transpose))
