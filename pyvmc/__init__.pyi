#!/usr/bin/env python3


#### Import Python Library
from collections.abc import Iterator
from typing import (Any, Final, TypeVar, Literal, Optional, Union,
                    overload, final)
import copy
import re

#### Import Files
from .pyvmc_functions import *  # here also import Sequence, Iterable and sys

if sys.version_info <= (3, 9):
    from typing import Tuple, List, Dict
else:
    Tuple = tuple
    List = list
    Dict = dict

copy = copy  # this because are imported in `.py`
re = re  # this because are imported in `.py`
######################################## TypeAlias
_Numbers = Union[float, int]
_AnyIndex = Union[slice, int]
_4StrOr4Bytes = Union[Sequence[str], Sequence[bytes],
    Tuple[str, str, str, str], Tuple[bytes, bytes, bytes, bytes]]
_2Int = Union[Tuple[int, int], Sequence[int]]
_Tuple2Numbers = Tuple[_Numbers, _Numbers]
_Tuple3Numbers = Tuple[_Numbers, _Numbers, _Numbers]
_Tuple4Numbers = Tuple[_Numbers, _Numbers, _Numbers, _Numbers]
_MatrixIndex = Union[_AnyIndex, Tuple[_AnyIndex, _AnyIndex]]
_EulerAnglesOrders = Literal[
    "XYZ", "XYz", "XZY", "XZy", "XyZ", "Xyz", "XzY", "Xzy",
    "YXZ", "YXz", "YZX", "YZx", "YxZ", "Yxz", "YzX", "Yzx",
    "ZXY", "ZXy", "ZYX", "ZYx", "ZxY", "Zxy", "ZyX", "Zyx",
    "xYZ", "xYz", "xZY", "xZy", "xyZ", "xyz", "xzY", "xzy",
    "yXZ", "yXz", "yZX", "yZx", "yxZ", "yxz", "yzX", "yzx",
    "zXY", "zXy", "zYX", "zYx", "zxY", "zxy", "zyX", "zyx"]
_EulerAnglesOrdersUpper = Literal["XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX"]

#####
# _AnyFixList = Union[Sequence[Any], List[Any]]  # not used

_Color = Union[Sequence[int], Tuple[int, int, int, int]]

_AnyColor = Union[Iterable[int], _Color]

##### Vectors
_Vector = Sequence[_Numbers]
_Vector2 = Union[_Vector, _Tuple2Numbers]
_Vector3 = Union[_Vector, _Tuple3Numbers]
_Vector4 = Union[_Vector, _Tuple4Numbers]

_AnyVector = Union[Iterable[_Numbers], _Vector]
_AnyVector2 = Union[Iterable[_Numbers], _Vector2]
_AnyVector3 = Union[Iterable[_Numbers], _Vector3]
_AnyVector4 = Union[Iterable[_Numbers], _Vector4]

##### Matrices (Matrix)
_Matrix = Sequence[_Vector]
# _Matrix_2x2 = Union[_Matrix, Sequence[_Vector2]]  # not used
_Matrix_3x3 = Union[_Matrix, Sequence[_Vector3]]
# _Matrix_4x4 = Union[_Matrix, Sequence[_Vector4]]  # not used

##### Self
_FixListSelf = TypeVar("_FixListSelf", bound="FixList")

_ColorSelf = TypeVar("_ColorSelf", bound="Color")

_VectorSelf = TypeVar("_VectorSelf", bound="Vector")

_Vector2Self = TypeVar("_Vector2Self", bound="Vector2")

_Vector3Self = TypeVar("_Vector3Self", bound="Vector3")

_EulerSelf = TypeVar("_EulerSelf", bound="Euler")

_Vector4Self = TypeVar("_Vector4Self", bound="Vector4")

_MatrixSelf = TypeVar("_MatrixSelf", bound="Matrix")

######################################## GenericType
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

########################################
__author__: Final[str]
__copyright__: Final[str]
__licence__: Final[str]
__version__: Final[str]

MATRIX_START_LETTER_ATTRIB: Final[str]
MATRIX_PATTERN_ATTRIB: Final[str]

## ``EM`` stand for ``Error Message``
EM_UNSUPPORTED_TYPE_OPERATION: Final[str]
EM_NO_ATTRIBUTE: Final[str]
EM_WRONG_MATRIX_PATTERN_ATTRIB: Final[str]


class FixList(Sequence[_T_co]):

    def __new__(cls, *args, **kwargs) -> _FixListSelf: ...

    def __init__(self, iterable: Iterable[_T_co], *args, **kwargs) -> None:
        self._data: List[_T_co]
        self.__first_length: int

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    @final
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int) -> _T_co: ...

    @overload
    def __getitem__(self, index: slice) -> List[_T]: ...

    def __setitem__(self, index: Any, new_value: Any) -> None: ...

    @final
    def __delitem__(self, key) -> None: ...

    def __iter__(self) -> Iterator[_T]: ...

    def __reversed__(self) -> Iterator[_T]: ...

    def __copy__(self) -> _FixListSelf: ...

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None
                     ) -> _FixListSelf: ...

    ########## Methods
    def strict_length(self, expect_length: int) -> None: ...

    def change_data(self, new_data: Iterable[Any],
                    offset_index: int = 0, strict: bool = False) -> None: ...

    def copy(self) -> _FixListSelf: ...

    def copy_tuple(self) -> Tuple[_T_co]: ...

    def copy_list(self) -> List[_T]: ...

    def deepcopy(self,
                 memo: Optional[Dict[int, Any]] = None) -> _FixListSelf: ...

    def deepcopy_tuple(self, memo: Optional[Dict[int, Any]] = None
                       ) -> Tuple[_T_co]: ...

    def deepcopy_list(self, memo: Optional[Dict[int, Any]] = None
                      ) -> List[_T]: ...


class Color(FixList):
    COLOR_SPECIAL_STR: str
    COLOR_SPECIAL_REPR: str

    def __init__(self, red_green_blue_alpha: Optional[_AnyColor] = None,
                 *args: Any, **kwargs: Any) -> None:
        self._data: List[int]

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __format__(self, format_spec: str) -> str: ...

    ########## Properties
    @property
    def r(self) -> int: ...

    @r.setter
    def r(self, value: int) -> None: ...

    @property
    def r_hex(self) -> str: ...

    @property
    def r_bytes(self) -> bytes: ...

    @property
    def g(self) -> int: ...

    @g.setter
    def g(self, value: int) -> None: ...

    @property
    def g_hex(self) -> str: ...

    @property
    def g_bytes(self) -> bytes: ...

    @property
    def b(self) -> int: ...

    @b.setter
    def b(self, value: int) -> None: ...

    @property
    def b_hex(self) -> str: ...

    @property
    def b_bytes(self) -> bytes: ...

    @property
    def a(self) -> int: ...

    @a.setter
    def a(self, value: int) -> None: ...

    @property
    def a_hex(self) -> str: ...

    @property
    def a_bytes(self) -> bytes: ...

    @property
    def to_hex_tuple(self) -> Tuple[str, str, str, str]: ...

    @property
    def to_hex_str(self) -> str: ...

    @property
    def to_bytes_tuple(self) -> Tuple[bytes, bytes, bytes, bytes]: ...

    @property
    def to_bytes(self) -> bytes: ...

    @property
    def color_normalize(self) -> _Tuple4Numbers: ...

    @property
    def rgb(self) -> Tuple[int, int, int]: ...

    @property
    def rgb_normalize(self) -> _Tuple3Numbers: ...

    ########## Methods
    def from_str_or_bytes(self, str_or_bytes: Union[str, bytes], base: int
                          ) -> None: ...

    def from_tuple(self, t_4str_or_4bytes: _4StrOr4Bytes, base: int
                   ) -> None: ...


## Note: all those are from Raylib in:
# https://www.raylib.com/cheatsheet/cheatsheet.html#colors
## with some tiny modification of values. THANKS TO RAYLIB :D
LIGHTGRAY: Final[Color]
GRAY: Final[Color]
DARKGRAY: Final[Color]
YELLOW: Final[Color]
GOLD: Final[Color]
ORANGE: Final[Color]
PINK: Final[Color]
RED: Final[Color]
MAROON: Final[Color]
GREEN: Final[Color]
LIME: Final[Color]
DARKGREEN: Final[Color]
SKYBLUE: Final[Color]
BLUE: Final[Color]
DARKBLUE: Final[Color]
PURPLE: Final[Color]
VIOLET: Final[Color]
DARKPURPLE: Final[Color]
BEIGE: Final[Color]
BROWN: Final[Color]
DARKBROWN: Final[Color]
WHITE: Final[Color]
BLACK: Final[Color]
BLANK: Final[Color]
MAGENTA: Final[Color]
RAYWHITE: Final[Color]
##
ALL_COLORS: Final[List[Color]]


class Vector(FixList):

    ## Note: this is Not in `.py` file this just for annotation only.
    def __init__(self, iterable_numbers: Iterable[_Numbers], *args, **kwargs
                 ) -> None:
        self._data: List[_Numbers]

    def __format__(self, format_spec: str) -> str: ...

    ########## Operation
    def method_add(self, other) -> _VectorSelf: ...

    def method_sub(self, other) -> _VectorSelf: ...

    def method_mul(self, other) -> _VectorSelf: ...

    def method_truediv(self, other, reverse: bool = False) -> _VectorSelf: ...

    def method_floordiv(self, other, reverse: bool = False) -> _VectorSelf: ...

    def method_mod(self, other, reverse: bool = False) -> _VectorSelf: ...

    def method_pow(self, power, mod: Optional[int] = None, reverse: bool = False
                   ) -> _VectorSelf: ...

    def method_divmod(self, other, reverse: bool = False
                      ) -> List[_Tuple2Numbers]: ...

    def method_round(self, ndigits: Optional[int] = None) -> _VectorSelf: ...

    def method_ceil(self) -> _VectorSelf: ...

    def method_floor(self) -> _VectorSelf: ...

    def __add__(self, other) -> _VectorSelf: ...

    __radd__ = method_add

    def __sub__(self, other) -> _VectorSelf: ...

    __rsub__ = method_sub

    def __mul__(self, other) -> _VectorSelf: ...

    __rmul__ = method_mul

    def __truediv__(self, other) -> _VectorSelf: ...

    def __rtruediv__(self, other) -> _VectorSelf: ...

    def __floordiv__(self, other) -> _VectorSelf: ...

    def __rfloordiv__(self, other) -> _VectorSelf: ...

    def __mod__(self, other) -> _VectorSelf: ...

    def __rmod__(self, other) -> _VectorSelf: ...

    def __pow__(self, power, modulo: Optional[int] = None) -> _VectorSelf: ...

    def __rpow__(self, power, modulo: Optional[int] = None) -> _VectorSelf: ...

    def __divmod__(self, power) -> List[Tuple[_Numbers, _Numbers]]: ...

    def __rdivmod__(self, power) -> List[Tuple[_Numbers, _Numbers]]: ...

    __round__ = method_round
    __ceil__ = method_ceil
    __floor__ = method_floor

    def __lt__(self, other) -> bool: ...

    def __le__(self, other) -> bool: ...

    def __eq__(self, other) -> bool: ...

    def __ne__(self, other) -> bool: ...

    def __gt__(self, other) -> bool: ...

    def __ge__(self, other) -> bool: ...

    def __abs__(self) -> _VectorSelf: ...

    def __neg__(self) -> _VectorSelf: ...

    def __pos__(self) -> _VectorSelf: ...

    ########## Properties
    @property
    def magnitude(self) -> _Numbers: ...

    @property
    def magnitude_sq(self) -> _Numbers: ...

    @property
    def normalize(self) -> _VectorSelf: ...

    @property
    def is_normalized(self) -> bool: ...

    ########## Methods
    def to_vector(self) -> Vector: ...

    def to_vector2(self) -> Vector2: ...

    def to_vector3(self) -> Vector3: ...

    def to_vector4(self) -> Vector4: ...

    def to_matrix(self, size: _2Int) -> Matrix: ...

    def normalize_it(self) -> None: ...

    def midpoint_between(self, vector: _Vector) -> _VectorSelf: ...

    ## those just are alias for functions
    def dot_product(self, *vectors: _Vector) -> _Numbers: ...

    def distance_to(self, vector: _Vector) -> _Numbers: ...

    def is_close_vector(self, vector: _Vector,
                        rel_tol: _Numbers = 1e-09, abs_tol: _Numbers = 0.0
                        ) -> bool: ...

    def is_close_value(self, value: _Numbers,
                       rel_tol: _Numbers = 1e-09, abs_tol: _Numbers = 0.0
                       ) -> bool: ...

    def is_nan_or_inf(self, is_any: bool = False) -> bool: ...

    is_inf_or_nan = is_nan_or_inf

    def is_nan(self, is_any: bool = False) -> bool: ...

    def is_inf(self, is_any: bool = False) -> bool: ...


class Vector2(Vector):
    VECTOR2_SPECIAL_STR: str
    # VECTOR2_SPECIAL_REPR: str  # not used

    def __init__(self, any_vector2: Optional[_AnyVector2] = None,
                    *args: Any, **kwargs: Any) -> None: ...

    def __str__(self) -> str: ...

    __repr__ = __str__

    def __format__(self, format_spec: str) -> str: ...

    ########## Properties
    @property
    def x(self) -> _Numbers: ...

    @x.setter
    def x(self, value: _Numbers) -> None: ...

    @property
    def x_int(self) -> int: ...

    @property
    def y(self) -> _Numbers: ...

    @y.setter
    def y(self, value: _Numbers) -> None: ...

    @property
    def y_int(self) -> int: ...

    ########## Methods
    def angle(self, vector2: _Vector2, center: Optional[_Vector2] = None
              ) -> _Numbers: ...

    def cross_product(self, vector2: _Vector2) -> Vector3: ...


Point2D = Vector2


class Vector3(Vector):
    VECTOR3_SPECIAL_STR: str
    # VECTOR3_SPECIAL_REPR: str  # not used

    def __init__(self, any_vector3: Optional[_AnyVector3] = None,
            *args, **kwargs) -> None: ...

    def __str__(self) -> str: ...

    __repr__ = __str__

    def __format__(self, format_spec: str) -> str: ...

    ########## Properties
    @property
    def x(self) -> _Numbers: ...

    @x.setter
    def x(self, value: _Numbers) -> None: ...

    @property
    def x_int(self) -> int: ...

    @property
    def y(self) -> _Numbers: ...

    @y.setter
    def y(self, value: _Numbers) -> None: ...

    @property
    def y_int(self) -> int: ...

    @property
    def z(self) -> _Numbers: ...

    @z.setter
    def z(self, value: _Numbers) -> None: ...

    @property
    def z_int(self) -> int: ...

    ########## Methods
    def angle(self, vector3: _Vector3, center: Optional[_Vector3] = None
              ) -> _Numbers: ...

    def cross_product(self, vector3: _Vector3) -> Vector3: ...


Point3D = Vector3


class Euler(Vector):
    EULER_SPECIAL_STR: Final[str]
    EULER_SPECIAL_REPR: Final[str]

    def __init__(self, yaw_pitch_roll: _AnyVector3, order: _EulerAnglesOrders,
                 *args: Any, **kwargs: Any) -> None:
        self.__order: str

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __format__(self, format_spec: str) -> str: ...

    ########## Properties
    @property
    def order(self) -> _EulerAnglesOrdersUpper: ...

    @property
    def yaw(self) -> _Numbers: ...

    @yaw.setter
    def yaw(self, value) -> None: ...

    @property
    def yaw_degrees(self) -> _Numbers: ...

    @property
    def pitch(self) -> _Numbers: ...

    @pitch.setter
    def pitch(self, value) -> None: ...

    @property
    def pitch_degrees(self) -> _Numbers: ...

    @property
    def roll(self) -> _Numbers: ...

    @roll.setter
    def roll(self, value) -> None: ...

    @property
    def roll_degrees(self) -> _Numbers: ...

    ########## Methods
    def change_order(self, new_order: _EulerAnglesOrders) -> None: ...

    def to_matrix_3x3(self) -> Matrix_3x3: ...

    def to_quaternion(self) -> Vector4: ...

    def to_axis_angle(self) -> Tuple[Vector3, _Numbers]: ...

    def from_matrix_3x3(self, matrix_3x3: _Matrix_3x3) -> None: ...

    def from_quaternion(self, quaternion: _Vector4) -> None: ...

    def from_axis_angle(self, axis: _Vector3, angle: _Numbers) -> None: ...

    def from_euler(self, yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                   input_order: _EulerAnglesOrders) -> None: ...


class Vector4(Vector):
    VECTOR4_SPECIAL_STR: str
    # VECTOR4_SPECIAL_REPR: str  # not used

    def __init__(self, any_vector4: Optional[_AnyVector4] = None,
                 *args: Any, **kwargs: Any) -> None: ...

    def __str__(self) -> str: ...

    __repr__ = __str__

    def __format__(self, format_spec: str) -> str: ...

    ########## Main Info
    @property
    def x(self) -> _Numbers: ...

    @x.setter
    def x(self, value: _Numbers) -> None: ...

    @property
    def x_int(self) -> int: ...

    @property
    def y(self) -> _Numbers: ...

    @y.setter
    def y(self, value: _Numbers) -> None: ...

    @property
    def y_int(self) -> int: ...

    @property
    def z(self) -> _Numbers: ...

    @z.setter
    def z(self, value: _Numbers) -> None: ...

    @property
    def z_int(self) -> int: ...

    @property
    def w(self) -> _Numbers: ...

    @w.setter
    def w(self, value: _Numbers) -> None: ...

    @property
    def w_int(self) -> int: ...

    ########## Properties
    @classmethod
    @property
    def identity(cls) -> Vector4: ...

    @property
    def opposite(self) -> Vector4: ...

    ########## Methods
    def identity_it(self) -> None: ...

    def opposite_it(self) -> None: ...

    def mul_quaterion(self, other: _Vector4) -> Vector4: ...

    def mul_quaterion_it(self, other: _Vector4) -> None: ...

    def to_axis_angle(self) -> Tuple[Vector3, _Numbers]: ...

    def to_euler(self, order: _EulerAnglesOrders) -> Euler: ...

    def to_matrix_3x3(self) -> Matrix_3x3: ...

    def from_axis_angle(self, axis: _Vector3, angle: _Numbers) -> None: ...

    def from_euler(self, yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                   order: _EulerAnglesOrders) -> None: ...

    def from_matrix_3x3(self, matrix_3x3: _Matrix_3x3) -> None: ...


Quaternion = Point4D = Vector4


class Matrix(FixList):

    def __init__(self, iterable_vectors: Iterable[_AnyVector],
                 *args: Any, **kwargs: Any) -> None:
        self._data: List[List[_Numbers]]

    def __str__(self) -> str: ...

    __repr__ = __str__

    def __format__(self, format_spec: str) -> str: ...

    @overload
    def __getitem__(self,
                    index: Union[int, Tuple[slice, int], Tuple[int, slice]]
                    ) -> Vector: ...

    @overload
    def __getitem__(self, index: Union[slice, Tuple[slice, slice]]
                    ) -> Matrix: ...

    @overload
    def __getitem__(self, index: Tuple[int, int]) -> _Numbers: ...

    def __setitem__(self, index: _MatrixIndex,
                    new_value: Union[_Numbers, _Vector, _Matrix]) -> None: ...

    def __getattr__(self, name: str) -> Union[_Numbers, Any]: ...

    def __setattr__(self, name: str, value: Any) -> None: ...

    ########## Operation
    def method_add(self, other) -> _MatrixSelf: ...

    def method_sub(self, other) -> _MatrixSelf: ...

    # TODO add overload here
    def method_mul(self, other, reverse: bool = False
                   ) -> Union[Vector, _MatrixSelf]: ...

    def method_truediv(self, other, reverse: bool = False) -> _MatrixSelf: ...

    def method_round(self, ndigits: Optional[int] = None) -> _MatrixSelf: ...

    def method_ceil(self) -> _MatrixSelf: ...

    def method_floor(self) -> _MatrixSelf: ...

    def __add__(self, other) -> _MatrixSelf: ...

    __radd__ = method_add

    def __sub__(self, other) -> _MatrixSelf: ...

    __rsub__ = method_sub

    # TODO add overload AND here
    def __mul__(self, other) -> Union[Vector, _MatrixSelf]: ...

    def __rmul__(self, other) -> _MatrixSelf: ...

    def __truediv__(self, other) -> _MatrixSelf: ...

    def __rtruediv__(self, other) -> _MatrixSelf: ...

    __round__ = method_round
    __ceil__ = method_ceil
    __floor__ = method_floor

    ########## Property
    @property
    def num_rows(self) -> int: ...

    @property
    def num_columns(self) -> int: ...

    @property
    def size(self) -> _2Int: ...

    @property
    def is_size_square(self) -> bool: ...

    @property
    def transpose(self) -> _MatrixSelf: ...

    @property
    def trace(self) -> _Numbers: ...

    @property
    def determinant(self) -> _Numbers: ...

    @property
    def adjugate(self) -> _MatrixSelf: ...

    @property
    def inv(self) -> _MatrixSelf: ...

    ########## Methods
    def strict_size(self, expect_size: _2Int) -> None: ...

    def to_vector(self) -> Vector: ...

    def to_matrix(self) -> Matrix: ...

    def to_matrix_2x2(self) -> Matrix_2x2: ...

    def to_matrix_3x3(self) -> Matrix_3x3: ...

    def to_matrix_4x4(self) -> Matrix_4x4: ...

    @overload
    @classmethod
    def identity(cls, n: Literal[2]) -> Matrix_2x2: ...
    @overload
    @classmethod
    def identity(cls, n: Literal[3]) -> Matrix_3x3: ...
    @overload
    @classmethod
    def identity(cls, n: Literal[4]) -> Matrix_4x4: ...
    @overload
    @classmethod
    def identity(cls, n: int) -> Matrix: ...

    def identity_it(self) -> None: ...

    def adjugate_it(self) -> None: ...

    def inv_it(self) -> None: ...


class Matrix_2x2(Matrix):

    def __init__(self, any_matrix_2x2: Optional[Iterable[_AnyVector2]] = None,
                 *args, **kwargs) -> None: ...


class Matrix_3x3(Matrix):

    def __init__(self, any_matrix_3x3: Optional[Iterable[_AnyVector3]] = None,
                 *args: Any, **kwargs: Any) -> None: ...

    ########## Methods
    def from_x_rotation(self, angle: _Numbers, transpose: bool = False) -> None:
        ...

    def from_y_rotation(self, angle: _Numbers, transpose: bool = False) -> None:
        ...

    def from_z_rotation(self, angle: _Numbers, transpose: bool = False) -> None:
        ...

    def from_euler(self, yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                   order: _EulerAnglesOrders) -> None: ...

    def from_axis_angle(self, axis: _Vector3, angle: _Numbers) -> None: ...

    def from_quaternion(self, quaternion: _Vector4) -> None: ...

    def from_scale(self, scale_v3: _Vector3) -> None: ...

    def from_direction_scale(self, direction_v3: _Vector3, scale: _Numbers
                             ) -> None: ...


class Matrix_4x4(Matrix):

    def __init__(self, any_matrix_4x4: Optional[Iterable[_AnyVector4]] = None,
                 *args: Any, **kwargs: Any) -> None: ...

    ########## Methods
    def create_look_at(self,
                       eye: _Vector3, target: _Vector3, up: _Vector3,
                       transpose: bool = False
                       ) -> None: ...

    def perspective_projection_bounds(self,
                                      left: _Numbers, right: _Numbers,
                                      bottom: _Numbers, top: _Numbers,
                                      near: _Numbers, far: _Numbers,
                                      transpose: bool = False) -> None: ...

    def perspective_projection(self,
                               angle: _Numbers, aspect: _Numbers,
                               near: _Numbers, far: _Numbers,
                               transpose: bool = False) -> None: ...

    def from_translation(self, vector3: _Vector3, transpose: bool = False
                         ) -> None: ...
