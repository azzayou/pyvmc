"""
Function for most Operation and Comparison between Vectors.
also for most Operation for Matrices and some collision detection.
also there are other math function (including ``math`` module its self)
for Backwork Compatibility.

Note: Quaternion order is (x, y, z, w).

Note: Euler angles Support Tait–Bryan Angles Only (no repeat axis)
and it's follow this order ``yaw`` and ``pitch`` and ``roll``.

Info: Vector is Sequence of Numbers (float or integer).

Info: Matrix is Sequence of Sequences of Numbers (float or integer).
Or in other Word Sequence of Vectors.

Info: ``yaw`` and ``pitch`` and ``roll`` is equivalent
to ``Heading`` and ``Attitude`` and ``Bank`` also equivalent
to ``α`` (φ) and ``β`` (θ) and ``γ`` (ψ) . (it's just different name :D).

RULE 0: All functions Must be documented (expect if it's self-explain).

RULE 1: All functions Must be in the `.pyi` file with type annotation support
Python 3.8+ for NOW. And the Functions itself Must support Python 2.7+ for NOW.

RULE 2: for function must start will name (or any similar names) of type/class
that will Return. (e.g. is_dummy_integer(dummy: Any) -> bool: ...).

RULE 3: ``Warning`` Then ``Note`` Then ``Info`` Then ``Examples``.

RULE 4: make functions independent and maintainable as possible.

RULE 5: check Must be between ``##### check`` and ``##### end check``.

RULE 6: Import Python Library Only and add comment for which function used.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#### Enable Feature Python
from __future__ import division

#### Import Python library
import math  # for: cos, acos, sin, asin, tan, atan2, copysign, isinf, isnan,
# ceil, floor
import sys  # for: version_info

if sys.version_info < (3, 3):
    from collections import Sequence, Iterable
else:  # collections.abc is added in Python 3.3
    # Info: https://docs.python.org/3/library/collections.abc.html
    from collections.abc import Sequence, Iterable

# no class.
# functions.

Numbers_Tuple = (float, int)
AnyIndex_Tuple = (int, slice)
EulerAnglesOrders = ["XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"]

## ``EM`` stand for ``Error Message``
EM_UNSUPPORTED_ORDER_EULER = ("Unsupported rotation order `%s`." + (
        " Choose from %s." % str(EulerAnglesOrders)))
EM_WRONG_TYPE_FOR_INDEX = "Unsupported type %s of `%s` while index `%s`"
EM_WRONG_VECTOR_LENGTH = "Expect length of value be %i, got: %i `%s`"
EM_WRONG_MATRIX_SIZE = "Expect size of value be (%i x %i), got: (%i x %i) `%s`"
EM_NOT_SQUARE_MATRIX = "Expect square of matrix NxN, got: (%ix%i) `%s`"
EM_NOT_TUPLE_INDEX = ("Expect tuple of 2 index (integers or/and slices),"
                      " got: `%s`")
EM_NOT_EXPECTED = "Expect %s, got: `%s`"
EM_WRONG_LENGTH = "Expect length be %i, got: %i `%s`"
EM_NOT_ALL_LENGTH_RIGHT = "Expect all length be %i, but some of it got: %i `%s`"
EM_ZERO_DIVISION = "Division By Zero"
EM_ZERO_MOD = "Modulo By Zero"
# EM_ZERO_POW_ZERO = "Undefined Zero Power of Zero"  # not used

e = 2.718281828459045
pi = 3.141592653589793
tau = 6.283185307179586
epsilon = 1e-15
inf = float('inf')
nan = float('nan')


############################ Backwork Compatibility ############################
if sys.version_info < (3, 5):  # `math.isclose` is added in Python 3.5
    # Info: https://docs.python.org/3/library/math.html#math.isclose
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        """Determine whether two floating-point numbers are close in value.
        Return True if ``a`` is close in value to ``b``, and False otherwise.

        ``rel_tol`` : maximum difference for being considered "close",
        relative to the magnitude of the input values.

        ``abs_tol`` : maximum difference for being considered "close",
        regardless of the magnitude of the input values.

        For the values to be considered close, the difference between them
        must be smaller than at least one of the tolerances.
        -inf, inf and NaN behave similarly to the IEEE 754 Standard.
        That is, NaN is not close to anything, even itself.
        inf and -inf are only close to themselves.

        Info: added for backwork compatibility and for PEP 485.
        """
        if math.isnan(a) or math.isnan(b):
            return False
        if math.isinf(a) and math.isinf(b):
            return a == b  # True only if both inf or -inf
        ##
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
else:
    isclose = math.isclose


if sys.version_info < (3, 2):  # `erf`, `erfc`, `gamma` add in Python 3.2
    # Info: https://docs.python.org/3/library/math.html#math.erf
    def erf(x):
        """Return the error function at x.

        Info: added for backwork compatibility.

        Info: https://www.johndcook.com/blog/python_erf

        Info: https://en.wikipedia.org/wiki/Error_function
        """
        # A&S 7.1.26 constants
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        t = 1 / (1 + p * abs(x))
        y = ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * pow(e, -(x**2))
        if x >= 0:
            return 1.0 - y
        else:
            return y - 1.0


    # Info: https://docs.python.org/3/library/math.html#math.erfc
    def erfc(x):
        """Return Complementary error function at x.

        Info: added for backwork compatibility.

        Info: https://en.wikipedia.org/wiki/Error_function#Complementary_error_function
        """
        return 1 - erf(x)


    __GAMMA = [1.00000000000000000000, 0.57721566490153286061,
               -0.65587807152025388108, -0.04200263503409523553,
               0.16653861138229148950, -0.04219773455554433675,
               -0.00962197152787697356, 0.00721894324666309954,
               -0.00116516759185906511, -0.00021524167411495097,
               0.00012805028238811619, -0.00002013485478078824,
               -0.00000125049348214267, 0.00000113302723198170,
               -0.00000020563384169776, 0.00000000611609510448,
               0.00000000500200764447, -0.00000000118127457049,
               0.00000000010434267117, 0.00000000000778226344,
               -0.00000000000369680562, 0.00000000000051003703,
               -0.00000000000002058326, -0.00000000000000534812,
               0.00000000000000122678, -0.00000000000000011813,
               0.00000000000000000119, 0.00000000000000000141,
               -0.00000000000000000023, 0.00000000000000000002]


    # Info: https://docs.python.org/3/library/math.html#math.gamma
    def gamma(x):
        """Return Gamma function at x.

        Info: added for backwork compatibility.

        Info: https://rosettacode.org/wiki/Gamma_function#Python

        Info: https://en.wikipedia.org/wiki/Gamma_function
        """
        y  = float(x) - 1.0
        sm = __GAMMA[-1]
        for an in __GAMMA[-2::-1]:
          sm = (sm * y) + an
        return 1.0 / sm
else:
    erf = math.erf
    erfc = math.erfc
    gamma = math.gamma


############################## Important Function ##############################
def xor(a, b):
    """``a`` XOR ``b`` is equivalent to: ((not a) and not b) or (a and b)."""
    return ((not a) and not b) or (a and b)


def degrees(x):
    """Convert angle ``x`` from radians to degrees."""
    return x * 57.295779513082321  # this's accurate value of (180/pi)


def radians(x):
    """Convert angle ``x`` from degrees to radians."""
    return x * (1.745329251994329 * 0.01)  # this's accurate value of (pi/180)


def clamp(value, max_value, min_value):
    """Clamp any value (float or integer) between maximal and minimal."""
    return max(min_value, min(value, max_value))


def lerp(a, b, factor):
    """Return calculation of linear interpolation a value between two values
     ``a`` and ``b`` based on a specific ``factor``.
    """
    return a + (factor * (b - a))


def inv_lerp(a, b, factor):
    """Return calculation of inverse linear interpolation a value between two
     values ``a`` and ``b`` based on a specific ``factor``.

    Warning: Be Careful about ZeroDivision (in case ``a`` is Equal To ``b``).
    """
    return (factor - a) / (b - a)


def remap(value, from_range, to_range):
    """Remap a value from range to another range.

    Warning: ``value`` Must be in the range ``form_range``, also ``form_range``
     and ``to_range`` Must be any Vector2 (min, max).
     Or it will raise ValueError.

    Examples:

    >>> value1 = 10
    >>> range1 = [0, 100]
    >>> range2 = [0, pi]
    >>> print(remap(value1, range1, range2))
    0.3141592653589793
    >>> value2 = -50
    >>> range3 = (-100, 100)  # work with any Sequence of Numbers :D
    >>> range4 = [0, 100]
    >>> print(remap(value2, range3, range4))
    25.0
    >>> try:
    ...     print(remap(value2, range1, range2))
    ... except ValueError as error:
    ...     print(error)
    Value `-50` is Out of Range between [0, 100]
    >>> try:
    ...     not_valid_range = [100, -100]
    ...     print(remap(0, not_valid_range, range1))
    ... except ValueError as error:
    ...     print(error)
    Invalid range `[100, -100]`
    """
    x_min, x_max = from_range[0], from_range[1]
    y_min, y_max = to_range[0], to_range[1]
    ##### check
    if x_min > x_max:
        raise ValueError("Invalid range `%s`" % from_range)
    if y_min > y_max:
        raise ValueError("Invalid range `%s`" % to_range)
    if not (x_min <= value <= x_max):
        raise ValueError(
            "Value `%s` is Out of Range between %s" % (value, str(from_range)))
    ##### end check
    x_ratio = 1 / (x_max - x_min)
    return y_min + ((y_max - y_min) * x_ratio * (value - x_min))


def all_map(func, *iterables):
    """Make an iterator that computes the function using arguments from an
     iterable. Return True if All elements of the iterable (result after
     computes) are true (or if the iterable is empty). otherwise False.
    """
    return all(map(func, *iterables))


def any_map(func, *iterables):
    """Make an iterator that computes the function using arguments from an
     iterable. Return True if Any elements of the iterable (result after
     computes) are true. otherwise False (or if the iterable is empty).
    """
    return any(map(func, *iterables))


def list_map(func, *iterables):
    """Make a List that computes the function using arguments from an
     iterable.
    """
    return list(map(func, *iterables))


def tuple_map(func, *iterables):
    """Make a Tuple that computes the function using arguments from an
     iterable.
    """
    return tuple(map(func, *iterables))


def max_map(func, *iterables):
    """Return Maximal Value of an iterator that computes the function using
     arguments from an iterable.
    """
    return max(map(func, *iterables))


def min_map(func, *iterables):
    """Return Minimal Value of an iterator that computes the function using
     arguments from an iterable.
    """
    return min(map(func, *iterables))


def sum_map(func, *iterables):
    """Return Sum of iterator that computes the function using arguments from
     an iterable.
    """
    return sum(map(func, *iterables))


def merge_iterables(*iterables):
    """Return Merged iterables in order as a List."""
    return [x for iterable in iterables for x in iterable]


def merge_from_same_index(sequences, index):
    """Return Iterator of all value from Sequences in same index."""
    return map(lambda sequence: sequence[index], sequences)


def sub_values(iterable):
    """Subtract all numbers inside an iterable."""
    func_sub = lambda index, x: -x if index == 0 else x
    return sum(map(lambda index_x: func_sub(index_x[0], index_x[1]),
                   enumerate(iterable)))


def mul_values(iterable):
    """Multiply all numbers inside an iterable."""
    result = 1
    for number in iterable:
        result *= number
    return result


def int_from_str_or_bytes(str_or_bytes, base):
    """Convert string/bytes to integer.

    Warning: ``str_or_bytes`` if it's Unicode string. it will raise ValueError.

    Examples:

    >>> int_from_str_or_bytes("0xff", base=16)
    255
    >>> int_from_str_or_bytes("ff", base=16)
    255
    >>> try:
    ...     int_from_str_or_bytes("\xff", base=16)  # BAD it's Unicode
    ... except ValueError as error:
    ...     print(error)
    invalid literal for int() with base 16: 'ÿ'
    >>> int_from_str_or_bytes("0o77", base=8)
    63
    >>> int_from_str_or_bytes("77", base=8)
    63
    >>> int_from_str_or_bytes("0b01011", base=2)
    11
    >>> int_from_str_or_bytes("1011", base=2)
    11
    >>> int_from_str_or_bytes(b"0xff", base=16)
    255
    >>> int_from_str_or_bytes(b"ff", base=16)
    255
    >>> # int_from_str_or_bytes(b"\xff", base=16)  # output: 255
    >>> int_from_str_or_bytes(b"0o77", base=8)
    63
    >>> int_from_str_or_bytes(b"77", base=8)
    63
    >>> int_from_str_or_bytes(b"0b01011", base=2)
    11
    >>> int_from_str_or_bytes(b"1011", base=2)
    11
    """
    if str_or_bytes.isalnum():  # for str/bytes like: "0xff", "ff", "0o70"
        return int(str_or_bytes, base=base)
    else:  # hex code like: "\x0f" or b"\x0f"
        if sys.version_info <= (2, 7):
            # In Python 2 (both of `bytes` and `str` are same class/type)
            return int(str_or_bytes.encode("hex"), base=base)
        else:
            if isinstance(str_or_bytes, str):  # TODO find way to get hex code
                message = ("bytes of hex code" + (
                        " Or str/bytes of number base %i" % base))
                raise ValueError(EM_NOT_EXPECTED % (message, str_or_bytes))
            else:  # hex code bytes like: b"\x0f"
                hex_code = "%02x" % str_or_bytes[0]
                return int(hex_code, base=base)


################################ Check Functions ###############################
def is_same_sign(a, b, *c):
    """Return True if all values of ``a`` and ``b`` etc... have same sign.
     Otherwise, Return False.

    Note: Zero (0) is neither a positive nor a negative number.

    Info: have same sign means both are negative Or positive.

    Examples:

    >>> a1 = 10
    >>> b1 = -10
    >>> is_same_sign(a1, b1)
    False
    >>> a2 = 5
    >>> b2 = 1
    >>> is_same_sign(a2, b2)
    True
    >>> a3 = -0.2
    >>> b3 = -1
    >>> is_same_sign(a3, b3)
    True
    >>> a3 = -0
    >>> b3 = 0
    >>> is_same_sign(a3, b3)  # because 0 is Equal To -0
    True
    >>> a4 = -1
    >>> b4 = -1000
    >>> c4 = -9
    >>> is_same_sign(a4, b4, c4)  # you can check for multiple values at once
    True
    >>> a5 = -0
    >>> b5 = 0
    >>> c5 = 0
    >>> is_same_sign(a5, b5, c5)  # Don't forget 0 is Equal To -0
    True
    >>> a6 = 10
    >>> b6 = 1.02
    >>> c6 = 0
    >>> is_same_sign(a6, b6, c6)  # Zero is NOT positive nor a negative number
    False
    """
    if c:
        is_pos = all(map(lambda x: x > 0, c))
        is_neg = all(map(lambda x: x < 0, c))
        is_eq = all(map(lambda x: (a == b == x), c))
    else:
        is_pos = is_neg = is_eq = True
    ##
    if a == b and is_eq:  # in case of zero Or all has same value
        return True
    elif ((a > 0) and (b > 0) and is_pos) or (a < 0 and b < 0 and is_neg):
        return True
    else:
        return False


def is_sequence(obj):
    """Return True if object is instance of Sequence And NOT (str Or bytes Or
     bytearray). Otherwise, Return False.
    """
    not_wanted = (str, bytes, bytearray)
    return isinstance(obj, Sequence) and not isinstance(obj, not_wanted)


def is_has_only(iterable, expect_value, use_is=False):
    """Return True if Iterable has Only the expected value.
     Otherwise, Return False.

    Note: ``use_is`` (by default is False).
    | * if it's True. function will use `is` for checking if All values are
    | expected values.
    | * if it's False. the functions will use `==` for checking if All values
    | are expected values.
    """
    if use_is:
        func_check = lambda item: item is expect_value
    else:
        func_check = lambda item: item == expect_value
    return all(map(func_check, iterable))


def is_contain_only(iterable, expect_types, use_issubclass=False):
    """Return True if Iterable contain Only at least one of the expected types.
     Otherwise, Return False.

    Note: ``use_is`` (by default is False).
    | * if it's True. function will use `issubclass` for checking if All values
    | types are at least one of the expected types.
    | * if it's False. the functions will use `isinstance` for checking if All
    | values at least instance one of the expected types.
    """
    if use_issubclass:
        func_check = lambda item: issubclass(type(item), expect_types)
    else:
        func_check = lambda item: isinstance(item, expect_types)
    return all(map(func_check, iterable))


def is_number(obj, not_nan=False, not_inf=False):
    """Return True if the object is a Number (float or integer).
     Otherwise, Return False.

    Note: ``not_nan`` (by default False)
    | * if it's True. function will NOT count ``float("nan")`` as a Number.
    | * if it's False. function will count ``float("nan")`` as a Number.

    Note: ``not_inf`` (by default False)
    | * if it's True. function will NOT count ``float("inf")`` as a Number.
    | * if it's False. function will count ``float("inf")`` as a Number.

    Examples:

    >>> NaN = float("nan")
    >>> Inf = float("inf")
    >>> is_number("ARE YOU SERIOUS THIS IS NOT A NUMBER >:C !")
    False
    >>> is_number(1)
    True
    >>> is_number(1.1)
    True
    >>> is_number(NaN)
    True
    >>> is_number(-NaN)
    True
    >>> is_number(NaN, not_nan=True)
    False
    >>> is_number(-NaN, not_nan=True)
    False
    >>> is_number(NaN, not_inf=True)
    True
    >>> is_number(-NaN, not_nan=True, not_inf=True)
    False
    >>> is_number(Inf)
    True
    >>> is_number(-Inf)
    True
    >>> is_number(Inf, not_inf=True)
    False
    >>> is_number(-Inf, not_inf=True)
    False
    >>> is_number(Inf, not_nan=True)
    True
    >>> is_number(Inf, not_nan=True, not_inf=True)
    False
    """
    is_if_nan = not_nan and math.isnan(obj)
    is_if_inf = not_inf and math.isinf(obj)
    return isinstance(obj, Numbers_Tuple) and not (is_if_nan or is_if_inf)


def is_all_numbers(iterable, not_nan=False, not_inf=False):
    """Return True if Iterable Not contain Only Numbers (float or integer).
     Otherwise, Return False.

    Note: ``not_nan`` (by default False)
    | * if it's True. function will NOT count ``float("nan")`` as a Number.
    | * if it's False. function will count ``float("nan")`` as a Number.

    Note: ``not_inf`` (by default False)
    | * if it's True. function will NOT count ``float("inf")`` as a Number.
    | * if it's False. function will count ``float("inf")`` as a Number.

    Examples:

    >>> not_all_numbers = [1, 2, 3, "F+"]  # someone failed on exam :C
    >>> print(is_all_numbers(not_all_numbers))
    False
    >>> all_numbers = [1.1, 2, 3000, float("inf"), float("nan"), 6, 7, 8, 9]
    >>> print(is_all_numbers(all_numbers))
    True
    >>> print(is_all_numbers(all_numbers, not_nan=True))
    False
    >>> print(is_all_numbers(all_numbers, not_inf=True))
    False
    """
    func_check = lambda obj: is_number(obj, not_nan=not_nan, not_inf=not_inf)
    return all(map(func_check, iterable))


def is_all_same_length(sequence_of_sized, specific_length=None):
    """Return True if all Sized object have same length (Or Equal to specific
     length if specified). Otherwise, Return False.

    Note: ``specific_length`` (by default None)
    | * if it's None Or not specified. it will check if all have same length.
    | * if it's specified. it will check if all have length equal to
    | ``specific_length``.
    """
    if specific_length is None:
        func_check_length = lambda obj: len(obj) == len(sequence_of_sized[0])
    else:
        func_check_length = lambda obj: len(obj) == specific_length
    return all(map(func_check_length, sequence_of_sized))


def is_vector(obj, specific_length=None):
    """Return True if object is Vector. Otherwise, Return False.

    Note: ``specific_length`` (by default None)
    | * if it's None Or not specified. it will just check if it's valid Vector.
    | * if it's specified. it will check if length of Vector is equal to
    | ``specific_length``.

    Info: `Vector` is Sequence of Numbers (float or integer).

    Examples:

    >>> vector1 = (1, 2, 3, 4)
    >>> is_vector(vector1)
    True
    >>> is_vector(vector1, specific_length=3)  # you want to be specific length
    False
    >>> vector2 = [1, 2, 3]  # any Sequence of Number is Vector
    >>> is_vector(vector2)
    True
    >>> is_vector(vector2, specific_length=3)
    True
    >>> class CustomSequence(Sequence):
    ...     def __init__(self, *numbers, **kwargs):
    ...         self._data = list(numbers)
    ...     def __len__(self):
    ...         return len(self._data)
    ...     def __getitem__(self, index):
    ...         return self._data[index]
    ...     def __setitem__(self, key, value):
    ...         self._data[key] = value
    >>> vector3 = CustomSequence(1,2,3,4)
    >>> is_vector(vector3)  # work with any Sequence of Numbers
    True
    >>> is_vector(vector3, specific_length=100)  # :| seriously ?
    False
    >>> vector4 = range(10)
    >>> is_vector(vector4)  # range also are Sequence
    True
    >>> not_vector = map(lambda x: x**2, range(100))  # event it has only number
    >>> ## this based on Python version if Python 2 ``map`` is return list
    >>> # if Python 3 ``map`` return instance of ``map`` class/type
    >>> # and this ``map`` IS NOT SEQUENCE.
    >>> is_vector(not_vector)
    False
    >>> NOT_VECTOR = "12344"  # ARE YOU KIDDING MEE !!?!
    >>> is_vector(NOT_VECTOR)
    False
    >>> is_vector(NOT_VECTOR, specific_length=1)
    False
    """
    if is_sequence(obj):
        if specific_length:
            return is_all_numbers(obj) and (len(obj) == specific_length)
        else:
            return is_all_numbers(obj)
    else:  # for any other type/class
        return False


def is_matrix(obj, specific_rows=None, specific_columns=None):
    """Return True if object is Matrix. Otherwise, Return False.

    Warning: this is heavy function Don't use it A LOT !!!

    Note: ``specific_rows`` (by default None)
    | * if it's None Or not specified. it will just check if it's valid Matrix.
    | * if it's specified. it will check if number Rows of Matrix is equal to
    | ``specific_rows``.

    Note: ``specific_columns`` (by default None)
    | * if it's None Or not specified. it will just check if it's valid Matrix.
    | * if it's specified. it will check if number Columns of Matrix is equal to
    | ``specific_columns``.

    Info: `Matrix` is Sequence of Sequences of Numbers (float or integer)
     In other word Sequence of Vectors (all have of same length).

    Examples:

    >>> not_matrix1 = [[1,2,3], [1,2], [1,2,3]]  #all rows Must have same length
    >>> not_matrix2 = [[1,], [1,], [1,2]]  #all rows Must have same length
    >>> matrix1 = [[1,2,3], [1,2,3], [1,2,3]]
    >>> matrix2 = [[1,], [1,], [1,]]
    >>> print(is_matrix(not_matrix1))
    False
    >>> print(is_matrix(matrix1))
    True
    >>> print(is_matrix(not_matrix2))
    False
    >>> print(is_matrix(matrix2))
    True
    >>> matrix3 = [[1,2,3,4], [1,2,3,4], [1,2,3,4]]  # it has 3 rows, 4 columns
    >>> print(is_matrix(matrix3, specific_rows=3))
    True
    >>> print(is_matrix(matrix3, specific_rows=4))
    False
    >>> print(is_matrix(matrix3, specific_columns=4))
    True
    >>> print(is_matrix(matrix3, specific_columns=3))
    False
    >>> print(is_matrix(matrix3, specific_rows=3, specific_columns=4))
    True
    >>> print(is_matrix(matrix3, specific_rows=3, specific_columns=3))
    False
    """
    if is_sequence(obj):
        if specific_rows:
            is_same_num_rows = (len(obj) == specific_rows)
        else:
            is_same_num_rows = True
        if specific_columns:
            is_same_num_columns = all(
                map(lambda v: is_vector(v, specific_length=specific_columns),
                    obj))
        else:
            is_same_num_columns = all(
                map(lambda v: is_vector(v, specific_length=len(obj[0])), obj))
        return is_same_num_rows and is_same_num_columns
    else:  # for any other type/class
        return False


########################## Simple Operation Functions ##########################
def vector_add_vectors(*any_vectors):
    """Addition between Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_add = (-7, 2)
    >>> v2_add = (10, -5)
    >>> v3_add = (-1, 7)
    >>> v4_add = (-26, 0)
    >>> v5_add = (50, -1)
    >>> result = vector_add_vectors(v1_add, v2_add, v3_add, v4_add, v5_add)
    >>> print(list(result))
    [26, 3]
    >>> try:
    ...     no_result = vector_add_vectors((1, 2), (1, 2, 3))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length >:C")
    Those Vectors Don't Have Same Length >:C
    """
    max_length = len(any_vectors[0])
    ##### check
    for length, vector in map(lambda v: (len(v), v), any_vectors):
        if max_length != length:
            raise IndexError(EM_NOT_ALL_LENGTH_RIGHT % (
                max_length, length, str(vector)))
    ##### end check
    return map(lambda index: sum(map(lambda v: v[index], any_vectors)),
               range(max_length))


def vector_add_values(any_vector, values):
    """Addition between a Vector and values.

    Examples:

    >>> v1_add = (-7, 2)
    >>> values_add = [10, 7, -26]
    >>> result1 = vector_add_values(v1_add, values_add)
    >>> print(list(result1))
    [-16, -7]
    >>> result2 = vector_add_values(v1_add, 10)
    >>> print(list(result2))
    [3, 12]
    """
    if isinstance(values, Iterable):
        return map(lambda x: x + sum(values), any_vector)
    return map(lambda x: x + values, any_vector)


def vector_sub_vectors(*any_vectors):
    """Subtract between Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_sub = (-7, 2)
    >>> v2_sub = (10, -5)
    >>> v3_sub = (-1, 7)
    >>> v4_sub = (-26, 0)
    >>> v5_sub = (50, -1)
    >>> result1 = vector_sub_vectors(v1_sub, v2_sub, v3_sub, v4_sub, v5_sub)
    >>> print(list(result1))
    [-40, 1]
    >>> try:
    ...     print(vector_sub_vectors((1, 2), (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length.")
    Those Vectors Don't Have Same Length.
    """
    max_length = len(any_vectors[0])
    ##### check
    for length, vector in map(lambda v: (len(v), v), any_vectors):
        if max_length != length:
            raise IndexError(
                EM_NOT_ALL_LENGTH_RIGHT % (max_length, length, str(vector)))
    ##### end check
    func_sub = lambda index: any_vectors[0][index] - sum(
        map(lambda v: v[index], any_vectors[1:]))
    return map(func_sub, range(max_length))


def vector_sub_values(any_vector, values, reverse=False):
    """Subtract between a Vector and sequence of Numbers (float or integer).

    Note: ``reverse`` (by default False)
    | * if it's False the operation order will be (vector - values).
    | * if it's True the operation order will be (values - vector).

    Examples:

    >>> v1_sub = (-7, 2)
    >>> values_sub = [5, -17, 25]
    >>> result1 = vector_sub_values(v1_sub, values_sub)
    >>> print(list(result1))
    [-20, -11]
    >>> result2 = vector_sub_values(v1_sub, values_sub, reverse=True)
    >>> print(list(result2))
    [4, -5]
    >>> result3 = vector_sub_values(v1_sub, 5)
    >>> print(list(result3))
    [-12, -3]
    >>> result4 = vector_sub_values(v1_sub, 5, reverse=True)
    >>> print(list(result4))
    [12, 3]
    """
    if reverse:
        if isinstance(values, Iterable):
            func_sub = lambda index, x: -x if index != 0 else x
            value = sum(map(lambda index_x: func_sub(index_x[0], index_x[1]),
                            enumerate(values)))
            return map(lambda x: value - x, any_vector)
        return map(lambda x: values - x, any_vector)
    else:
        if isinstance(values, Iterable):
            return map(lambda x: x - sum(values), any_vector)
        return map(lambda x: x - values, any_vector)


def vector_mul_vectors(*any_vectors):
    """Multiplication between Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_mul = (-7, 2)
    >>> v2_mul = (10, -5)
    >>> v3_mul = (-1, 7)
    >>> v4_mul = (-26, 0)
    >>> v5_mul = (50, -1)
    >>> result1 = vector_mul_vectors(v1_mul, v2_mul, v3_mul, v4_mul, v5_mul)
    >>> print(list(result1))
    [-91000, 0]
    >>> try:
    ...     print(vector_mul_vectors(v1_mul, (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length.")
    Those Vectors Don't Have Same Length.
    """
    max_length = len(any_vectors[0])
    ##### check
    for length, vector in map(lambda v: (len(v), v), any_vectors):
        if max_length != length:
            raise IndexError(EM_NOT_ALL_LENGTH_RIGHT % (
                max_length, length, str(vector)))

    ##### end check
    def multi_vs(index):
        """Return result of Multiplication values from vectors in same index."""
        result = 1
        for v in any_vectors:
            result *= v[index]
        return result

    return map(multi_vs, range(max_length))


def vector_mul_values(any_vector, values):
    """Multiplication between Vector and sequence of Numbers (float or integer).

    Examples:

    >>> v1_mul = (-7, 2)
    >>> values_mul = [-5, 7, -26]
    >>> result1 = vector_mul_values(v1_mul, values_mul)
    >>> print(list(result1))
    [-6370, 1820]
    >>> result2 = vector_mul_values(v1_mul, -5)
    >>> print(list(result2))
    [35, -10]
    """
    if isinstance(values, Iterable):
        value = 1
        for n in values:
            value *= n
        return map(lambda x: x * value, any_vector)
    else:
        return map(lambda x: x * values, any_vector)


def vector_truediv_vector(v1, v2):
    """True Division between Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_div = (-1, 7)
    >>> v2_div = (-26, 0)
    >>> try:
    ...     print(vector_truediv_vector(v1_div, v2_div))
    ... except ZeroDivisionError:
    ...     print("division by zero")
    division by zero
    >>> v1_div = (-7, 2)
    >>> v2_div = (10, -5)
    >>> result1 = vector_truediv_vector(v1_div, v2_div)
    >>> print(list(result1))
    [-0.7, -0.4]
    >>> try:
    ...     print(vector_truediv_vector(v1_div, (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length.")
    Those Vectors Don't Have Same Length.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    if any(map(lambda i: i == 0, v2)):
        raise ZeroDivisionError(EM_ZERO_DIVISION)
    ##### end check
    func_truediv = lambda x1, x2: x1 / x2
    return map(func_truediv, v1, v2)


def vector_truediv_value(any_vector, value, reverse=False):
    """True Division between a Vector and a Number (float or integer).

    Note: ``reverse`` (by default False)
    | * if it's False the operation order will be (vector / value).
    | * if it's True the operation order will be (value / vector).

    Examples:

    >>> v1_div = (-7, 2)
    >>> value1_div = -3
    >>> result1 = vector_truediv_value(v1_div, value1_div)
    >>> print(list(result1))
    [2.3333333333333335, -0.6666666666666666]
    >>> result2 = vector_truediv_value(v1_div, value1_div, reverse=True)
    >>> print(list(result2))
    [0.42857142857142855, -1.5]
    """
    if reverse:
        ##### check
        if any(map(lambda i: i == 0, any_vector)):
            raise ZeroDivisionError(EM_ZERO_DIVISION)
        ##### end check
        return map(lambda x: value / x, any_vector)
    else:
        ##### check
        if value == 0:
            raise ZeroDivisionError(EM_ZERO_DIVISION)
        ##### end check
        return map(lambda x: x / value, any_vector)


def vector_floordiv_vector(v1, v2):
    """Floor Division between Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_div = (-1, 7)
    >>> v2_div = (-26, 0)
    >>> try:
    ...     print(vector_truediv_vector(v1_div, v2_div))
    ... except ZeroDivisionError:
    ...     print("division by zero")
    division by zero
    >>> v1_div = (-7, 2)
    >>> v2_div = (10, -5)
    >>> result1 = vector_floordiv_vector(v1_div, v2_div)
    >>> print(list(result1))
    [-1, -1]
    >>> try:
    ...     print(vector_floordiv_vector(v1_div, (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length. Please Stop do this:C")
    Those Vectors Don't Have Same Length. Please Stop do this:C
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    if any(map(lambda i: i == 0, v2)):
        raise ZeroDivisionError(EM_ZERO_DIVISION)
    ##### end check
    func_floordiv = lambda x1, x2: x1 // x2
    return map(func_floordiv, v1, v2)


def vector_floordiv_value(any_vector, value, reverse=False):
    """Floor Division between a Vector and a Number (float or integer).

    Note: ``reverse`` (by default False)
    | * if it's False the operation order will be (vector // value).
    | * if it's True the operation order will be (value // vector).

    Examples:

    >>> v1_div = (-7, 2)
    >>> value1_div = -1
    >>> result1 = vector_floordiv_value(v1_div, value1_div)
    >>> print(list(result1))
    [7, -2]
    >>> result2 = vector_floordiv_value(v1_div, value1_div, reverse=True)
    >>> print(list(result2))
    [0, -1]
    """
    if reverse:
        ##### check
        if any(map(lambda i: i == 0, any_vector)):
            raise ZeroDivisionError(EM_ZERO_DIVISION)
        ##### end check
        return map(lambda x: value // x, any_vector)
    else:
        ##### check
        if value == 0:
            raise ZeroDivisionError(EM_ZERO_DIVISION)
        ##### end check
        return map(lambda x: x // value, any_vector)


def vector_mod_vector(v1, v2):
    """Mod between 2 Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_mod = (190.7, 193)
    >>> v2_mod = (0.25, 4)
    >>> result1 = vector_mod_vector(v1_mod, v2_mod)
    >>> print(list(result1))
    [0.19999999999998863, 1]
    >>> try:
    ...     print(vector_mod_vector(v1_mod, (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length.")
    Those Vectors Don't Have Same Length.
    >>> try:
    ...     print(vector_mod_vector(v1_mod, (0, 1)))
    ... except ZeroDivisionError:
    ...     print("NO ZERO MOD >:C.")
    NO ZERO MOD >:C.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    if any(map(lambda i: i == 0, v2)):
        raise ZeroDivisionError(EM_ZERO_MOD)
    ##### end check
    func_mod = lambda x1, x2: x1 % x2
    return map(func_mod, v1, v2)


def vector_mod_value(any_vector, value, reverse=False):
    """Mod between a Vectors and a Number (float or integer).

    Note: ``reverse`` (by default False)
    | * if it's False the operation order will be (vector % value).
    | * if it's True the operation order will be (value % vector).

    Examples:

    >>> vector1 = (-7, 2)
    >>> value1 = -5
    >>> result1 = vector_mod_value(vector1, value1)
    >>> print(list(result1))
    [-2, -3]
    >>> result2 = vector_mod_value(vector1, value1, reverse=True)
    >>> print(list(result2))
    [-5, 1]
    """
    if reverse:
        ##### check
        if any(map(lambda i: i == 0, any_vector)):
            raise ZeroDivisionError(EM_ZERO_MOD)
        ##### end check
        return map(lambda x: value % x, any_vector)
    else:
        ##### check
        if value == 0:
            raise ZeroDivisionError(EM_ZERO_MOD)
        ##### end check
        return map(lambda x: x % value, any_vector)


def vector_pow_vector(v1, v2, mod=None):
    """Power (using pow) between 2 Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Note: ``mod`` is same as parameter `mod` from builtins function ``pow``.

    Examples:

    >>> v1_pow = (7, 9)
    >>> v2_pow = (0.25, 3)
    >>> result1 = vector_pow_vector(v1_pow, v2_pow)
    >>> print(list(result1))
    [1.6265765616977856, 729]
    >>> try:
    ...     print(vector_pow_vector(v1_pow, (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length.")
    Those Vectors Don't Have Same Length.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    func_pow = lambda x1, x2: pow(x1, x2, mod=mod)
    return map(func_pow, v1, v2)


def vector_pow_value(any_vector, value, mod=None, reverse=False):
    """Power (using pow) between a Vector and a Number (float or integer).

    Note: ``mod`` is same as parameter `mod` from builtins function ``pow``.

    Note: ``reverse`` (by default False)
    | * if it's False the operation order will be (vector ** value).
    | * if it's True the operation order will be (value ** vector).

    Examples:

    >>> vector1 = (3, 2)
    >>> value1 = 5
    >>> result1 = vector_pow_value(vector1, value1)
    >>> print(list(result1))
    [243, 32]
    >>> result2 = vector_pow_value(vector1, value1, reverse=True)
    >>> print(list(result2))
    [125, 25]
    """
    if reverse:
        return map(lambda x: pow(value, x, mod=mod), any_vector)
    return map(lambda x: pow(x, value, mod=mod), any_vector)


def vector_divmod_vector(v1, v2):
    """Divmod(floor division, mod) between 2 Vectors (Must have same length).

    Warning: in case vector doesn't have same length. it will raise IndexError.

    Examples:

    >>> v1_divmod = (7, 9)
    >>> v2_divmod = (0.25, 3)
    >>> result1 = vector_divmod_vector(v1_divmod, v2_divmod)
    >>> print(list(result1))
    [(28.0, 0.0), (3, 0)]
    >>> try:
    ...     print(vector_divmod_vector(v1_divmod, (1, 2, 3)))
    ... except IndexError:
    ...     print("Those Vectors Don't Have Same Length.")
    Those Vectors Don't Have Same Length.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return map(divmod, v1, v2)


def vector_divmod_value(any_vector, value, reverse=False):
    """Divmod(floor division, mod) between Vector and Number (float or integer).

    Note: ``reverse`` (by default False)
    | * if it's False the operation order will be divmod(vector, value).
    | * if it's True the operation order will be divmod(value, vector).

    Examples:

    >>> vector1 = (30, 42)
    >>> value1 = 5
    >>> result1 = vector_divmod_value(vector1, value1)
    >>> print(list(result1))
    [(6, 0), (8, 2)]
    >>> result2 = vector_divmod_value(vector1, value1, reverse=True)
    >>> print(list(result2))
    [(0, 5), (0, 5)]
    """
    if reverse:
        return map(lambda x: divmod(value, x), any_vector)
    else:
        return map(lambda x: divmod(x, value), any_vector)


########################## Simple Comparison Functions #########################
def is_vector_lt_vector(v1, v2):
    """Return True if All values in First Vector Lest Than Second Vector.
     Otherwise, Return False.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return all(map(lambda x1, x2: x1 < x2, v1, v2))


def is_vector_le_vector(v1, v2):
    """Return True if All values in First Vector Lest Than Or Equal To
     Second Vector. Otherwise, Return False.

    Warning: in case vector doesn't have same length. it will raise IndexError.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return all(map(lambda x1, x2: x1 <= x2, v1, v2))


def is_vector_eq_vector(v1, v2):
    """Return True if All values in First Vector Equal To Second Vector.
     Otherwise, Return False.

    Warning: in case vector doesn't have same length. it will raise IndexError.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return all(map(lambda x1, x2: x1 == x2, v1, v2))


def is_vector_ne_vector(v1, v2):
    """Return True if All values in First Vector Not Equal To Second Vector.
     Otherwise, Return False.

    Warning: in case vector doesn't have same length. it will raise IndexError.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return all(map(lambda x1, x2: x1 != x2, v1, v2))


def is_vector_gt_vector(v1, v2):
    """Return True if All values in First Vector Greater Than Second Vector.
     Otherwise, Return False.

    Warning: in case vector doesn't have same length. it will raise IndexError.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return all(map(lambda x1, x2: x1 > x2, v1, v2))


def is_vector_ge_vector(v1, v2):
    """Return True if All values in First Vector Greater Than Or Equal To
     Second Vector. Otherwise, Return False.

    Warning: in case vector doesn't have same length. it will raise IndexError.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    return all(map(lambda x1, x2: x1 >= x2, v1, v2))


############# Comparison With Value
def is_vector_lt_value(any_vector, value):
    """Return True if all value of vector are Less Than specific Number.
     Otherwise, Return False
    """
    return all(map(lambda x: x < value, any_vector))


def is_vector_le_value(any_vector, value):
    """Return True if all value of vector are Less Than Or Equal To a Number.
     Otherwise, Return False.
    """
    return all(map(lambda x: x <= value, any_vector))


def is_vector_eq_value(any_vector, value):
    """Return True if all value of vector are Equal To specific Number.
     Otherwise, Return False.
    """
    return all(map(lambda x: x == value, any_vector))


def is_vector_ne_value(any_vector, value):
    """Return True if all value of vector are Not Equal To specific Number.
     Otherwise, Return False.
    """
    return all(map(lambda x: x != value, any_vector))


def is_vector_gt_value(any_vector, value):
    """Return True if all value of vector are Greater Than specific Number.
     Otherwise, Return False.
    """
    return all(map(lambda x: x > value, any_vector))


def is_vector_ge_value(any_vector, value):
    """Return True if all value of vector are Greater Than Or Equal To a Number.
     Otherwise, Return False.
    """
    return all(map(lambda x: x >= value, any_vector))


############# Compare Vector with 0
def is_vector_negative_not_zero(any_vector):
    """Return True if all value of vector are Less Than 0.
     Otherwise, Return False
    """
    return all(map(lambda x: x < 0, any_vector))


def is_vector_negative(any_vector):
    """Return True if all value of vector are Less Than Or Equal To 0.
     Otherwise, Return False
    """
    return all(map(lambda x: x <= 0, any_vector))


def is_vector_eq_zero(any_vector):
    """Return True if All value of vector are Equal To 0.
     Otherwise, Return False.
    """
    return all(map(lambda x: x == 0, any_vector))


def is_vector_ne_zero(any_vector):
    """Return True if All value of vector are NOT Equal To 0.
     Otherwise, Return False.
    """
    return all(map(lambda x: x != 0, any_vector))


def is_vector_positive_not_zero(any_vector):
    """Return True if All value of vector are Greater Than 0.
     Otherwise, Return False.
    """
    return all(map(lambda x: x > 0, any_vector))


def is_vector_positive(any_vector):
    """Return True if All value of vector are Greater Than Or Equal To 0.
     Otherwise, Return False.
    """
    return all(map(lambda x: x >= 0, any_vector))


################## Vector isclose
def is_vector_close_vector(v1, v2, rel_tol=1e-09, abs_tol=0.0):
    """Return True if All value in First Vector are Close To Second Vector.
     Otherwise, Return False.

    Warning: in case vector doesn't have same length. it will raise IndexError.
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    func_isclose = lambda x1, x2: isclose(x1, x2, rel_tol=rel_tol,
                                          abs_tol=abs_tol)
    return all(map(func_isclose, v1, v2))


def is_vector_close_value(any_vector, value, rel_tol=1e-09, abs_tol=0.0):
    """Return True if All value of vector are Close To specific Number.
     Otherwise, Return False.
    """
    func_isclose = lambda x: isclose(x, value, rel_tol=rel_tol, abs_tol=abs_tol)
    return all(map(func_isclose, any_vector))


def is_vector_close_zero(any_vector):
    """Return True if All value of vector are Close To 0.
     Otherwise, Return False.
    """
    return all(map(lambda x: isclose(x, 0, abs_tol=epsilon), any_vector))


################## Vector is NaN or Inf
def is_vector_nan_or_inf(any_vector, is_any=False):
    """Return True if value of Vector is ``float("nan")`` (Not a Number) or
     ``float("inf)`` (Infinite). Otherwise, Return False.

    Note: ``is_any`` (by default False)
    | * if it's True. function will check for ANY value of Vector.
    | * if it's False. function will check for ALL value of Vector.
    """
    check = map(lambda x: math.isnan(x) or math.isinf(x), any_vector)
    if is_any:
        return any(check)
    return all(check)


is_vector_inf_or_nan = is_vector_nan_or_inf  # :D


def is_vector_nan(any_vector, is_any=False):
    """Return True if value of Vector is ``float("nan")`` (Not a Number).
     Otherwise, Return False.

    Note: ``is_any`` (by default False)
    | * if it's True. function will check for ANY value of Vector.
    | * if it's False. function will check for ALL value of Vector.
    """
    check = map(math.isnan, any_vector)
    if is_any:
        return any(check)
    return all(check)


def is_vector_inf(any_vector, is_any=False):
    """Return True if value of Vector is ``float("inf")`` (Infinite).
     Otherwise, Return False.

    Note: ``is_any`` (by default False)
    | * if it's True. function will check for ANY value of Vector.
    | * if it's False. function will check for ALL value of Vector.
    """
    check = map(math.isinf, any_vector)
    if is_any:
        return any(check)
    return all(check)


######################### Specific Operation Functions #########################
def dot_product_vectors(*any_vectors):
    """Return Dot Product between Vectors (Must have same length).

    Examples:

    >>> v1 = (7, 9)
    >>> v2 = (0.5, 2)
    >>> print(dot_product_vectors(v1, v2))
    21.5
    >>> v1 = [1, -90, 6]  # works with any Sequence
    >>> v2 = (10, 0.5, 7)
    >>> print(dot_product_vectors(v1, v2))
    7.0
    """

    def multi_vs(index):
        """Return result of Multiplication values from vectors in same index."""
        result = 1
        for v in any_vectors:
            result *= v[index]
        return result

    max_length = max(map(len, any_vectors))
    return sum(map(multi_vs, range(max_length)))


def distance_vectors_sq(from_v1, to_v2):
    """Give Square of distance Between 2 Vectors (Must have same length).

    Warning: in case Vectors don't have same length. it will raise IndexError.

    Examples:

    >>> v1_dist = (1, 70)
    >>> v2_dist = (-10, 5)
    >>> print(distance_vectors_sq(v1_dist, v2_dist))
    4346
    >>> v1_dist = [1, 20, 5]  # works with any Sequence
    >>> v2_dist = (0, -5, 10)
    >>> print(distance_vectors_sq(v1_dist, v2_dist))
    651
    """
    ##### check
    if len(from_v1) != len(to_v2):
        raise IndexError(
            EM_WRONG_LENGTH % (len(from_v1), len(to_v2), str(to_v2)))
    ##### end check
    func_distance_sq = lambda x1, x2: (x1 - x2) ** 2
    return sum(map(func_distance_sq, from_v1, to_v2))


def distance_vectors(from_v1, to_v2):
    """Give distance Between 2 Vectors (Must have same length).

    Examples:

    >>> v1_dist = (1, 70)
    >>> v2_dist = (-10, 5)
    >>> print(distance_vectors(v1_dist, v2_dist))
    65.92419889539804
    >>> v1_dist = [1, 20, 5]  # works with any Sequence
    >>> v2_dist = (0, -5, 10)
    >>> print(distance_vectors(v1_dist, v2_dist))
    25.514701644346147
    """
    ##### check
    if len(from_v1) != len(to_v2):
        raise IndexError(
            EM_WRONG_LENGTH % (len(from_v1), len(to_v2), str(to_v2)))
    ##### end check
    func_distance_sq = lambda x1, x2: (x1 - x2) ** 2
    return sum(map(func_distance_sq, from_v1, to_v2)) ** 0.5


def magnitude_vector_sq(any_vector):
    """Return Square of Euclidean norm (or magnitude) of Iterable of Numbers
     (float or integer).

    Examples:

    >>> v1 = (1, 70)
    >>> print(magnitude_vector_sq(v1))
    4901
    >>> v2 = [-10, 5, 2]
    >>> print(magnitude_vector_sq(v2))
    129
    >>> v3 = (0.2, 0.5)
    >>> result = magnitude_vector_sq(v3)  # float point :[
    >>> print(round(result, 15))
    0.29
    """
    return sum(map(lambda x: x ** 2, any_vector))


def magnitude_vector(any_vector):
    """Return Euclidean norm (or magnitude) of Iterable of Numbers
     (float or integer).

    Examples:

    >>> v1 = (1, 70)
    >>> print(magnitude_vector(v1))
    70.00714249274856
    >>> v2 = [-10, 5, 2]
    >>> print(magnitude_vector(v2))
    11.357816691600547
    >>> v3 = (0, 0)
    >>> print(magnitude_vector(v3))
    0.0
    """
    return sum(map(lambda x: x ** 2, any_vector)) ** 0.5


def vector_normalize(any_vector):
    """Return a Normalized Vector.

    Note: if Euclidean norm (or Magnitude) of Vector Equal 0. Return as it is.
    """
    magnitude_sq = sum(map(lambda x: x ** 2, any_vector))
    if magnitude_sq:
        return map(lambda x: x / (magnitude_sq ** 0.5), any_vector)
    return any_vector


def is_vector_normalized(any_vector):
    """Return True if vector is normalized, otherwise False."""
    return isclose(sum(map(lambda x: x ** 2, any_vector)), 1)


def vector_direction(from_v1, to_v2):
    """Return Vector of direction between 2 Vectors (Must have same length).

    Warning: in case vectors doesn't have same length. it will raise IndexError.

    Note: output Vector is Not normalized.

    Examples:

    >>> point_v1 = (10, 10)
    >>> point_v2 = (1, 1)
    >>> mid_point1 = vector_direction(point_v1, point_v2)
    >>> print(list(mid_point1))
    [9, 9]
    >>> point_v3 = (-1, 5, 9)
    >>> point_v4 = (18, 0, -10)
    >>> mid_point2 = vector_direction(point_v3, point_v4)
    >>> print(list(mid_point2))
    [-19, 5, 19]
    """
    ##### check
    if len(from_v1) != len(to_v2):
        raise IndexError(EM_WRONG_LENGTH % (
            len(from_v1), len(to_v2), str(to_v2)))
    ##### end check
    func_sub = lambda x1, x2: x1 - x2
    return map(func_sub, from_v1, to_v2)


def vector_midpoint(v1, v2):
    """Return Coordinate of midpoint between 2 Vectors (Must have same length).

    Warning: in case vectors doesn't have same length. it will raise IndexError.

    Examples:

    >>> point_v1 = (7, 9)
    >>> point_v2 = (1, 2)
    >>> mid_point1 = vector_midpoint(point_v1, point_v2)
    >>> print(list(mid_point1))
    [4.0, 5.5]
    >>> point_v3 = (-1, 5, 9)
    >>> point_v4 = (18, 7, -10)
    >>> mid_point2 = vector_midpoint(point_v3, point_v4)
    >>> print(list(mid_point2))
    [8.5, 6.0, -0.5]
    """
    ##### check
    if len(v1) != len(v2):
        raise IndexError(EM_WRONG_LENGTH % (len(v1), len(v2), str(v2)))
    ##### end check
    func_add_div2 = lambda x1, x2: (x1 + x2) / 2
    return map(func_add_div2, v1, v2)


def vector_round(any_vector, ndigits=None):
    """Return Vector after round all Numbers (float or integer)."""
    return map(lambda x: round(x, ndigits=ndigits), any_vector)


def vector_ceil(any_vector):
    """Return Vector after ceil all Numbers (float or integer)."""
    return map(math.ceil, any_vector)


def vector_floor(any_vector):
    """Return Vector after floor all Numbers (float or integer)."""
    return map(math.floor, any_vector)


def vector_negative(any_vector):
    """Return Vector after change the sign of all Numbers (float or integer).
    """
    return map(lambda x: -x, any_vector)


def vector_abs(any_vector):
    """Return Vector of absolute value of all its Numbers (float or integer).
    """
    return map(abs, any_vector)


def vector_zero(n):
    """Return Vector length ``n`` full of Zero ."""
    return map(lambda _: 0, range(n))


def vector_from_matrix(any_matrix):
    """convert Any Matrix to a Vector of Numbers (float or integer).
     Return Vector (it length equal of rows*columns of Matrix) as a List.

    Examples:

    >>> matrix1 = [[0, 1, 0], [0, 1, 2]]
    >>> print(vector_from_matrix(matrix1))
    [0, 1, 0, 0, 1, 2]
    >>> matrix2 = [[0, 1, 0, -4], [0, 1, 2, 3], [1, 2, 7, 10], [9, 7, -1, 0]]
    >>> print(vector_from_matrix(matrix2))
    [0, 1, 0, -4, 0, 1, 2, 3, 1, 2, 7, 10, 9, 7, -1, 0]
    """
    return [column for row in any_matrix for column in row]


def string_format_vector(any_vector, format_spec):
    """make string format of Any Vector (Sequences of Numbers (float or int)).

    Examples:
    >>> vector1 = [1, 2, 3, 4, 5, 6]
    >>> print(string_format_vector(vector1, ".2f"))
    [1.00, 2.00, 3.00, 4.00, 5.00, 6.00]
    """
    return "[%s]" % ", ".join(map(lambda x: format(x, format_spec), any_vector))


#################################### Vector2 ###################################
def cross_product_v2(v1, v2):
    """Cross Product Between 2 Vector2 (x, y).
     Return a Tuple of 3 Numbers (First 2 Numbers are always zero 0).

    Warning: in case any of ``v1`` or ``v2`` are not Vector2.
     it will raise IndexError.

    Examples:

    >>> v1_cross = (1, 2)
    >>> v2_cross = (10, 7)
    >>> print(cross_product_v2(v1_cross, v2_cross))
    (0, 0, -13)
    >>> v1_cross = (3, 7)
    >>> v2_cross = (5, 12)
    >>> print(cross_product_v2(v1_cross, v2_cross))
    (0, 0, 1)
    """
    ##### check
    if not (len(v1) == len(v2) == 2):
        got = "v1=%s, v2=%s" % (str(v1), str(v2))
        raise IndexError(EM_NOT_EXPECTED % ("`v1` And `v2` be Vector2", got))
    ##### end check
    return 0, 0, (v1[0] * v2[1]) - (v1[1] * v2[0])


def angle_v2(v1, v2, center=None):
    """Return Angle (in radians range in [-pi, pi]) Between 2 Vector2 (x, y)
     based on center.

    Warning: in case any of ``center`` or ``v1`` or ``v2`` are not Vector2.
     it will raise IndexError.

    Warning: ``center`` Must not Equal To any ``v1`` or ``v2``.
     Or it will Raise ValueError.

    Note: ``center`` (by default None)
    | * if it's None or not specified. center will be [x=0, y=0].
    | * if it's specified use it (it should be any Vector2 (x, y)) :D.

    Note: output will return angle in radius between [-pi, pi].

    Examples:

    >>> vector1 = (0, 1)
    >>> vector2 = (1, 0)
    >>> print(angle_v2(vector1, vector2))
    -1.5707963267948966
    >>> print(angle_v2(vector2, vector1))
    1.5707963267948966
    >>> print(angle_v2(vector1, vector2, center=(0.5, 0.5)))
    3.141592653589793
    >>> print(angle_v2(vector2, vector1, center=(0.5, 0.5)))
    3.141592653589793
    >>> try:
    ...     print(angle_v2(vector1, vector2, center=(1, 0)))
    ... except ValueError:
    ...     print("DON'T make any point/vector same as center!!")
    DON'T make any point/vector same as center!!
    """
    length = 2
    if center is None:
        center = [0, 0]
    ####
    if not (len(center) == len(v1) == len(v2) == length):
        message = "`center` And `v1` And `v2` be Vector2"
        got = "v1=%s, v2=%s, center=%s" % (str(v1), str(v2), str(center))
        raise IndexError(EM_NOT_EXPECTED % (message, got))
    check1 = [center[i] == v1[i] for i in range(length)]
    check2 = [center[i] == v2[i] for i in range(length)]
    if all(check1) or all(check2):
        message = "`center` Not Equal To `v1` or `v2`"
        got = "v1=%s, v2=%s, center=%s" % (str(v1), str(v2), str(center))
        raise ValueError(EM_NOT_EXPECTED % (message, got))
    ##
    v1 = [v1[i] - center[i] for i in range(length)]
    v2 = [v2[i] - center[i] for i in range(length)]
    dot_product = sum([(v1[i] * v2[i]) for i in range(length)])
    cross_product = (v1[0] * v2[1]) - (v1[1] * v2[0])
    return math.atan2(cross_product, dot_product)


#################################### Vector3 ###################################
def cross_product_v3(v1, v2):
    """Cross Product Between 2 Vector3 (x, y, z). Return a Tuple of 3 Numbers.

    Warning: in case any of ``v1`` or ``v2`` are not Vector3.
     it will raise IndexError.

    Examples:

    >>> v1_cross = (1, 2, 10)
    >>> v2_cross = (10, 7, 3)
    >>> print(cross_product_v3(v1_cross, v2_cross))
    (-64, 97, -13)
    >>> v3_cross = (-4, 0, 8)
    >>> v4_cross = (9, 16, 2)
    >>> print(cross_product_v3(v3_cross, v4_cross))
    (-128, 80, -64)
    """
    ##### check
    if not (len(v1) == len(v2) == 3):
        got = "v1=%s, v2=%s" % (str(v1), str(v2))
        raise IndexError(EM_NOT_EXPECTED % ("`v1` And `v2` be Vector3", got))
    ##### end check
    return ((v1[1] * v2[2]) - (v1[2] * v2[1]),
            (v1[2] * v2[0]) - (v1[0] * v2[2]),
            (v1[0] * v2[1]) - (v1[1] * v2[0]))


def angle_v3(v1, v2, center=None):
    """Return Angle (in radians range in [-pi, pi]) Between 2 Vector3 (x, y, z)
     based on center.

    Warning: in case any of ``center`` or ``v1`` or ``v2`` are not Vector3.
     it will raise IndexError.

    Warning: ``center`` Must not Equal To any ``v1`` or ``v2``.
     Or it will Raise ValueError.

    Note: ``center`` (by default None)
    | * if it's None or not specified. center will be [x=0, y=0, z=0].
    | * if it's specified use it (it should be any Vector2 (x, y, z)).

    Examples:

    >>> vector1 = (0, 1, 0)
    >>> vector2 = (1, 0, 1)
    >>> vector3 = (10, 2, 10)
    >>> print(angle_v3(vector1, vector2))
    1.5707963267948966
    >>> print(angle_v3(vector2, vector1))
    1.5707963267948966
    >>> print(angle_v3(vector1, vector3))
    1.4303066250413763
    >>> print(angle_v3(vector3, vector1))
    ... # in 3D reverse the order not change result !
    1.4303066250413763
    >>> print(angle_v3(vector1, vector2, center=(0.5, 0.5, 0.5)))
    3.141592653589793
    >>> print(angle_v3(vector2, vector1, center=(0.5, 0.5, 0.5)))
    3.141592653589793
    >>> try:
    ...     print(angle_v3(vector1, vector2, center=(1, 0, 1)))
    ... except ValueError:
    ...     print("DON'T make any point/vector same as center!!")
    DON'T make any point/vector same as center!!
    """
    length = 3
    if center is None:
        center = [0, 0, 0]
    ##### check
    if not (len(center) == len(v1) == len(v2) == length):
        message = "`center` And `v1` And `v2` be Vector3"
        got = "v1=%s, v2=%s, center=%s" % (str(v1), str(v2), str(center))
        raise IndexError(EM_NOT_EXPECTED % (message, got))
    check1 = [center[i] == v1[i] for i in range(length)]
    check2 = [center[i] == v2[i] for i in range(length)]
    if all(check1) or all(check2):
        message = "`center` Not Equal To `v1` or `v2`"
        got = "v1=%s, v2=%s, center=%s" % (str(v1), str(v2), str(center))
        raise ValueError(EM_NOT_EXPECTED % (message, got))
    ##### end check
    v1 = [v1[i] - center[i] for i in range(length)]
    v2 = [v2[i] - center[i] for i in range(length)]
    dot_product = sum([(v1[i] * v2[i]) for i in range(length)])
    cross_product = ((v1[1] * v2[2]) - (v1[2] * v2[1]),
                     (v1[2] * v2[0]) - (v1[0] * v2[2]),
                     (v1[0] * v2[1]) - (v1[1] * v2[0]))
    return math.atan2(sum(map(lambda x: x ** 2, cross_product)) ** 0.5,
                      dot_product)


def axis_angle_from_quaternion(quaternion):
    """Convert Quaternion To Axis (x, y, z) and Angle (in radians [0, 2*pi]).
     Return them in a tuple of (axis, angle).

    Note: ``quaterion`` are normalized in function (only if not (-1 >= w >= 1)).
    """
    is_w_norm = abs(quaternion[3]) <= 1
    if is_w_norm:
        axis = quaternion[:3]
        w = quaternion[3]
    else:
        magnitude = sum(map(lambda x: x ** 2, quaternion)) ** 0.5
        axis = [x / magnitude for x in quaternion[:3]]
        w = quaternion[3] / magnitude
    angle = 2 * math.acos(w)
    num = (1 - w ** 2) ** 0.5
    ##
    if num:
        return tuple(map(lambda x: x / num, axis)), angle
    else:
        return axis, angle


def axis_angle_from_matrix_3x3(any_matrix_3x3):
    """Convert Matrix (3x3) To Axis (x, y, z) and angle (in radians [0, 2*pi]).
     Return them in a tuple of (axis, angle).

    Note: ``any_matrix_3x3`` is Not normalized in function.
    """
    ##### matrix to quaternion
    a0_0, a0_1, a0_2 = any_matrix_3x3[0]
    a1_0, a1_1, a1_2 = any_matrix_3x3[1]
    a2_0, a2_1, a2_2 = any_matrix_3x3[2]
    ##### Doubles conversion: Quaternion -> Axis angle -> Matrix 3x3.
    trace = a0_0 + a1_1 + a2_2
    if trace > 0:
        s = 0.5 / (trace + 1.0) ** 0.5
        ##
        axis = ((a2_1 - a1_2) * s, (a0_2 - a2_0) * s, (a1_0 - a0_1) * s)
        w = 0.25 / s
    elif (a0_0 > a1_1) and (a0_0 > a2_2):
        s = 2.0 * (1.0 + a0_0 - a1_1 - a2_2) ** 0.5
        ##
        axis = (0.25 * s, (a0_1 + a1_0) / s, (a0_2 + a2_0) / s)
        w = (a2_1 - a1_2) / s
    elif a1_1 > a2_2:
        s = 2.0 * (1.0 - a0_0 + a1_1 - a2_2) ** 0.5
        ##
        axis = ((a0_1 + a1_0) / s, 0.25 * s, (a1_2 + a2_1) / s)
        w = (a0_2 - a2_0) / s
    else:
        s = 2.0 * (1.0 - a0_0 - a1_1 + a2_2) ** 0.5
        ##
        axis = ((a0_2 + a2_0) / s, (a1_2 + a2_1) / s, 0.25 * s)
        w = (a1_0 - a0_1) / s
    ##
    w = max(-1, max(w, 1))
    angle = 2 * math.acos(w)
    num = (1 - w ** 2) ** 0.5
    ##
    if isclose(num, 0, abs_tol=epsilon):
        return axis, angle
    else:
        return tuple(vector_truediv_value(axis, num)), angle


def axis_angle_from_euler(yaw, pitch, roll, order):
    """Convert Euler Angles To Axis (x, y, z) and angle (in radians).
     Return them in a tuple of (axis, angle).

    Warning: ``yaw`` and ``pitch`` and ``roll`` all in radians.
     also be Careful about Gimbal Lock.

    Warning: ``order`` must be string for order axis rotation for Euler angles
     (a.k.a. Tait–Bryan angles) either uppercase or lowercase or mixed
     (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.
    """
    order = order.upper()
    ##### check
    if order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % order)
    ##### end check
    ## Doubles conversion: Euler Angles -> Quaternion -> Axis angle
    yaw, pitch, roll = (yaw % tau) / 2, (pitch % tau) / 2, (roll % tau) / 2
    ##
    qx = lambda a: (math.sin(a), 0, 0, math.cos(a))
    qy = lambda b: (0, math.sin(b), 0, math.cos(b))
    qz = lambda c: (0, 0, math.sin(c), math.cos(c))
    #### Start X
    if order == "XYZ":
        x, y, z, w = quaternion_mul_quaternions(qx(yaw), qy(pitch), qz(roll))
    elif order == "XZY":
        x, y, z, w = quaternion_mul_quaternions(qx(yaw), qz(pitch), qy(roll))
    #### Start Y
    elif order == "YXZ":
        x, y, z, w = quaternion_mul_quaternions(qy(yaw), qx(pitch), qz(roll))
    elif order == "YZX":
        x, y, z, w = quaternion_mul_quaternions(qy(yaw), qz(pitch), qx(roll))
    #### Start Z
    elif order == "ZXY":
        x, y, z, w = quaternion_mul_quaternions(qz(yaw), qx(pitch), qy(roll))
    else:  # order == "ZYX"
        x, y, z, w = quaternion_mul_quaternions(qz(yaw), qy(pitch), qx(roll))
    ##
    axis = (x, y, z)
    w = max(-1, min(w, 1))
    angle = 2 * math.acos(w)
    num = (1 - w ** 2) ** 0.5
    ##
    if isclose(num, 0, abs_tol=epsilon):
        return axis, angle
    else:
        return tuple(vector_truediv_value(axis, num)), angle


def euler_from_matrix_3x3(any_matrix_3x3, order):
    """Convert Any Matrix (3x3) To Euler Angles (yaw, pitch, roll).
     Return Euler Angle as Tuple (yaw, pitch, roll) (all in radians).

    Warning: ``order`` must be string for order axis rotation for Euler angles
     (a.k.a. Tait–Bryan angles) either uppercase or lowercase or mixed
     (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.

    Note: ``any_matrix_3x3`` is Not normalized in function.

    Note: in the output both of ``yaw`` and ``roll`` are between [-pi, pi],
     and ``pitch`` is between [-pi/2, pi/2].
    """
    order = order.upper()
    ##### check
    if order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % order)
    ##### end check
    a0_0, a0_1, a0_2 = any_matrix_3x3[0]
    a1_0, a1_1, a1_2 = any_matrix_3x3[1]
    a2_0, a2_1, a2_2 = any_matrix_3x3[2]
    ## get function from ``math``
    atan2, asin = math.atan2, math.asin
    ## Start X
    if order == "XYZ":
        pitch_value = max(-1, min(a0_2, 1))
        return atan2(-a1_2, a2_2), asin(pitch_value), atan2(-a0_1, a0_0)
    elif order == "XZY":
        pitch_value = max(-1, min(-a0_1, 1))
        return atan2(a2_1, a1_1), asin(pitch_value), atan2(a0_2, a0_0)
    ## Start Y
    elif order == "YXZ":
        pitch_value = max(-1, min(-a1_2, 1))
        return atan2(a0_2, a2_2), asin(pitch_value), atan2(a1_0, a1_1)
    elif order == "YZX":
        pitch_value = max(-1, min(a1_0, 1))
        return atan2(-a2_0, a0_0), asin(pitch_value), atan2(-a1_2, a1_1)
    ## Start Z
    elif order == "ZYX":
        pitch_value = max(-1, min(-a2_0, 1))
        return atan2(a1_0, a0_0), asin(pitch_value), atan2(a2_1, a2_2)
    else:  # ZXY
        pitch_value = max(-1, min(a2_1, 1))
        return atan2(-a0_1, a1_1), asin(pitch_value), atan2(-a2_0, a2_2)


def euler_from_quaternion(quaternion, order):
    """Convert Quaternion (a.k.a. Vector4 (x, y, z, w)) To Euler angles.
     Return Euler angles as Tuple (yaw, pitch, roll) (all in radians).

    Warning: be Careful about ZeroDivision in case ``quaternion`` Equal To 0.

    Warning: ``order`` must be string for order axis rotation for Euler angles
     (a.k.a. Tait–Bryan angles) either uppercase or lowercase or mixed
     (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.

    Note: ``quaternion`` is normalized in function.

    Note: in the output both of ``yaw`` and ``roll`` are between [-pi, pi],
     and ``pitch`` is between [-pi/2, pi/2].
    """
    x, y, z, w = tuple(vector_normalize(quaternion))
    ## Doubles conversion: Quaternion -> Matrix 3x3 -> Euler Angles.
    x_2, y_2, z_2, w_2 = x ** 2, y ** 2, z ** 2, w ** 2
    ##
    x_y, x_z, x_w = x * y, x * z, x * w
    y_z, y_w = y * z, y * w
    z_w = z * w
    inv = 1 / (x_2 + y_2 + z_2 + w_2)
    ## get function from ``math``
    atan2, asin = math.atan2, math.asin
    ## Start X
    if order == "XYZ":
        return (atan2(-2.0 * (y_z - x_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv),
                asin(max(-1, min(2.0 * (x_z + y_w) * inv, 1))),
                atan2(-2.0 * (x_y - z_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv))
    elif order == "XZY":
        return (atan2(2.0 * (y_z + x_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(-2.0 * (x_y - z_w) * inv, 1))),
                atan2(2.0 * (x_z + y_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv))
    ## Start Y
    elif order == "YXZ":
        return (atan2(2.0 * (x_z + y_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv),
                asin(max(-1, min(-2.0 * (y_z - x_w) * inv, 1))),
                atan2(2.0 * (x_y + z_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv))
    elif order == "YZX":
        return (atan2(-2.0 * (x_z - y_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(2.0 * (x_y + z_w) * inv, 1))),
                atan2(-2.0 * (y_z - x_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv))
    ## Start Z
    elif order == "ZYX":
        return (atan2(2.0 * (x_y + z_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(-2.0 * (x_z - y_w) * inv, 1))),
                atan2(2.0 * (y_z + x_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv))
    else:  # ZXY
        return (atan2(-2.0 * (x_y - z_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(2.0 * (y_z + x_w) * inv, 1))),
                atan2(-2.0 * (x_z - y_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv))


def euler_from_axis_angle(axis, angle, order):
    """Convert Axis (x, y, z) and angle (in radians) To Euler angles.
     Return Euler angles as Tuple (yaw, pitch, roll) (all in radians).

    Warning: be Careful about ZeroDivision in case ``axis`` Equal To 0.

    Warning: ``order`` must be string for order axis rotation for Euler angles
     (a.k.a. Tait–Bryan angles) either uppercase or lowercase or mixed
     (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.

    Note: ``axis`` is normalized in function.

    Note: in the output both of ``yaw`` and ``roll`` are between [-pi, pi],
     and ``pitch`` is between [-pi/2, pi/2].
    """
    ##### check
    order = order.upper()
    if order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % order)
    ##### end check
    ## Doubles conversion: Axis angle -> Quaternion -> Euler Angles
    angle = ((angle % tau) / 2)
    sin_angle = math.sin(angle)
    w = math.cos(angle)
    ##
    axis = tuple(vector_normalize(axis))
    x, y, z = (axis[0] * sin_angle, axis[1] * sin_angle, axis[2] * sin_angle)
    x_2, y_2, z_2, w_2 = x ** 2, y ** 2, z ** 2, w ** 2
    ##
    x_y, x_z, x_w = x * y, x * z, x * w
    y_z, y_w = y * z, y * w
    z_w = z * w
    inv = 1 / (x_2 + y_2 + z_2 + w_2)
    ## get function from ``math``
    atan2, asin = math.atan2, math.asin
    ## Start X
    if order == "XYZ":
        return (atan2(-2.0 * (y_z - x_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv),
                asin(max(-1, min(2.0 * (x_z + y_w) * inv, 1))),
                atan2(-2.0 * (x_y - z_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv))
    elif order == "XZY":
        return (atan2(2.0 * (y_z + x_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(-2.0 * (x_y - z_w) * inv, 1))),
                atan2(2.0 * (x_z + y_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv))
    ## Start Y
    elif order == "YXZ":
        return (atan2(2.0 * (x_z + y_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv),
                asin(max(-1, min(-2.0 * (y_z - x_w) * inv, 1))),
                atan2(2.0 * (x_y + z_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv))
    elif order == "YZX":
        return (atan2(-2.0 * (x_z - y_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(2.0 * (x_y + z_w) * inv, 1))),
                atan2(-2.0 * (y_z - x_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv))
    ## Start Z
    elif order == "ZYX":
        return (atan2(2.0 * (x_y + z_w) * inv, (x_2 - y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(-2.0 * (x_z - y_w) * inv, 1))),
                atan2(2.0 * (y_z + x_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv))
    else:  # ZXY
        return (atan2(-2.0 * (x_y - z_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv),
                asin(max(-1, min(2.0 * (y_z + x_w) * inv, 1))),
                atan2(-2.0 * (x_z - y_w) * inv, (-x_2 - y_2 + z_2 + w_2) * inv))


def euler_from_euler(yaw, pitch, roll, input_order, output_order):
    """Convert Euler Angles from input order To Euler Angles from output order.
     Return Euler angles as Tuple (yaw, pitch, roll) (all in radians).

    Warning: all of input ``yaw`` and ``pitch`` and ``roll`` all in radians.
     also be Careful about Gimbal Lock.

    Warning: ``input_order`` and ``output_order`` must be string for order axis
     rotation for Euler Angles (a.k.a. Tait–Bryan angles) either uppercase or
     lowercase or mixed (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.
    """
    input_order = input_order.upper()
    output_order = output_order.upper()
    ##### check
    if input_order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % input_order)
    if output_order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % output_order)
    ##### end check
    ## Doubles conversion: Euler Angles -> Matrix 3x3 -> Euler Angles
    c_y, s_y = math.cos(yaw), math.sin(yaw)
    c_p, s_p = math.cos(pitch), math.sin(pitch)
    c_r, s_r = math.cos(roll), math.sin(roll)
    ## Start X
    if input_order == "XYZ":
        matrix_3x3 = [[c_p * c_r, -c_p * s_r, s_p],
                      [(c_y * s_r) + (s_y * s_p * c_r),
                       (c_y * c_r) - (s_y * s_p * s_r), -s_y * c_p],
                      [(s_y * s_r) - (c_y * s_p * c_r),
                       (s_y * c_r) + (c_y * s_p * s_r), c_y * c_p]]
    elif input_order == "XZY":
        matrix_3x3 = [[c_p * c_r, -s_p, c_p * s_r],
                      [(c_y * s_p * c_r) + (s_y * s_r), c_y * c_p,
                       (c_y * s_p * s_r) - (s_y * c_r)],
                      [(s_y * s_p * c_r) - (c_y * s_r), s_y * c_p,
                       (s_y * s_p * s_r) + (c_y * c_r)]]
    ## Start Y
    elif input_order == "YXZ":
        matrix_3x3 = [
            [(s_y * s_p * s_r) + (c_y * c_r), (s_y * s_p * c_r) - (c_y * s_r),
             s_y * c_p], [c_p * s_r, c_p * c_r, -s_p],
            [(c_y * s_p * s_r) - (s_y * c_r), (c_y * s_p * c_r) + (s_y * s_r),
             c_y * c_p]]
    elif input_order == "YZX":
        matrix_3x3 = [[c_y * c_p, (s_y * s_r) - (c_y * s_p * c_r),
                       (s_y * c_r) + (c_y * s_p * s_r)],
                      [s_p, c_p * c_r, -c_p * s_r],
                      [-s_y * c_p, (c_y * s_r) + (s_y * s_p * c_r),
                       (c_y * c_r) - (s_y * s_p * s_r)]]
    ## Start Z
    elif input_order == "ZYX":
        matrix_3x3 = [[c_y * c_p, (c_y * s_p * s_r) - (s_y * c_r),
                       (c_y * s_p * c_r) + (s_y * s_r)],
                      [c_y * c_p, (s_y * s_p * s_r) + (c_y * c_r),
                       (s_y * s_p * c_r) - (c_y * s_r)],
                      [-s_p, c_p * s_r, c_p * c_r]]
    else:  # ZXY
        matrix_3x3 = [[(c_y * c_r) - (s_y * s_p * s_r), -s_y * c_p,
                       (c_y * s_r) + (s_y * s_p * c_r)],
                      [(s_y * c_r) + (c_y * s_p * s_r), c_y * c_p,
                       (s_y * s_p) - (c_y * s_p * c_r)],
                      [-s_y * c_p, s_p, c_p * c_r]]
    #####
    a0_0, a0_1, a0_2 = matrix_3x3[0]
    a1_0, a1_1, a1_2 = matrix_3x3[1]
    a2_0, a2_1, a2_2 = matrix_3x3[2]
    ## get function from ``math``
    atan2, asin = math.atan2, math.asin
    ## Start X
    if output_order == "XYZ":
        pitch_value = max(-1, min(a0_2, 1))
        return atan2(-a1_2, a2_2), asin(pitch_value), atan2(-a0_1, a0_0)
    elif output_order == "XZY":
        pitch_value = max(-1, min(-a0_1, 1))
        return atan2(a2_1, a1_1), asin(pitch_value), atan2(a0_2, a0_0)
    ## Start Y
    elif output_order == "YXZ":
        pitch_value = max(-1, min(-a1_2, 1))
        return atan2(a0_2, a2_2), asin(pitch_value), atan2(a1_0, a1_1)
    elif output_order == "YZX":
        pitch_value = max(-1, min(a1_0, 1))
        return atan2(-a2_0, a0_0), asin(pitch_value), atan2(-a1_2, a1_1)
    ## Start Z
    elif output_order == "ZYX":
        pitch_value = max(-1, min(-a2_0, 1))
        return atan2(a1_0, a0_0), asin(pitch_value), atan2(a2_1, a2_2)
    else:  # ZXY
        pitch_value = max(-1, min(a2_1, 1))
        return atan2(-a0_1, a1_1), asin(pitch_value), atan2(-a2_0, a2_2)


############################## Vector4/Quaternion ##############################
def quaternion_identity():
    """Return Tuple of Quaternion (a.k.a. Vector4) (x=0, y=0, z=0, w=1)."""
    return 0, 0, 0, 1


def quaternion_multiply(q1, q2):
    """Multiplication between 2 Quaternions (a.k.a. Vector4).
     Return Result as Tuple (x, y, z, w).

    Examples:

    >>> quaternion1 = (1, 0.4, 1, 0.6)
    >>> quaternion2 = [0.8, 2, 7, 1]  # work with any Sequence of Numbers
    >>> print(quaternion_multiply(quaternion1, quaternion2))
    (2.2800000000000002, -4.6, 6.88, -8.0)
    >>> print(quaternion_multiply(quaternion2, quaternion1))  # Not the Same !!!
    (0.6799999999999997, 7.8, 3.5200000000000005, -8.0)
    >>> quaternion3 = quaternion_identity()  # (x=0, y=0, z=0, w=1)
    >>> print(quaternion_multiply(quaternion1, quaternion3))
    (1.0, 0.4, 1.0, 0.6)
    >>> print(quaternion_multiply(quaternion1, quaternion3))
    (1.0, 0.4, 1.0, 0.6)
    """
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return ((x1 * w2) + (w1 * x2) + (y1 * z2) - (z1 * y2),
            (y1 * w2) + (w1 * y2) + (z1 * x2) - (x1 * z2),
            (z1 * w2) + (w1 * z2) + (x1 * y2) - (y1 * x2),
            (w1 * w2) - (x1 * x2) - (y1 * y2) - (z1 * z2))


def quaternion_mul_quaternions(*quaternions):
    """Multiplication between Quaternions (a.k.a. Vector4).
     Return Result as Tuple (x, y, z, w).

    Examples:

    >>> quaternion1 = (1, 0.4, 1, 0.6)
    >>> quaternion2 = [0.8, 2, 7, 1]  # work with any Sequence of Number
    >>> quaternion3 = (0.2, -0.01, 0.5, -1)
    >>> print(quaternion_mul_quaternions(quaternion1, quaternion2, quaternion3))
    (-6.111199999999999, 4.916, -9.9828, 4.058)
    >>> print(quaternion_mul_quaternions(quaternion2, quaternion1, quaternion3))
    (1.6552, -7.356, -9.0868, 6.182)
    >>> quaternion4 = quaternion_identity()  # (x=0, y=0, z=0, w=1)
    >>> print(quaternion_mul_quaternions(quaternion1, quaternion4))
    (1.0, 0.4, 1.0, 0.6)
    >>> print(quaternion_mul_quaternions(quaternion1, quaternion4))
    (1.0, 0.4, 1.0, 0.6)
    """
    result = (0, 0, 0, 1)  # quaternion identity (x, y, z, w)
    for q in quaternions:
        result = quaternion_multiply(result, q)
    return result


def quaternion_opposite(quaternion):
    """Return opposite rotation of Quaternion (-x, -y, -z, w) as a Tuple."""
    return -quaternion[0], -quaternion[1], -quaternion[2], quaternion[3]


def quaternion_from_axis_angle(axis, angle):
    """Convert axis (x, y, z) and angle (in radians) To Quaternion.
     Return Quaternion (x, y, z, w) as a Tuple.

    Note: ``axis`` is normalized in function.
    """
    angle = (angle % tau) / 2
    sin_angle = math.sin(angle)
    magnitude_sq = sum(map(lambda x: x ** 2, axis))
    if magnitude_sq:
        x, y, z = [(v / (magnitude_sq ** 0.5)) * sin_angle for v in axis]
    else:
        x, y, z = [v * sin_angle for v in axis]
    ##
    return x, y, z, math.cos(angle)


def quaternion_from_euler(yaw, pitch, roll, order):
    """Convert Euler angles (yaw, pitch, roll) (all in radians) To Quaternion.
     Return Quaternion (a.k.a. Vector4) as Tuple (x, y, z, w).

    Warning: ``yaw`` and ``pitch`` and ``roll`` all Must be in radians.

    Warning: ``order`` must be string for order axis rotation for Euler angles
     (a.k.a. Tait–Bryan angles) either uppercase or lowercase or mixed
     (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.
    """
    order = order.upper()
    ##### check
    if order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % order)
    ##### end check
    yaw, pitch, roll = (yaw % tau) / 2, (pitch % tau) / 2, (roll % tau) / 2
    ##
    qx = lambda angle: (math.sin(angle), 0, 0, math.cos(angle))
    qy = lambda angle: (0, math.sin(angle), 0, math.cos(angle))
    qz = lambda angle: (0, 0, math.sin(angle), math.cos(angle))
    #### Start X
    if order == "XYZ":
        return quaternion_mul_quaternions(qx(yaw), qy(pitch), qz(roll))
    elif order == "XZY":
        return quaternion_mul_quaternions(qx(yaw), qz(pitch), qy(roll))
    #### Start Y
    elif order == "YXZ":
        return quaternion_mul_quaternions(qy(yaw), qx(pitch), qz(roll))
    elif order == "YZX":
        return quaternion_mul_quaternions(qy(yaw), qz(pitch), qx(roll))
    #### Start Z
    elif order == "ZXY":
        return quaternion_mul_quaternions(qz(yaw), qx(pitch), qy(roll))
    else:  # ZYX
        return quaternion_mul_quaternions(qz(yaw), qy(pitch), qx(roll))


def quaternion_from_matrix_3x3(any_matrix_3x3):
    """Convert a Matrix (3x3) To Quaternion.
     Return A Quaternion as Tuple (x, y, z, w) with the Matrix's rotation.

    Note: ``any_matrix_3x3`` is Not normalized in function.
    """
    a0_0, a0_1, a0_2 = any_matrix_3x3[0]
    a1_0, a1_1, a1_2 = any_matrix_3x3[1]
    a2_0, a2_1, a2_2 = any_matrix_3x3[2]
    ##
    trace = a0_0 + a1_1 + a2_2
    if trace > 0:
        s = 0.5 / (trace + 1.0) ** 0.5
        qx = (a2_1 - a1_2) * s
        qy = (a0_2 - a2_0) * s
        qz = (a1_0 - a0_1) * s
        qw = 0.25 / s
    elif (a0_0 > a1_1) and (a0_0 > a2_2):
        s = 2.0 * (1.0 + a0_0 - a1_1 - a2_2) ** 0.5
        qx = 0.25 * s
        qy = (a0_1 + a1_0) / s
        qz = (a0_2 + a2_0) / s
        qw = (a2_1 - a1_2) / s
    elif a1_1 > a2_2:
        s = 2.0 * (1.0 - a0_0 + a1_1 - a2_2) ** 0.5
        qx = (a0_1 + a1_0) / s
        qy = 0.25 * s
        qz = (a1_2 + a2_1) / s
        qw = (a0_2 - a2_0) / s
    else:
        s = 2.0 * (1.0 - a0_0 - a1_1 + a2_2) ** 0.5
        qx = (a0_2 + a2_0) / s
        qy = (a1_2 + a2_1) / s
        qz = 0.25 * s
        qw = (a1_0 - a0_1) / s
    ##
    return qx, qy, qz, qw


#################################### Matrix ####################################
def matrix_getitem(any_matrix, index):
    """Return items of Any Matrix from index (integer Or slice) Or
     Tuple of 2 index (int Or/And slice).

    Info: this function is similar to how NumPy array works.

    Examples:

    >>> m1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> result1 = matrix_getitem(m1, 1)
    >>> print(list(result1))
    [5, 6, 7, 8]
    >>> result2 = matrix_getitem(m1, slice(None, 2))
    >>> print(list(result2))
    [[1, 2, 3, 4], [5, 6, 7, 8]]
    >>> result3 = matrix_getitem(m1, (2, 3))
    >>> print(result3)
    12
    >>> result4 = matrix_getitem(m1, (3, slice(2, None)))
    >>> print(list(result4))
    [15, 16]
    >>> result5 = matrix_getitem(m1, (slice(None, 3), 3))
    >>> print(list(result5))
    [4, 8, 12]
    >>> result6 = matrix_getitem(m1, (slice(None, 3), slice(1, 3)))
    >>> print(list(result6))
    [[2, 3], [6, 7], [10, 11]]
    """
    if isinstance(index, tuple):
        ##### check
        func_is_index = lambda x: isinstance(x, AnyIndex_Tuple)
        if (not all(map(func_is_index, index))) or len(index) != 2:
            raise TypeError(EM_NOT_TUPLE_INDEX % index)
        ##### end check
        index1, index2 = index
        if isinstance(index1, int):
            if isinstance(index2, int):
                return any_matrix[index1][index2]
            else:  # second index are slice
                item = any_matrix[index1][index2]
                if isinstance(item, Iterable):
                    return iter(item)
                else:  # got one item
                    return item
        else:  # first index are slice
            return map(lambda v: v[index2], any_matrix[index1])
    elif isinstance(index, int):
        return map(lambda i: i, any_matrix[index])
    else:  # index is slice
        return map(lambda v: [i for i in v], any_matrix[index])


def _matrix_setitem_from_index(any_matrix, index, new_value):
    """Return a new Matrix after changes from an index (int or slice).

    Info: this allows to use matrix like NumPy array :].

    Examples:

    >>> m1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> result1 = _matrix_setitem_from_index(m1, 2, 1)
    >>> print(list(result1))
    [[1, 2, 3, 4], [5, 6, 7, 8], [1, 1, 1, 1], [13, 14, 15, 16]]
    >>> result2 = _matrix_setitem_from_index(m1, 2, [100, 10, 140, 300])
    >>> print(list(result2))
    [[1, 2, 3, 4], [5, 6, 7, 8], [100, 10, 140, 300], [13, 14, 15, 16]]
    >>> result3 = _matrix_setitem_from_index(m1, 2, [[80, 10, 40, 30]])
    >>> print(list(result3))
    [[1, 2, 3, 4], [5, 6, 7, 8], [80, 10, 40, 30], [13, 14, 15, 16]]
    >>> result4 = _matrix_setitem_from_index(m1, 2, [[80], [10], [40], [30]])
    >>> print(list(result4))
    [[1, 2, 3, 4], [5, 6, 7, 8], [80, 10, 40, 30], [13, 14, 15, 16]]
    >>>  ############### Slice
    >>> result5 = _matrix_setitem_from_index(m1, slice(None, 2), 1)
    >>> print(list(result5))
    [[1, 1, 1, 1], [1, 1, 1, 1], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> result6 = _matrix_setitem_from_index(m1, slice(None, 2),
    ... [10, 10, 140, 300])
    >>> print(list(result6))
    [[10, 10, 140, 300], [10, 10, 140, 300], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> m2 = [[8, 10, 40, 30], [9.1, 10.5, 3.33, 1.9]]
    >>> result7 = _matrix_setitem_from_index(m1, slice(None, 2), m2)
    >>> print(list(result7))
    [[8, 10, 40, 30], [9.1, 10.5, 3.33, 1.9], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> m1  # untouch :D
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> m2  # untouch :D
    [[8, 10, 40, 30], [9.1, 10.5, 3.33, 1.9]]
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    ##
    return_matrix = lambda special_case, special_result: map(lambda r: [
        (special_result(r, c) if special_case(r) else any_matrix[r][c]) for c in
        range(num_columns)], range(num_rows))
    """return matrix for result.

    Note: ``special_case`` Must be lambda function accept 1 argument:
     ``row`` is from range number rows of matrix Then return bool.

    Note: ``special_result`` Must be lambda function accept 2 argument:
     `row` is from ``range_rows`` and `column` is from ``range_columns``.
     and return Number (float or integer)
    """
    ##
    if isinstance(index, int):
        is_in_case = lambda row: row == index
        if isinstance(new_value, Numbers_Tuple):
            return return_matrix(is_in_case, lambda *args: new_value)
        elif isinstance(new_value, Sequence):
            length_value = len(new_value)
            if is_contain_only(new_value, Numbers_Tuple):  # Vector
                ##### check
                if num_columns != length_value:
                    raise ValueError(EM_WRONG_VECTOR_LENGTH % (
                        num_columns, length_value, str(new_value)))
                ##### end check
                return return_matrix(is_in_case,
                                     lambda _, column: new_value[column])
            else:  # Matrix
                columns_value = len(new_value[0])
                is_1_row = (length_value == 1 and columns_value == num_columns)
                is_1_column = (
                        length_value == num_columns and columns_value == 1)
                ##### check
                if xor(is_1_row, is_1_column):
                    message = ("size of new value be either (1x%i) or (%ix1),"
                               % (num_columns, num_columns))
                    got = "(%ix%i) `%s`" % (
                        length_value, columns_value, str(new_value))
                    raise ValueError(EM_NOT_EXPECTED % (message, got))
                ##### end check
                if is_1_row:
                    return return_matrix(is_in_case,
                                         lambda _, column: new_value[0][column])
                else:  # case 2
                    return return_matrix(is_in_case,
                                         lambda _, column: new_value[column][0])
        else:
            raise TypeError(EM_WRONG_TYPE_FOR_INDEX % (
                type(new_value), str(new_value), index))
    else:  # index is slice
        range_items = range(num_rows)[index]
        is_in_case = lambda row: row in range_items
        if isinstance(new_value, Numbers_Tuple):
            return return_matrix(is_in_case, lambda *args: new_value)
        elif isinstance(new_value, Sequence):
            length_value = len(new_value)
            if is_contain_only(new_value, Numbers_Tuple):  # Vector
                ##### check
                if num_columns != length_value:
                    raise ValueError(EM_WRONG_VECTOR_LENGTH % (
                        num_columns, length_value, str(new_value)))
                ##### end check
                return return_matrix(is_in_case,
                                     lambda _, column: new_value[column])
            else:  # Matrix
                columns_value = len(new_value[0])
                num_items = len(range_items)
                ##### check
                if num_items != length_value or num_columns != columns_value:
                    raise ValueError(EM_WRONG_MATRIX_SIZE % (
                        num_items, num_columns, length_value, columns_value,
                        str(new_value)))
                ##### end check
                return return_matrix(is_in_case,
                                     lambda row, column: new_value[row][column])
        else:
            raise TypeError(EM_WRONG_TYPE_FOR_INDEX % (
                type(new_value), str(new_value), index))


def _matrix_setitem_from_tuple(any_matrix, tuple_index, new_value):
    """Return a new Matrix after changing values from tuple of 2 index
     (int Or/And slices).

    Info: this allows to use matrix like NumPy array :].

    Examples:

    >>> m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> result1 = _matrix_setitem_from_tuple(m1, (2, 1), 100)
    >>> print(list(result1))
    [[1, 2, 3], [4, 5, 6], [7, 100, 9]]
    >>> result2 = _matrix_setitem_from_tuple(m1, (2, slice(None, 2)), 100)
    >>> print(list(result2))
    [[1, 2, 3], [4, 5, 6], [100, 100, 9]]
    >>> result3 = _matrix_setitem_from_tuple(m1, (2, slice(None, 2)), [-1, 9.4])
    >>> print(list(result3))
    [[1, 2, 3], [4, 5, 6], [-1, 9.4, 9]]
    >>> ########## First Slice
    >>> result4 = _matrix_setitem_from_tuple(m1, (slice(None, 2), 1), -0.5)
    >>> print(list(result4))
    [[1, -0.5, 3], [4, -0.5, 6], [7, 8, 9]]
    >>> result5 = _matrix_setitem_from_tuple(m1, (slice(None, 2), 1), [90, -90])
    >>> print(list(result5))
    [[1, 90, 3], [4, -90, 6], [7, 8, 9]]
    >>> result6 = _matrix_setitem_from_tuple(m1, (slice(None, 2), 1),
    ...                                      [[0.33], [0]])
    >>> print(list(result6))
    [[1, 0.33, 3], [4, 0, 6], [7, 8, 9]]
    >>> result7 = _matrix_setitem_from_tuple(m1,
    ...                                      (slice(None, 2), slice(None, 3)),
    ...                                      -1)
    >>> print(list(result7))
    [[-1, -1, -1], [-1, -1, -1], [7, 8, 9]]
    >>> result8 = _matrix_setitem_from_tuple(m1,
    ...                                      (slice(None, 2), slice(None, 3)),
    ...                                      [-1, -2, -3])
    >>> print(list(result8))
    [[-1, -2, -3], [-1, -2, -3], [7, 8, 9]]
    >>> result9 = _matrix_setitem_from_tuple(m1,
    ...                                      (slice(None, 2), slice(None, 3)),
    ...                                      [[100, 9.3, 53], [8, -6, -1.1]])
    >>> print(list(result9))
    [[100, 9.3, 53], [8, -6, -1.1], [7, 8, 9]]
    >>> m1  # untouch :D
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    ##
    make_matrix = lambda special_case, special_result: map(lambda r: [
        (any_matrix[r][c] if not special_case(r, c) else special_result(r, c))
        for c in range(num_columns)], range(num_rows))
    """make matrix for result.

    Note: ``special_case`` Must be lambda function accept 2 arguments:
     ``row`` is from range number rows of matrix and
     ``column`` is from range number columns of matrix,
     Then return bool.

    Note: ``special_result`` Must be lambda function accept 2 argument:
     `row` is from ``range_rows`` and `column` is from ``range_columns``.
     and return Number (float or integer)
    """
    ##### check
    is_index = lambda x: isinstance(x, AnyIndex_Tuple)
    if (not all(map(is_index, tuple_index))) or len(tuple_index) != 2:
        raise TypeError(EM_NOT_TUPLE_INDEX % tuple_index)
    ##### end check
    index1, index2 = tuple_index
    if isinstance(index1, int):
        if isinstance(index2, int):
            is_in_case = lambda row, column: row == index1 and column == index2
            if isinstance(new_value, Numbers_Tuple):
                return make_matrix(is_in_case, lambda *args: new_value)
            else:
                raise TypeError(EM_WRONG_TYPE_FOR_INDEX % (
                    type(new_value), str(new_value), str(tuple_index)))
        else:  # second index are slice
            item_range = range(num_columns)[index2]
            length_lst_items = len(item_range)
            is_in_case = lambda row, column: row == index1 and (
                    column in item_range)
            if isinstance(new_value, Numbers_Tuple):
                return make_matrix(is_in_case, lambda *args: new_value)
            elif isinstance(new_value, Sequence):
                length_value = len(new_value)
                if is_contain_only(new_value, Numbers_Tuple):  # Vector
                    ##### check
                    if length_lst_items != length_value:
                        raise ValueError(EM_WRONG_VECTOR_LENGTH % (
                            length_lst_items, length_value, str(new_value)))
                    ##### end check
                    return make_matrix(is_in_case, lambda _, column: new_value[
                        item_range.index(column)])
                else:  # Matrix
                    columns_value = len(new_value[0])
                    ##### end check
                    if (length_lst_items != 1
                            or columns_value != length_lst_items):
                        raise ValueError(EM_WRONG_MATRIX_SIZE % (
                            1, length_lst_items, length_value, columns_value,
                            str(new_value)))
                    ##### end check
                    return make_matrix(is_in_case,
                                       lambda _, column: new_value[0][
                                           item_range.index(column)])
            else:
                raise TypeError(EM_WRONG_TYPE_FOR_INDEX % (
                    type(new_value), str(new_value), str(tuple_index)))
    else:  # first index are slice
        lst_items_range = range(num_rows)[index1]
        length_lst_items = len(lst_items_range)
        if isinstance(index2, int):
            is_in_case = lambda row, column: ((row in lst_items_range)
                                              and (column == index2))
            if isinstance(new_value, Numbers_Tuple):
                return make_matrix(is_in_case, lambda *args: new_value)
            elif isinstance(new_value, Sequence):
                length_value = len(new_value)
                if is_contain_only(new_value, Numbers_Tuple):  # Vector
                    ##### check
                    if length_lst_items != length_value:
                        raise ValueError(EM_WRONG_VECTOR_LENGTH % (
                            length_value, length_lst_items, str(new_value)))
                    ##### end check
                    return make_matrix(is_in_case, lambda row, _: new_value[
                        lst_items_range.index(row)])
                else:  # Matrix
                    columns_value = len(new_value[0])
                    ##### check
                    if length_lst_items != length_value or columns_value != 1:
                        raise ValueError(EM_WRONG_MATRIX_SIZE % (
                            length_lst_items, 1, length_value, columns_value,
                            str(new_value)))
                    ##### end check
                    return make_matrix(is_in_case, lambda row, _:
                    new_value[lst_items_range.index(row)][0])
            else:
                raise TypeError(EM_WRONG_TYPE_FOR_INDEX % (
                    type(new_value), str(new_value), str(tuple_index)))
        else:  # second index are slice
            item_range = range(num_columns)[index2]
            length_items = len(item_range)
            is_in_case = lambda row, column: ((row in lst_items_range)
                                              and (column in item_range))
            if isinstance(new_value, Numbers_Tuple):
                return make_matrix(is_in_case, lambda *args: new_value)
            elif isinstance(new_value, Sequence):
                length_value = len(new_value)
                if is_contain_only(new_value, Numbers_Tuple):  # Vector
                    ##### check
                    if length_items != length_value:
                        raise ValueError(EM_WRONG_VECTOR_LENGTH % (
                            length_value, length_items, str(new_value)))
                    ##### end check
                    return make_matrix(is_in_case, lambda _, column: new_value[
                        item_range.index(column)])
                else:  # Matrix
                    columns_value = len(new_value[0])
                    ##### check
                    if (length_lst_items != length_value
                            or length_items != columns_value):
                        raise ValueError(EM_WRONG_MATRIX_SIZE % (
                            length_lst_items, length_items, length_value,
                            columns_value, str(new_value)))
                    ##### end check
                    return make_matrix(is_in_case, lambda row, column:
                    new_value[lst_items_range.index(row)][
                        item_range.index(column)])
            else:
                raise TypeError(EM_WRONG_TYPE_FOR_INDEX % (
                    type(new_value), str(new_value), str(tuple_index)))


def matrix_setitem(any_matrix, index, new_value):
    """Return a new Matrix after changing values from index (integer Or slice)
     tuple of 2 index (integers Or/And slices).

    Info: this allows to use matrix like NumPy array :].

    Examples:

    >>> m1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> result1 = matrix_setitem(m1, 2, 1)
    >>> print(list(result1))
    [[1, 2, 3, 4], [5, 6, 7, 8], [1, 1, 1, 1], [13, 14, 15, 16]]
    >>> result2 = matrix_setitem(m1, 2, [100, 10, 140, 300])
    >>> print(list(result2))
    [[1, 2, 3, 4], [5, 6, 7, 8], [100, 10, 140, 300], [13, 14, 15, 16]]
    >>> result3 = matrix_setitem(m1, 2, [[80, 10, 40, 30]])
    >>> print(list(result3))
    [[1, 2, 3, 4], [5, 6, 7, 8], [80, 10, 40, 30], [13, 14, 15, 16]]
    >>> result4 = matrix_setitem(m1, 2, [[80], [10], [40], [30]])
    >>> print(list(result4))
    [[1, 2, 3, 4], [5, 6, 7, 8], [80, 10, 40, 30], [13, 14, 15, 16]]
    >>>  ############### Slice
    >>> result5 = matrix_setitem(m1, slice(None, 2), 1)
    >>> print(list(result5))
    [[1, 1, 1, 1], [1, 1, 1, 1], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> result6 = matrix_setitem(m1, slice(None, 2), [10, 10, 140, 300])
    >>> print(list(result6))
    [[10, 10, 140, 300], [10, 10, 140, 300], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> m2 = [[8, 10, 40, 30], [9.1, 10.5, 3.33, 1.9]]
    >>> result7 = matrix_setitem(m1, slice(None, 2), m2)
    >>> print(list(result7))
    [[8, 10, 40, 30], [9.1, 10.5, 3.33, 1.9], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> m1  # untouch :D
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> m2  # untouch :D
    [[8, 10, 40, 30], [9.1, 10.5, 3.33, 1.9]]
    >>> ##### Tuple Index
    >>> m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> result1 = matrix_setitem(m1, (2, 1), 100)
    >>> print(list(result1))
    [[1, 2, 3], [4, 5, 6], [7, 100, 9]]
    >>> result2 = matrix_setitem(m1, (2, slice(None, 2)), 100)
    >>> print(list(result2))
    [[1, 2, 3], [4, 5, 6], [100, 100, 9]]
    >>> result3 = matrix_setitem(m1, (2, slice(None, 2)), [-1, 9.4])
    >>> print(list(result3))
    [[1, 2, 3], [4, 5, 6], [-1, 9.4, 9]]
    >>> ########## First Slice
    >>> result4 = matrix_setitem(m1, (slice(None, 2), 1), -0.5)
    >>> print(list(result4))
    [[1, -0.5, 3], [4, -0.5, 6], [7, 8, 9]]
    >>> result5 = matrix_setitem(m1, (slice(None, 2), 1), [90, -90])
    >>> print(list(result5))
    [[1, 90, 3], [4, -90, 6], [7, 8, 9]]
    >>> result6 = matrix_setitem(m1, (slice(None, 2), 1), [[0.33], [0]])
    >>> print(list(result6))
    [[1, 0.33, 3], [4, 0, 6], [7, 8, 9]]
    >>> result7 = matrix_setitem(m1, (slice(None, 2), slice(None, 3)), -1)
    >>> print(list(result7))
    [[-1, -1, -1], [-1, -1, -1], [7, 8, 9]]
    >>> result8 = matrix_setitem(m1, (slice(None, 2), slice(None, 3)),
    ...                          [-1, -2, -3])
    >>> print(list(result8))
    [[-1, -2, -3], [-1, -2, -3], [7, 8, 9]]
    >>> result9 = matrix_setitem(m1, (slice(None, 2), slice(None, 3)),
    ...                          [[100, 9.3, 53], [8, -6, -1.1]])
    >>> print(list(result9))
    [[100, 9.3, 53], [8, -6, -1.1], [7, 8, 9]]
    >>> m1  # untouch :D
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    if isinstance(index, tuple):
        return _matrix_setitem_from_tuple(any_matrix, index, new_value)
    ##
    return _matrix_setitem_from_index(any_matrix, index, new_value)


def string_matrix(any_matrix):
    """make string of Any Matrix (Sequence of Sequences of Numbers) better.

    Examples:

    >>> matrix1 = [[1, 2, 3], [4, 5, 6]]
    >>> print(string_matrix(matrix1))
    [[1, 2, 3],
     [4, 5, 6]]
    """
    return str(any_matrix).replace("],", "],\n")


def string_format_matrix(any_matrix, format_spec):
    """make string format of Any Matrix (Sequence of Sequences of Numbers).

    Examples:

    >>> matrix1 = [[1, 2, 3], [4, 5, 6]]
    >>> print(string_format_matrix(matrix1, ".2f"))
    [[1.00, 2.00, 3.00],
     [4.00, 5.00, 6.00]]
    """
    values_format = [format(c, format_spec) for row in any_matrix for c in row]
    columns = [("%s, " % v if i % len(any_matrix[0]) else "%s],\n [" % v) for
               i, v in enumerate(values_format[:-1], start=1)]
    columns.append(values_format[-1])
    return "[[%s]]" % "".join(columns)


def size_matrix(any_matrix):
    """Return size of any Matrix in a Tuple (Rows, Columns)."""
    return len(any_matrix), len(any_matrix[0])


def trace_matrix(any_matrix):
    """Return trace of any Matrix.
     The "trace" in linear algebra is sum of the values diagonally on Matrix.
     (like: a0_0 + a1_1 + a2_2 + ...)

    Info: https://en.wikipedia.org/wiki/Trace_(linear_algebra)
    """
    min_length = min(len(any_matrix), len(any_matrix[0]))
    return sum(map(lambda index: any_matrix[index][index], range(min_length)))


def determinant_matrix(any_matrix):
    """Return determinant of any square Matrix NxN (Rows x Columns).

    Warning: if Matrix is NOT a Square Matrix NxN. it will raise ValueError.

    Info: Using Cofactor expansion formula (recursive).

    Info: https://en.wikipedia.org/wiki/Determinant
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    ##### check
    if num_rows != num_columns:
        raise ValueError(
            EM_NOT_SQUARE_MATRIX % (num_rows, num_columns, str(any_matrix)))
    ##### end check
    if num_rows == 1:
        return any_matrix[0][0]
    elif num_rows == 2:
        return ((any_matrix[0][0] * any_matrix[1][1])
                - (any_matrix[0][1] * any_matrix[1][0]))
    else:
        c_func = lambda j: pow(-1, j) * determinant_matrix(
            [merge_iterables(v[:j], v[j + 1:]) for v in any_matrix[1:]])
        ## remove first row and column j
        return sum(map(lambda column: any_matrix[0][column] * c_func(column),
                       range(num_columns)))


def matrix_from_vector(vector, size):
    """convert Any Vector To a Matrix size of MxN (rows x columns).

    Warning: ``vector`` Must have same length of `rows * columns`.
     Or it will raise IndexError.

    Examples:

    >>> vector1 = [0, 1, 0, 0, 1, 2]
    >>> result1 = matrix_from_vector(vector1, (2, 3))
    >>> print(list(result1))
    [[0, 1, 0], [0, 1, 2]]
    >>> result2 = matrix_from_vector(vector1, (3, 2))
    >>> print(list(result2))
    [[0, 1], [0, 0], [1, 2]]
    >>> vector2 = [0, 1, 0, -4, 0, 1, 2, 3, 1, 2, 7, 10, 9, 7, -1, 0]
    >>> result3 = matrix_from_vector(vector2, (4, 4))
    >>> print(list(result3))
    [[0, 1, 0, -4], [0, 1, 2, 3], [1, 2, 7, 10], [9, 7, -1, 0]]
    >>> result4 = matrix_from_vector(vector2, (2, 8))
    >>> print(list(result4))
    [[0, 1, 0, -4, 0, 1, 2, 3], [1, 2, 7, 10, 9, 7, -1, 0]]
    """
    num_rows, num_columns = size
    ##### check
    expect_length = num_rows * num_columns
    if len(vector) != expect_length:
        raise IndexError(EM_WRONG_VECTOR_LENGTH % (
            expect_length, len(vector), str(vector)))
    ##### end check
    return map(lambda i: vector[i:i + num_columns],
               range(0, num_rows * num_columns, num_columns))


def matrix_identity(n):
    """Return identity of Matrix NxN (square of ``n``).

    Warning: ``n`` Must be an integer (>0), or it will raise ValueError.

    Examples:

    >>> martix1 = matrix_identity(1)
    >>> print(list(martix1))
    [[1]]
    >>> matrix2 = matrix_identity(2)
    >>> print(list(matrix2))
    [[1, 0], [0, 1]]
    >>> matrix3 = matrix_identity(3)
    >>> print(list(matrix3))
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    >>> matrix4 = matrix_identity(4)
    >>> print(list(matrix4))
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    """
    ##### check
    if n <= 0 or not isinstance(n, int):
        raise ValueError(EM_NOT_EXPECTED % ("a Positive integer (>0)", n))
    ##### end check
    return map(lambda i: [int(i == j) for j in range(n)], range(n))


def matrix_adjugate(any_matrix):
    """Return adjugate of any square Matrix NxN (Rows x Columns).

    Warning: if Matrix is NOT a Square Matrix NxN. it will raise ValueError.

    Info: https://en.wikipedia.org/wiki/Adjugate_matrix
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    ##### check
    if num_rows != num_columns:
        raise ValueError(
            EM_NOT_SQUARE_MATRIX % (num_rows, num_columns, str(any_matrix)))
    ##### end check
    c_func = lambda i, j: pow(-1, i + j) * determinant_matrix(
        [merge_iterables(v[:j], v[j + 1:]) for v in
         merge_iterables(any_matrix[:i], any_matrix[i + 1:])])
    ## remove row i and column j.
    return map(lambda column: [c_func(row, column) for row in range(num_rows)],
               range(num_columns))


def matrix_transpose(any_matrix):
    """Return transposed Matrix.
     The "transpose" a Matrix is swap the rows with columns.

    Info: https://www.mathsisfun.com/algebra/matrix-introduction.html

    Examples:

    >>> m1 = [[6, 4, 24], [1, -9, 8]]
    >>> m1_t = list(matrix_transpose(m1))
    >>> print(m1_t)
    [[6, 1], [4, -9], [24, 8]]
    >>> print(list(matrix_transpose(m1_t)))
    [[6, 4, 24], [1, -9, 8]]
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    return map(
        lambda column: [any_matrix[row][column] for row in range(num_rows)],
        range(num_columns))


def matrix_inv(any_matrix):
    """Return inverse of any square Matrix NxN (Rows x Columns).

    Warning: if matrix is singular (don't have inverse) that is in case its
     determinant Equal To 0. it will raise ValueError.
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    det = determinant_matrix(any_matrix)
    ##### check
    if num_rows != num_columns:
        raise ValueError(
            EM_NOT_SQUARE_MATRIX % (num_rows, num_columns, str(any_matrix)))
    if det == 0:
        raise ValueError(("Matrix is singular (det = 0), no inverse exists"
                          " of `%s`") % str(any_matrix))
    ##### end check
    matrix_adj = list(matrix_adjugate(any_matrix))
    return map(lambda row: [matrix_adj[row][column] / det
                            for column in range(num_columns)], range(num_rows))


def matrix_round(any_matrix, ndigits=None):
    """Return Matrix after round all Numbers (float or integer)."""
    return map(lambda row: [round(c, ndigits=ndigits) for c in row], any_matrix)


def matrix_ceil(any_matrix):
    """Return Matrix after ceil all Numbers (float or integer)."""
    return map(lambda row: [math.ceil(c) for c in row], any_matrix)


def matrix_floor(any_matrix):
    """Return Matrix after floor all Numbers (float or integer)."""
    return map(lambda row: [math.floor(c) for c in row], any_matrix)


def matrix_negative(any_matrix):
    """Return Matrix change sign of all Numbers (float or integer).

    Info: https://www.mathsisfun.com/algebra/matrix-introduction.html

    Examples:

    >>> m1 = [[3, 8], [4, 6]]
    >>> print(list(matrix_negative(m1)))
    [[-3, -8], [-4, -6]]
    >>> m2 = [[2, -1, 4], [0, 13, -1]]
    >>> print(list(matrix_negative(m2)))  #Note: -0 is same as 0
    [[-2, 1, -4], [0, -13, 1]]
    """
    num_rows = len(any_matrix)
    num_columns = len(any_matrix[0])
    return map(lambda row: [-any_matrix[row][column]
                            for column in range(num_columns)], range(num_rows))


def matrix_abs(any_matrix):
    """Return absolute of any Matrix.

    Examples:

    >>> m1 = [[3, -8.1], [4, -6]]
    >>> print(list(matrix_abs(m1)))
    [[3, 8.1], [4, 6]]
    >>> m2 = [[2, -1, 4], [0, 13, -1]]
    >>> print(list(matrix_abs(m2)))  #Note: -0 is same as 0
    [[2, 1, 4], [0, 13, 1]]
    """
    return map(lambda row: [abs(column) for column in row], any_matrix)


def matrix_zero(size):
    """Return Matrix full of 0 of giving size (Row x Columns)."""
    return map(lambda _: [0] * size[1], range(size[0]))


############### Matrix Simple Operations
def matrix_add_matrices(*any_matrices):
    """Addition between Matrices (all must have same sizes).

    Info: https://www.mathsisfun.com/algebra/matrix-introduction.html

    Examples:

    >>> m1 = [[3, 8], [4, 6]]
    >>> m2 = [[4, 0], [1, -9]]
    >>> print(list(matrix_add_matrices(m1, m2)))
    [[7, 8], [5, -3]]
    >>> m3 = [[2, -1, 4], [0, 13, -1]]
    >>> m4 = [[4, 0, 10], [12, -19, 3]]
    >>> print(list(matrix_add_matrices(m3, m4)))
    [[6, -1, 14], [12, -6, 2]]
    >>> m5 = [[1, 2], [3, 4]]
    >>> print(list(matrix_add_matrices(m1, m2, m5)))
    [[8, 10], [8, 1]]
    """
    num_rows = len(any_matrices[0])
    num_columns = len(any_matrices[0][0])
    func_add = lambda r, c: sum(map(lambda matrix: matrix[r][c], any_matrices))
    return map(lambda row: [func_add(row, column)
                            for column in range(num_columns)], range(num_rows))


def matrix_sub_matrices(*any_matrices):
    """Subtraction between Matrices. (all must have same sizes).

    Info: https://www.mathsisfun.com/algebra/matrix-introduction.html

    Examples:

    >>> m1 = [[3, 8], [4, 6]]
    >>> m2 = [[4, 0], [1, -9]]
    >>> print(list(matrix_sub_matrices(m1, m2)))
    [[-1, 8], [3, 15]]
    >>> m3 = [[2, -1, 4], [0, 13, -1]]
    >>> m4 = [[4, 0, 10], [12, -19, 3]]
    >>> print(list(matrix_sub_matrices(m3, m4)))
    [[-2, -1, -6], [-12, 32, -4]]
    >>> m5 = [[1, 2], [3, 4]]
    >>> print(list(matrix_sub_matrices(m1, m2, m5)))
    [[-2, 6], [0, 11]]
    """
    num_rows = len(any_matrices[0])
    num_columns = len(any_matrices[0][0])
    func_sub = lambda r, c: any_matrices[0][r][c] - sum(
        map(lambda matrix: matrix[r][c], any_matrices[1:]))
    return map(lambda row: [func_sub(row, column)
                            for column in range(num_columns)], range(num_rows))


def matrix_mul_matrix(matrix1, matrix2):
    """Multiplication between 2 Matrices.

    Warning: First Matrix Must have same Number of Row be same as Number of
     Columns of Second Matrix. Or it will raise IndexError.

    Info: https://www.mathsisfun.com/algebra/matrix-multiplying.html

    Examples:

    >>> m1 = [[1, 2, 3], [4, 5, 6]]
    >>> m2 = [[7, 8], [9, 10], [11, 12]]
    >>> print(list(matrix_mul_matrix(m1, m2)))
    [[58, 64], [139, 154]]
    >>> print(list(matrix_mul_matrix(m2, m1)))
    [[39, 54, 69], [49, 68, 87], [59, 82, 105]]
    >>> m3 = [[4], [5], [6]]
    >>> m4 = [[1, 2, 3]]
    >>> print(list(matrix_mul_matrix(m3, m4)))
    [[4, 8, 12], [5, 10, 15], [6, 12, 18]]
    """
    max_length = max(len(matrix1), len(matrix2[0]))
    get_column = lambda index: [row[index] for row in matrix2]
    func_dot_product = lambda v1, v2: sum(map(lambda x1, x2: (x1 * x2), v1, v2))
    return map(lambda row: [func_dot_product(matrix1[row], get_column(column))
                            for column in range(max_length)], range(max_length))


def matrix_mul_vector(any_vector, any_matrix):
    """Multiplication between Vector and Matrix.

    Info: https://www.mathsisfun.com/algebra/matrix-multiplying.html

    Examples:

    >>> v1 = [1, 2, 3]
    >>> m1 = [[4], [5], [6]]
    >>> print(list(matrix_mul_vector(v1, m1)))
    [32]
    """
    num_columns = len(any_matrix[0])
    get_column = lambda index: [row[index] for row in any_matrix]
    func_dot_product = lambda v1, v2: sum(map(lambda x1, x2: (x1 * x2), v1, v2))
    return map(lambda column: func_dot_product(any_vector, get_column(column)),
               range(num_columns))


def matrix_mul_value(value, any_matrix):
    """Multiplication between a Number (float or integer) and Matrix.

    Info: https://www.mathsisfun.com/algebra/matrix-multiplying.html

    Examples:

    >>> n1 = 10
    >>> m1 = [[1, 2, 3], [4, 5, 6]]
    >>> print(list(matrix_mul_value(n1, m1)))
    [[10, 20, 30], [40, 50, 60]]
    """
    return map(lambda row: [column * value for column in row], any_matrix)


def matrix_truediv_matrix(any_matrix1, any_matrix2):
    """True Division between 2 Matrices.

    Warning: ``any_matrix1`` and ``any_matrix2`` Must have same size.
     Or it will raise IndexError.

    Warning: ``any_matrix2`` Must NOT be singular (don't have inverse)
     that is in case its determinant Equal To 0. it will raise ValueError.

    Info: https://www.mathsisfun.com/algebra/matrix-introduction.html

    Examples:

    >>> m1 = [[7, 8], [9, 10]]
    >>> m2 = [[1, 2], [3, 4]]
    >>> result1 = matrix_truediv_matrix(m1, m2)
    >>> print(list(result1))
    [[-2.0, 3.0], [-3.0, 4.0]]
    >>> m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> m4 = [[-2, 2, 0], [1, 1, 0], [4, 5, -1]]
    >>> result2 = matrix_truediv_matrix(m3, m4)
    >>> print(list(result2))
    [[1.0, 15.0, -3.0], [1.75, 31.5, -6.0], [2.5, 48.0, -9.0]]
    >>> result3 = matrix_truediv_matrix(m4, m4)
    >>> print(list(result3))
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    """
    return matrix_mul_matrix(any_matrix1, list(matrix_inv(any_matrix2)))


############################# Matrix 3x3
def matrix_3x3_from_x_rotation(angle, transpose=False):
    """Creates a Matrix with the specified rotation about the X-axis.
     Return A Matrix (3x3) with the rotation about the X-axis (but as a List).

    Note: ``angle`` is angle of rotation (in radians) in X-axis.

    Note: ``transpose`` (by default False)
    | * if it's False, the result of Matrix (3x3) will be:
    | [[1,         0,          0],
    |  [0, cos_angle, -sin_angle],
    |  [0, sin_angle,  cos_angle]]
    | * If it's True, the result of Matrix (3x3) will be:
    | [[1,          0,          0],
    |  [0,  cos_angle,  sin_angle],
    |  [0, -sin_angle,  cos_angle]]
    """
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    if transpose:
        return [[1, 0, 0],
                [0, cos_angle, sin_angle],
                [0, -sin_angle, cos_angle]]
    else:
        return [[1, 0, 0],
                [0, cos_angle, -sin_angle],
                [0, sin_angle, cos_angle]]


def matrix_3x3_from_y_rotation(angle, transpose=False):
    """Creates a Matrix with the specified rotation about the Y-axis.
     Return A Matrix (3x3) with the rotation about the Y-axis (but as a List).

    Note: ``angle`` is angle of rotation (in radians) in Y-axis.

    Note: ``transpose`` (by default False)
    | * if it's False, the result Matrix (3x3) will be:
    | [[ cos_angle,  0,  sin_angle],
    |  [         0,  1,          0],
    |  [-sin_angle,  0,  cos_angle]]
    | * if it's True, the result Matrix (3x3) will be:
    | [[cos_angle,  0, -sin_angle],
    |  [        0,  1,          0],
    |  [sin_angle,  0,  cos_angle]]
    """
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    if transpose:
        return [[cos_angle, 0, -sin_angle],
                [0, 1, 0],
                [sin_angle, 0, cos_angle]]
    else:
        return [[cos_angle, 0, sin_angle],
                [0, 1, 0],
                [-sin_angle, 0, cos_angle]]


def matrix_3x3_from_z_rotation(angle, transpose=False):
    """Creates a Matrix with the specified rotation about the Z-axis.
     Return A Matrix (3x3) with the rotation about the Z-axis (but as a List).

    Note: ``angle`` is angle of rotation (in radians) in Z-axis.

    Note: ``transpose`` (by default False)
    | * if it's False, the result Matrix (3x3) will be:
    | [[cos_angle, -sin_angle,  0],
    |  [sin_angle,  cos_angle,  0],
    |  [        0,          0,  1]]
    | * if it's True, the result Matrix (3x3) will be:
    | [[ cos_angle,  sin_angle,  0],
    |  [-sin_angle,  cos_angle,  0],
    |  [         0,          0,  1]]
    """
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    if transpose:
        return [[cos_angle, sin_angle, 0],
                [-sin_angle, cos_angle, 0],
                [0, 0, 1]]
    else:
        return [[cos_angle, -sin_angle, 0],
                [sin_angle, cos_angle, 0],
                [0, 0, 1]]


def matrix_3x3_from_euler(yaw, pitch, roll, order):
    """Convert Euler Angles (yaw, pitch, roll) To Matrix (3x3).
     Return A Matrix (3x3) as List.

    Warning: ``yaw`` and ``pitch`` and ``roll`` all in radians.
     also be Careful about Gimbal Lock.

    Warning: ``order`` must be string for order axis rotation for Euler angles
     (a.k.a. Tait–Bryan angles) either uppercase or lowercase or mixed
     (e.g. 'xyz', 'XYZ', 'XyZ', 'ZYX', 'zyx', 'Zyx', etc...).
     or it will raise ValueError.
    """
    order = order.upper()
    if order not in EulerAnglesOrders:
        raise ValueError(EM_UNSUPPORTED_ORDER_EULER % order)
    ##
    gimbal_lock = isclose(pitch % pi / 2, 0, abs_tol=epsilon)
    pitch = pitch if not gimbal_lock else math.copysign(pi / 2, pitch)
    c_y, s_y = math.cos(yaw), math.sin(yaw)
    c_p, s_p = math.cos(pitch), math.sin(pitch)
    c_r, s_r = math.cos(roll), math.sin(roll)
    ## Start X
    if order == "XYZ":
        return [[c_p * c_r, -c_p * s_r, s_p],
                [(c_y * s_r) + (s_y * s_p * c_r),
                 (c_y * c_r) - (s_y * s_p * s_r), -s_y * c_p],
                [(s_y * s_r) - (c_y * s_p * c_r),
                 (s_y * c_r) + (c_y * s_p * s_r), c_y * c_p]]
    elif order == "XZY":
        return [[c_p * c_r, -s_p, c_p * s_r],
                [(c_y * s_p * c_r) + (s_y * s_r), c_y * c_p,
                 (c_y * s_p * s_r) - (s_y * c_r)],
                [(s_y * s_p * c_r) - (c_y * s_r), s_y * c_p,
                 (s_y * s_p * s_r) + (c_y * c_r)]]
    ## Start Y
    elif order == "YXZ":
        return [[(s_y * s_p * s_r) + (c_y * c_r),
                 (s_y * s_p * c_r) - (c_y * s_r), s_y * c_p],
                [c_p * s_r, c_p * c_r, -s_p],
                [(c_y * s_p * s_r) - (s_y * c_r),
                 (c_y * s_p * c_r) + (s_y * s_r), c_y * c_p]]
    elif order == "YZX":
        return [[c_y * c_p, (s_y * s_r) - (c_y * s_p * c_r),
                 (s_y * c_r) + (c_y * s_p * s_r)],
                [s_p, c_p * c_r, -c_p * s_r],
                [-s_y * c_p,
                 (c_y * s_r) + (s_y * s_p * c_r),
                 (c_y * c_r) - (s_y * s_p * s_r)]]
    ## Start Z
    elif order == "ZYX":
        return [[c_y * c_p, (c_y * s_p * s_r) - (s_y * c_r),
                 (c_y * s_p * c_r) + (s_y * s_r)],
                [c_y * c_p, (s_y * s_p * s_r) + (c_y * c_r),
                 (s_y * s_p * c_r) - (c_y * s_r)],
                [-s_p, c_p * s_r, c_p * c_r]]
    else:  # ZXY
        return [[(c_y * c_r) - (s_y * s_p * s_r), -s_y * c_p,
                 (c_y * s_r) + (s_y * s_p * c_r)],
                [(s_y * c_r) + (c_y * s_p * s_r), c_y * c_p,
                 (s_y * s_p) - (c_y * s_p * c_r)],
                [-s_y * c_p, s_p, c_p * c_r]]


def matrix_3x3_from_axis_angle(axis, angle):
    """Convert Axis (x, y, z) and Angle (in radians) To a Matrix (3x3).
     Return A Matrix (3x3) as List with the angle rotation around an axis.

    Note: ``axis`` is normalized in function.
    """
    x, y, z = tuple(vector_normalize(axis))
    c = math.cos(angle)
    s = math.sin(angle)
    t = 1 - c
    return [[(x ** 2 * t) + c, (y * x * t) + (z * s), (z * x * t) - (y * s)],
            [(x * y * t) - (z * s), (y ** 2 * t) + c, (z * y * t) + (x * s)],
            [(x * z * t) + (y * s), (y * z * t) - (x * s), (z ** 2 * t) + c]]


def matrix_3x3_from_quaternion(quaternion):
    """Convert a Quaternion (x, y, z, w) To Matrix (3x3).
     Return A Matrix (3x3) as List with the Quaternion's rotation.

    Warning: Be CAREFUL with ZeroDivision (in case Quaternion Equal To 0).

    Note: ``quaternion`` is normalized in function.

    Info: http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
    """
    x, y, z, w = tuple(vector_normalize(quaternion))
    x_2, y_2, z_2, w_2 = x ** 2, y ** 2, z ** 2, w ** 2
    ##
    x_y, x_z, x_w = x * y, x * z, x * w
    y_z, y_w = y * z, y * w
    z_w = z * w
    ##
    inv = 1 / (x_2 + y_2 + z_2 + w_2)
    return [[(x_2 - y_2 - z_2 + w_2) * inv, 2.0 * (x_y - z_w) * inv,
             2.0 * (x_z + y_w) * inv],
            [2.0 * (x_y + z_w) * inv, (-x_2 + y_2 - z_2 + w_2) * inv,
             2.0 * (y_z - x_w) * inv],
            [2.0 * (x_z - y_w) * inv, 2.0 * (y_z + x_w) * inv,
             (-x_2 - y_2 + z_2 + w_2) * inv]]


def matrix_3x3_from_scale(scale_v3):
    """Creates an identity Matrix with the scale (x, y, z) set.
     Return A Matrix (3x3) as List with the scale set to the specified vector3.
    """
    return [[scale_v3[0], 0, 0],
            [0, scale_v3[1], 0],
            [0, 0, scale_v3[2]]]


def matrix_3x3_from_direction_scale(direction_v3, scale):
    """Creates a Matrix which can apply a directional scaling to vectors.
     Return a Matrix (3x3) as List know as scaling Matrix.

    Warning: ``direction_v3`` Must be any Vector3 (x, y, z).
    """
    magnitude_sq = sum(map(lambda x1: x1 ** 2, direction_v3))
    if isclose(magnitude_sq, 1) or not magnitude_sq:  # normalized or zero
        x, y, z = direction_v3
    else:
        x, y, z = [x / (magnitude_sq ** 0.5) for x in direction_v3]
    scale -= 1
    return [[1 + (scale * (x ** 2)), scale * x * (y ** 2), scale * x * z],
            [scale * x * y, 1 + (scale * y), scale * y * z],
            [scale * x * z, scale * y * z, 1 + (scale * (z ** 2))]]


############################# Matrix 4x4
def matrix_4x4_look_at(eye, target, up, transpose=False):
    """Creates a look at Matrix (4x4) according to OpenGL standards.
     Return A Matrix (4x4) as List that can be used as a view Matrix.

    Warning: ``eye`` and ``target`` and ``up`` all Must be any Vector3(x, y, z).

    Note: ``transpose`` (by default False).
    | * if it's False, Return Matrix according to OpenGL standards.
    | * if it's True, Return transpose of it.
    """
    forward = list(vector_normalize([target[i] - eye[i] for i in range(3)]))
    side = list(vector_normalize(cross_product_v3(forward, up)))
    up = list(vector_normalize(cross_product_v3(side, forward)))
    ##
    side_eye = dot_product_vectors(side, eye)
    up_eye = dot_product_vectors(up, eye)
    forward_eye = dot_product_vectors(forward, eye)
    if transpose:
        return [[side[0], side[1], side[2], -side_eye],
                [up[0], up[1], up[2], -up_eye],
                [-forward[0], -forward[1], -forward[2], forward_eye],
                [0, 0, 0, 1]]
    else:
        return [[side[0], up[0], -forward[0], 0],
                [side[1], up[1], -forward[1], 0],
                [side[2], up[2], -forward[2], 0],
                [-side_eye, -up_eye, forward_eye, 1]]


def matrix_4x4_perspective_projection_bounds(left, right, bottom, top, near,
                                             far, transpose=False):
    """Creates perspective projection Matrix using the specified bounds.
     Return a projection Matrix (4x4) as List representing the perspective.

    Note: ``transpose`` (by default False)
    | * if it's False, result Matrix (4x4) will be:
    | [[A, 0, 0,  0],   # A = 2*near/(right-left)
    |  [0, B, 0,  0],   # B = 2*near/(top-bottom); C = (right+left)/(right-left)
    |  [C, D, E, -1],   # D = (top+bottom)/(top-bottom)
    |  [0, 0, f,  0]]   # E = -(far+near)/(far-near); F = -2*far*near/(far-near)
    | * if it's True, result Matrix (4x4) will be (just transpose it :d):
    | [[A, 0,  C, 0],
    |  [0, B,  D, 0],
    |  [0, 0,  E, F],
    |  [0, 0, -1, 0]]
    """
    a = (2 * near) / (right - left)
    b = (2 * near) / (top - bottom)
    c = (right + left) / (right - left)
    d = (top + bottom) / (top - bottom)
    e_ = -(far + near) / (far - near)  # adding `_` for `e` math variable
    f = -(2 * far * near) / (far - near)
    if transpose:
        return [[a, 0, c, 0],
                [0, b, d, 0],
                [0, 0, e_, f],
                [0, 0, -1, 0]]
    else:
        return [[a, 0, 0, 0],
                [0, b, 0, 0],
                [c, d, e_, -1],
                [0, 0, f, 0]]


def matrix_4x4_perspective_projection(angle, aspect, near, far,
                                      transpose=False):
    """Creates perspective projection Matrix.
     Return A projection Matrix (4x4) as List representing the perspective.

    Warning: ``angle`` Must be in radians.

    Warning: all of ``aspect`` and ``near`` and ``far`` Must be Positive
     Numbers (float or integer) (>0). also``near`` Must be Less Than ``far``.
     Or it will raise ValueError.

    Note: ``transpose`` (by default False)
    | * if it's False, result Matrix (4x4) will be:
    | [[A, 0, 0,  0],   # A = 1 / (tan(angle/2) * aspect)
    |  [0, B, 0,  0],   # B = 1/tan(angle/2); C = 1/(2*near*tan(angle/2)*aspect)
    |  [C, D, E, -1],   # D = 1 / (2 * near * tan(angle / 2))
    |  [0, 0, F,  0]]   # E = -(far+near)/(far-near); F = -2*far*near/(far-near)
    | * if it's True, result Matrix (4x4) will be (just transpose it):
    | [[A, 0,  C, 0],
    |  [0, B,  D, 0],
    |  [0, 0,  E, F],
    |  [0, 0, -1, 0]]
    """
    if (aspect <= 0) or (near <= 0) or (far <= 0):
        got = "aspect=%f, near=%f, far=%f" % (aspect, near, far)
        raise ValueError(EM_NOT_EXPECTED % ("Values be Positive >0", got))
    if near >= far:
        got = "near=%f, far=%f" % (near, far)
        raise ValueError(EM_NOT_EXPECTED % ("`near` be Less Than `far`", got))
    ##
    y_max = near * math.tan((angle % tau) / 2)
    x_max = y_max * aspect
    return matrix_4x4_perspective_projection_bounds(-x_max, x_max, -y_max,
                                                    y_max, near, far,
                                                    transpose=transpose)


def matrix_4x4_from_translation(translation, transpose=False):
    """Creates an identity Matrix with the translation.
     Return A Matrix (4x4) as List with the translation from specified Vector3.

    Note: ``transpose`` (by default False)
    | * if it's False, result Matrix (4x4) will be:
    | [[1, 0, 0, 0],
    |  [0, 1, 0, 0],
    |  [0, 0, 1, 0],
    |  [translation[0], translation[1], translation[2], 1]]
    | * if it's True, result Matrix (4x4) will be (just transpose it):
    | [[1, 0, 0, translation[0]],
    |  [0, 1, 0, translation[1]],
    |  [0, 0, 1, translation[2]],
    |  [0, 0, 0, 1]]
    """
    if transpose:
        return [[1, 0, 0, translation[0]],
                [0, 1, 0, translation[1]],
                [0, 0, 1, translation[2]],
                [0, 0, 0, 1]]
    else:
        return [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [translation[0], translation[1], translation[2], 1]]


############################# Check Collisions 2D ##############################
def is_collision_point_line_2d(point, start_line, end_line):
    """Return True if Point is collided with Line in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/line-point

    Side Note: here not using another value for checking if point near line.
    """
    func_distance_sq = lambda x1, x2: (x1 - x2) ** 2
    d1 = sum(map(func_distance_sq, point, start_line)) ** 0.5
    d2 = sum(map(func_distance_sq, point, end_line)) ** 0.5
    return d1 + d2 == sum(map(func_distance_sq, start_line, end_line)) ** 0.5


def is_collision_line_line_2d(start_line1, end_line1, start_line2, end_line2):
    """Return True if Line1 is collided with Line2 in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/line-line
    """
    get_cross_product = lambda v1, v2: (v1[0] * v2[1]) - (v1[1] * v2[0])
    line_v1 = [end_line1[i] - start_line1[i] for i in range(2)]
    line_v2 = [end_line2[i] - start_line2[i] for i in range(2)]
    line_v3 = [start_line2[i] - start_line1[i] for i in range(2)]
    c = get_cross_product(line_v1, line_v2)
    a = get_cross_product(line_v3, line_v2)
    b = get_cross_product(line_v3, line_v1)
    if c >= 0:  # avoid division using math :D
        return (0 <= a <= c) and (0 <= b <= c)
    else:
        return (0 >= a >= c) and (0 >= b >= c)


def is_collision_point_circle_2d(point, circle_center, radius):
    """Return True if Point is collided with Circle in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/point-circle
    """
    func_distance_sq = lambda x1, x2: (x1 - x2) ** 2
    return sum(map(func_distance_sq, point, circle_center)) <= radius ** 2


def is_collision_line_circle_2d(start_line, end_line, circle_center, radius):
    """Return True if Line is collided with Circle in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/line-circle
    """
    line_v = [end_line[i] - start_line[i] for i in range(2)]
    magnitude_sq = sum(map(lambda x: x ** 2, line_v))
    if magnitude_sq:
        point_v = [circle_center[i] - start_line[i] for i in range(2)]
        func_mul = lambda x1, x2: x1 * x2
        t = max(0, min(1, sum(map(func_mul, line_v, point_v)) / magnitude_sq))
        closest_point = [start_line[i] + (t * line_v[i]) for i in range(2)]
    else:  # it's point not line
        closest_point = start_line
    func_dist_sq = lambda x1, x2: (x1 - x2) ** 2
    return sum(map(func_dist_sq, circle_center, closest_point)) <= radius ** 2


def is_collision_circle_circle_2d(circle_center1, radius1, circle_center2,
                                  radius2):
    """Return True if Circle1 is collided with Circle2 in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/circle-circle
    """
    func_dist_sq = lambda x1, x2: (x1 - x2) ** 2
    radius_sq = (radius1 + radius2) ** 2
    return sum(map(func_dist_sq, circle_center1, circle_center2)) <= radius_sq


def is_collision_point_rect_2d(point, rect_topleft, rect_width, rect_height):
    """Return True if Point is collided with Rectangle in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/point-rect
    """
    left_side, right_side = rect_topleft[0], rect_topleft[0] + rect_width
    down_side, up_side = rect_topleft[1] + rect_height, rect_topleft[1]
    return (left_side <= point[0] <= right_side and up_side <= point[
        1] <= down_side)


def is_collision_line_rect_2d(start_line, end_line, rect_topleft, rect_width,
                              rect_height):
    """Return True if Line is collided with Rectangle in 2D space.
     Otherwise, Return False.
    """
    left_side, right_side = rect_topleft[0], rect_topleft[0] + rect_width
    down_side, up_side = rect_topleft[1] + rect_height, rect_topleft[1]
    ## First check if any point of line in rectangle
    if (left_side <= start_line[0] <= right_side
            and up_side <= start_line[1] <= down_side):
        return True
    if (left_side <= end_line[0] <= right_side
            and up_side <= end_line[1] <= down_side):
        return True
    ## Now check if any lines collide
    rect_topright, rect_bottomleft, rect_bottomright = [
        (rect_topleft[0] + rect_width, rect_topleft[1]),
        (rect_topleft[0], rect_topleft[1] + rect_height),
        (rect_topleft[0] + rect_width, rect_topleft[1] + rect_height)]
    for start_line2, end_line2 in [(rect_topleft, rect_topright),
                                   (rect_topright, rect_bottomright),
                                   (rect_bottomright, rect_bottomleft),
                                   (rect_bottomleft, rect_topleft)]:
        get_cross_product = lambda v1, v2: (v1[0] * v2[1]) - (v1[1] * v2[0])
        line_v1 = [end_line[i] - start_line[i] for i in range(2)]
        line_v2 = [end_line2[i] - start_line2[i] for i in range(2)]
        line_v3 = [start_line2[i] - start_line[i] for i in range(2)]
        c = get_cross_product(line_v1, line_v2)
        a = get_cross_product(line_v3, line_v2)
        b = get_cross_product(line_v3, line_v1)
        if c >= 0:  # avoid division
            if (0 <= a <= c) and (0 <= b <= c):
                return True
        else:
            if (0 >= a >= c) and (0 >= b >= c):
                return True
    return False


def is_collision_circle_rect_2d(circle_center, radius, rect_topleft, rect_width,
                                rect_height):
    """Return True if Circle is collided with Rectangle in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/circle-rect
    """
    x = max(rect_topleft[0],
            min(circle_center[0], rect_topleft[0] + rect_width))
    y = max(rect_topleft[1],
            min(circle_center[1], rect_topleft[1] + rect_height))
    distance_sq = (circle_center[0] - x) ** 2 + (circle_center[1] - y) ** 2
    return distance_sq <= radius ** 2


def is_collision_rect_rect_2d(rect_topleft1, rect_width1, rect_height1,
                              rect_topleft2, rect_width2, rect_height2):
    """Return True if Rectangle1 is collided with Rectangle2 in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/rect-rect
    """
    left_side, right_side = (rect_topleft1[0] - rect_width2,
                             rect_topleft1[0] + rect_width1)
    down_side, up_side = (rect_topleft1[1] + rect_height1 - rect_height2,
                          rect_topleft1[1])
    return (left_side <= rect_topleft2[0] <= right_side
            and down_side <= rect_topleft2[1] <= up_side)


def is_collision_point_triangle_2d(point, p1_triangle, p2_triangle,
                                   p3_triangle):
    """Return True if Point is collided with Triangle in 2D space.
     Otherwise, Return False.

    Info: https://www.jeffreythompson.org/collision-detection/tri-point
    """
    point_v1 = [p1_triangle[i] - point[i] for i in range(2)]
    point_v2 = [p2_triangle[i] - point[i] for i in range(2)]
    point_v3 = [p3_triangle[i] - point[i] for i in range(2)]
    get_cross_product = lambda v1, v2: (v1[0] * v2[1]) - (v1[1] * v2[0])
    area1 = get_cross_product(point_v1, point_v2)
    area2 = get_cross_product(point_v2, point_v3)
    area3 = get_cross_product(point_v3, point_v1)
    return area1 <= 0 and area2 <= 0 and area3 <= 0


def is_collision_line_triangle_2d(start_line, end_line, p1_triangle,
                                  p2_triangle, p3_triangle):
    """Return True if Line is collided with Triangle in 2D space.
     Otherwise, Return False.
    """
    line_v = [end_line[i] - start_line[i] for i in range(2)]
    point_v1 = [p1_triangle[i] - start_line[i] for i in range(2)]
    point_v2 = [p2_triangle[i] - start_line[i] for i in range(2)]
    point_v3 = [p3_triangle[i] - start_line[i] for i in range(2)]
    ## check if any point of triangle is in other side of line
    get_cross_product = lambda v1, v2: (v1[0] * v2[1]) - (v1[1] * v2[0])
    s1 = get_cross_product(point_v1, line_v)
    s2 = get_cross_product(point_v2, line_v)
    s3 = get_cross_product(point_v3, line_v)
    ## see which point of triangle is in other direction of line
    # to skip check if all point of triangle are in one side of line
    # because it's impossible triangle to collide with line in this case
    if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
        return False
    ## check one point of line if it's inside of triangle
    area1 = get_cross_product(point_v1, point_v2)
    area2 = get_cross_product(point_v2, point_v3)
    area3 = get_cross_product(point_v3, point_v1)
    if ((area1 <= 0 and area2 <= 0 and area3 <= 0) or (
            area1 >= 0 and area2 >= 0 and area3 >= 0)):
        return True
    ## Now check if lines collide (we only need check 2 line of triangle)
    # base on which point of triangle is in other side of line
    # because it's impossible for line collide with all 3 line of triangle
    if ((s1 <= 0 <= s2 and s3 >= 0) or (
            s1 >= 0 >= s2 and s3 <= 0)):  # p1_triangle
        t1_v = [p2_triangle[i] - p1_triangle[i] for i in range(2)]
        a1 = get_cross_product(point_v1, t1_v)
        t2_v = [p3_triangle[i] - p1_triangle[i] for i in range(2)]
        a2 = get_cross_product(point_v1, t2_v)
        b = s1
    elif ((s1 >= 0 >= s2 and s3 >= 0) or (
            s1 <= 0 <= s2 and s3 <= 0)):  # p2_triangle
        t1_v = [p1_triangle[i] - p2_triangle[i] for i in range(2)]
        a1 = get_cross_product(point_v2, t1_v)
        t2_v = [p3_triangle[i] - p2_triangle[i] for i in range(2)]
        a2 = get_cross_product(point_v2, t2_v)
        b = s2
    else:  # p3_triangle
        t1_v = [p1_triangle[i] - p3_triangle[i] for i in range(2)]
        a1 = get_cross_product(point_v3, t1_v)
        t2_v = [p2_triangle[i] - p3_triangle[i] for i in range(2)]
        a2 = get_cross_product(point_v3, t2_v)
        b = s3
    ## First line of triangle
    c1 = get_cross_product(line_v, t1_v)
    if c1 >= 0:  # avoid division
        is_collide1 = (0 <= a1 <= c1) and (0 <= b <= c1)
    else:
        is_collide1 = (0 >= a1 >= c1) and (0 >= b >= c1)
    ## Second line of triangle
    c2 = get_cross_product(line_v, t2_v)
    if c2 >= 0:  # avoid division
        is_collide2 = (0 <= a2 <= c2) and (0 <= b <= c2)
    else:
        is_collide2 = (0 >= a2 >= c2) and (0 >= b >= c2)
    return is_collide1 or is_collide2


def is_collision_circle_triangle_2d(circle_center, radius, p1_triangle,
                                    p2_triangle, p3_triangle):
    """Return True if Circle is collided with Triangle in 2D space.
     Otherwise, Return False.
    """
    point_v1 = [p1_triangle[i] - circle_center[i] for i in range(2)]
    point_v2 = [p2_triangle[i] - circle_center[i] for i in range(2)]
    point_v3 = [p3_triangle[i] - circle_center[i] for i in range(2)]
    get_cross_product = lambda v1, v2: (v1[0] * v2[1]) - (v1[1] * v2[0])
    area1 = get_cross_product(point_v1, point_v2)
    area2 = get_cross_product(point_v2, point_v3)
    area3 = get_cross_product(point_v3, point_v1)
    ## First check if circle inside triangle
    if area1 <= 0 and area2 <= 0 and area3 <= 0:
        return True
    ## check if circle collide with any line of triangle
    lines_of_triangle = [(p1_triangle, p2_triangle), (p2_triangle, p3_triangle),
                         (p3_triangle, p1_triangle)]
    for start_line, end_line in lines_of_triangle:
        line_v = [end_line[i] - start_line[i] for i in range(2)]
        magnitude_sq = sum(map(lambda x: x ** 2, line_v))
        if magnitude_sq:
            point_v = [circle_center[i] - start_line[i] for i in range(2)]
            func_mul = lambda x1, x2: x1 * x2
            t = sum(map(func_mul, line_v, point_v)) / magnitude_sq
            t = max(0, min(1, t))
            closest_point = [start_line[i] + (t * line_v[i]) for i in range(2)]
        else:  # it's point not line
            closest_point = start_line
        func_distance_sq = lambda x1, x2: (x1 - x2) ** 2
        distance_sq = sum(map(func_distance_sq, circle_center, closest_point))
        if distance_sq <= radius ** 2:
            return True
    return False
