#!/usr/bin/env python3


#### Import Python Library
import sys
from collections.abc import Callable, Sequence, Iterable, Sized
from typing import Any, Optional, Literal, Union, Final, TypeVar, Protocol

if sys.version_info <= (3, 9):
    from typing import Tuple, List, Type
else:
    Tuple = tuple
    List = list
    Type = type

sys = sys  # this because are imported in `.py`
Sequence = Sequence  # this because are imported in `.py`
Iterable = Iterable  # this because are imported in `.py`
######################################## TypeAlias
_Numbers = Union[float, int]
_AnyIndex = Union[slice, int]
_AnyOrSequence = Union[Any, Sequence[Any]]
_2Int = Union[Sequence[int], Tuple[int, int]]
_Tuple2Index = Tuple[_AnyIndex, _AnyIndex]
_EulerAnglesOrders = Literal[
    "XYZ", "XYz", "XZY", "XZy", "XyZ", "Xyz", "XzY", "Xzy",
    "YXZ", "YXz", "YZX", "YZx", "YxZ", "Yxz", "YzX", "Yzx",
    "ZXY", "ZXy", "ZYX", "ZYx", "ZxY", "Zxy", "ZyX", "Zyx",
    "xYZ", "xYz", "xZY", "xZy", "xyZ", "xyz", "xzY", "xzy",
    "yXZ", "yXz", "yZX", "yZx", "yxZ", "yxz", "yzX", "yzx",
    "zXY", "zXy", "zYX", "zYx", "zxY", "zxy", "zyX", "zyx"]

##### Vectors
_Vector = Iterable[_Numbers]
_Vector2 = Tuple[_Numbers, _Numbers]
_Vector3 = Tuple[_Numbers, _Numbers, _Numbers]
_Vector4 = Tuple[_Numbers, _Numbers, _Numbers, _Numbers]

_AnyVector = Sequence[_Numbers]
_AnyVector2 = Union[_Vector2, _AnyVector]
_AnyVector3 = Union[_Vector3, _AnyVector]
_AnyVector4 = Union[_Vector4, _AnyVector]

_AxisAngle = Tuple[_Vector3, _Numbers]

##### Matrices (Matrix)
_Matrix = Iterable[List[_Numbers]]
# _Matrix_2x2 = List[List[_Numbers]]  # not used
_Matrix_3x3 = List[List[_Numbers]]
_Matrix_4x4 = List[List[_Numbers]]

_AnyMatrix = Sequence[Sequence[_Numbers]]
# _AnyMatrix_2x2 = Union[_AnyMatrix, Sequence[_Vector2]]  # not used
_AnyMatrix_3x3 = Union[_AnyMatrix, Sequence[_Vector3]]
_AnyMatrix_4x4 = Union[_AnyMatrix, Sequence[_Vector4]]

######################################## GenericType
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_S = TypeVar("_S")
_S_co = TypeVar("_S_co", covariant=True)


class _SupportsAdd(Protocol[_T_contra, _T_co]):
    def __add__(self, x: _T_contra, /) -> _T_co: ...


class _SupportsSub(Protocol[_T_contra, _T_co]):
    def __sub__(self, x: _T_contra, /) -> _T_co: ...
    def __neg__(self, x: _T_contra, /) -> _T_co: ...


class _SupportsMul(Protocol[_T_contra, _T_co]):
    def __mul__(self, x: _T_contra, /) -> _T_co: ...


class _SupportsComparison(Protocol[_T_contra]):
    def __lt__(self, other: _T_contra, /) -> bool: ...
    def __le__(self, other: _T_contra, /) -> bool: ...
    def __eq__(self, other: _T_contra, /) -> bool: ...
    def __ne__(self, other: _T_contra, /) -> bool: ...
    def __gt__(self, other: _T_contra, /) -> bool: ...
    def __ge__(self, other: _T_contra, /) -> bool: ...


_Addable_T = TypeVar("_Addable_T", bound=_SupportsAdd[Any, Any])
_Subtractable_T = TypeVar("_Subtractable_T", bound=_SupportsSub[Any, Any])
_Multiplicable_T = TypeVar("_Multiplicable_T", bound=_SupportsMul[Any, Any])
_Comparable_T = TypeVar("_Comparable_T", bound=_SupportsComparison)

########################################
Numbers_Tuple: Final[Tuple[Type[float], Type[int]]]
AnyIndex_Tuple: Final[Tuple[Type[int], Type[slice]]]
EulerAnglesOrders: Final[List[str]]

## ``EM`` stand for ``Error Message``
EM_UNSUPPORTED_ORDER_EULER: Final[str]
EM_WRONG_TYPE_FOR_INDEX: Final[str]
EM_WRONG_VECTOR_LENGTH: Final[str]
EM_WRONG_MATRIX_SIZE: Final[str]
EM_NOT_SQUARE_MATRIX: Final[str]
EM_NOT_TUPLE_INDEX: Final[str]
EM_NOT_EXPECTED: Final[str]
EM_WRONG_LENGTH: Final[str]
EM_NOT_ALL_LENGTH_RIGHT: Final[str]
EM_ZERO_DIVISION: Final[str]
EM_ZERO_MOD: Final[str]
# EM_ZERO_POW_ZERO: Final[str]  # not used

e: Final[float]
pi: Final[float]
tau: Final[float]
epsilon: Final[float]
inf: Final[float]
nan: Final[float]


############################## Important Function ##############################
def isclose(a: _Numbers, b: _Numbers,
    rel_tol: _Numbers = 1e-09, abs_tol: _Numbers = 0.0) -> bool: ...


def xor(a: object, b: object) -> bool: ...


def degrees(x: _Multiplicable_T) -> _Multiplicable_T: ...


def radians(x: _Multiplicable_T) -> _Multiplicable_T: ...


def clamp(value: _Numbers, max_value: _Numbers, min_value: _Numbers
) -> _Numbers: ...


def lerp(a: _Numbers, b: _Numbers, factor: _Numbers) -> _Numbers: ...


def inv_lerp(a: _Numbers, b: _Numbers, factor: _Numbers) -> _Numbers: ...


def remap(value: _Numbers, from_range: _AnyVector2, to_range: _AnyVector2
) -> _Numbers: ...


def all_map(func: Callable[[...], _S], *iterables: Iterable[_T]) -> bool: ...


def any_map(func: Callable[[...], _S], *iterables: Iterable[_T]) -> bool: ...


def list_map(func: Callable[[...], _S], *iterables: Iterable[_T]
) -> List[_S]: ...


def tuple_map(func: Callable[[...], _S_co], *iterables: Iterable[_T_co]
) -> Tuple[_S_co]: ...


def max_map(func: Callable[[...], _Comparable_T],
    *iterables: Iterable[_Comparable_T]) -> _Comparable_T: ...


def min_map(func: Callable[[...], _Comparable_T],
    *iterables: Iterable[_Comparable_T]) -> _Comparable_T: ...


def sum_map(func: Callable[[...], _Addable_T], *iterables: Iterable[_Addable_T]
) -> _Addable_T: ...


def merge_iterables(*iterables: Iterable[_T]) -> List[_T]: ...


def merge_from_same_index(sequences: Iterable[Sequence[_T_co]], index: int
) -> Iterable[_T_co]: ...


def sub_values(iterable: Iterable[_Subtractable_T]) -> _Subtractable_T: ...


def mul_values(iterable: Iterable[_Multiplicable_T]) -> _Multiplicable_T: ...


def int_from_str_or_bytes(str_or_bytes: Union[str, bytes], base: int) -> int:...


################################ Check Functions ###############################
def is_same_sign(a: _Comparable_T, b: _Comparable_T, *c: _Comparable_T
) -> bool: ...


def is_sequence(obj: Any) -> bool: ...


def is_has_only(iterable: Iterable[Any], expect_value: Any, use_is: bool = False
) -> bool: ...


def is_contain_only(iterable: Iterable[Any], expect_types: Union[type, Tuple],
    use_issubclass: bool = False) -> bool: ...


def is_number(obj: Any, not_nan: bool = False, not_inf: bool = False
              ) -> bool: ...


def is_all_numbers(iterable: Iterable[Any],
    not_nan: bool = False, not_inf: bool = False) -> bool: ...


def is_all_same_length(sequence_of_sized: Sequence[Sized],
    specific_length: Optional[int] = None) -> bool: ...


def is_vector(obj: Any, specific_length: Optional[int] = None) -> bool: ...


def is_matrix(obj: Any, specific_rows: Optional[int] = None,
    specific_columns: Optional[int] = None) -> bool: ...


########################## Simple Operation Functions ##########################
def vector_add_vectors(*any_vectors: _AnyVector) -> _Vector: ...


def vector_add_values(any_vector: _AnyVector, values: Union[_Numbers, _Vector]
) -> _Vector: ...


def vector_sub_vectors(*any_vectors: _AnyVector) -> _Vector: ...


def vector_sub_values(any_vector: _AnyVector, values: Union[_Numbers, _Vector],
    reverse: bool = False) -> _Vector: ...


def vector_mul_vectors(*any_vectors: _AnyVector) -> _Vector: ...
    ## unable to define function inside function
    # def multi_vs(index: int) -> _Numbers: ...


def vector_mul_values(any_vector: _AnyVector, values: Union[_Numbers, _Vector]
) -> _Vector: ...


def vector_truediv_vector(v1: _AnyVector, v2: _AnyVector) -> _Vector: ...


def vector_truediv_value(any_vector: _AnyVector, value: _Numbers,
    reverse: bool = False) -> _Vector: ...


def vector_floordiv_vector(v1: _AnyVector, v2: _AnyVector) -> _Vector: ...


def vector_floordiv_value(any_vector: _AnyVector, value: _Numbers,
    reverse: bool = False) -> _Vector: ...


def vector_mod_vector(v1: _AnyVector, v2: _AnyVector) -> _Vector: ...


def vector_mod_value(any_vector: _AnyVector, value: _Numbers,
    reverse: bool = False) -> _Vector: ...


def vector_pow_vector(v1: _AnyVector, v2: _AnyVector, mod: Optional[int] = None
) -> _Vector: ...


def vector_pow_value(any_vector: _AnyVector, value: _Numbers,
    mod: Optional[int] = None, reverse: bool = False) -> _Vector: ...


def vector_divmod_vector(v1: _AnyVector, v2: _AnyVector
) -> Iterable[_Vector2]: ...


def vector_divmod_value(any_vector: _AnyVector, value: _Numbers,
    reverse: bool = False) -> Iterable[_Vector2]: ...


########################## Simple Comparison Functions #########################
def is_vector_lt_vector(v1: _AnyVector, v2: _AnyVector) -> bool: ...


def is_vector_le_vector(v1: _AnyVector, v2: _AnyVector) -> bool: ...


def is_vector_eq_vector(v1: _AnyVector, v2: _AnyVector) -> bool: ...


def is_vector_ne_vector(v1: _AnyVector, v2: _AnyVector) -> bool: ...


def is_vector_gt_vector(v1: _AnyVector, v2: _AnyVector) -> bool: ...


def is_vector_ge_vector(v1: _AnyVector, v2: _AnyVector) -> bool: ...


############# Compare Vector with Number
def is_vector_lt_value(any_vector: _Vector, value: _Numbers) -> bool: ...


def is_vector_le_value(any_vector: _Vector, value: _Numbers) -> bool: ...


def is_vector_eq_value(any_vector: _Vector, value: _Numbers) -> bool: ...


def is_vector_ne_value(any_vector: _Vector, value: _Numbers) -> bool: ...


def is_vector_gt_value(any_vector: _Vector, value: _Numbers) -> bool: ...


def is_vector_ge_value(any_vector: _Vector, value: _Numbers) -> bool: ...


############# Compare Vector with 0
def is_vector_negative_not_zero(any_vector: _Vector) -> bool: ...


def is_vector_negative(any_vector: _Vector) -> bool: ...


def is_vector_eq_zero(any_vector: _Vector) -> bool: ...


def is_vector_ne_zero(any_vector: _Vector) -> bool: ...


def is_vector_positive_not_zero(any_vector: _Vector) -> bool: ...


def is_vector_positive(any_vector: _Vector) -> bool: ...


################## Vector isclose
def is_vector_close_vector(v1: _AnyVector, v2: _AnyVector,
    rel_tol: _Numbers = 1e-09, abs_tol: _Numbers = 0.0) -> bool: ...


def is_vector_close_value(any_vector: _AnyVector, value: _Numbers,
    rel_tol: _Numbers = 1e-09, abs_tol: _Numbers = 0.0) -> bool: ...


def is_vector_close_zero(any_vector: _AnyVector) -> bool: ...


################## Vector is NaN or Inf
def is_vector_nan_or_inf(any_vector: _AnyVector, is_any: bool = False
) -> bool: ...


is_vector_inf_or_nan = is_vector_nan_or_inf  # :D


def is_vector_nan(any_vector: _AnyVector, is_any: bool = False) -> bool: ...


def is_vector_inf(any_vector: _AnyVector, is_any: bool = False) -> bool: ...


######################### Specific Operation Functions #########################
def dot_product_vectors(*any_vectors: _AnyVector) -> _Numbers: ...
    ## unable to define function inside function :C
    # def multi_vs(index: int) -> _Numbers: ...


def distance_vectors_sq(from_v1: _AnyVector, to_v2: _AnyVector) -> _Numbers: ...


def distance_vectors(from_v1: _AnyVector, to_v2: _AnyVector) -> _Numbers: ...


def magnitude_vector_sq(any_vector: _Vector) -> _Numbers: ...


def magnitude_vector(any_vector: _Vector) -> _Numbers: ...


def vector_normalize(any_vector: _Vector) -> _Vector: ...


def is_vector_normalized(any_vector: _Vector) -> bool: ...


def vector_direction(from_v1: _AnyVector, to_v2: _AnyVector) -> _Vector: ...


def vector_midpoint(v1: _AnyVector, v2: _AnyVector) -> _Vector: ...


def vector_round(any_vector: _AnyVector, ndigits: Optional[int] = None
                 ) -> _Vector: ...


def vector_ceil(any_vector: _AnyVector) -> _Vector: ...


def vector_floor(any_vector: _AnyVector) -> _Vector: ...


def vector_negative(any_vector: _Vector) -> _Vector: ...


def vector_abs(any_vector: _Vector) -> _Vector: ...


def vector_zero(n: int) -> Iterable[Literal[0]]: ...


def vector_from_matrix(any_matrix: Iterable[Iterable[_Numbers]]
                       ) -> List[_Numbers]: ...


def string_format_vector(any_vector: _AnyVector, format_spec: str) -> str: ...


#################################### Vector2 ###################################
def cross_product_v2(v1: _AnyVector2, v2: _AnyVector2
                     ) -> Tuple[Literal[0], Literal[0], _Numbers]: ...


def angle_v2(v1: _AnyVector2, v2: _AnyVector2,
             center: Optional[_AnyVector2] = None) -> _Numbers: ...


#################################### Vector3 ###################################
def cross_product_v3(v1: _AnyVector3, v2: _AnyVector3) -> _Vector3: ...


def angle_v3(v1: _AnyVector3, v2: _AnyVector3,
             center: Optional[_AnyVector3] = None) -> _Numbers: ...


def axis_angle_from_quaternion(quaternion: _AnyVector4) -> _AxisAngle: ...


def axis_angle_from_matrix_3x3(any_matrix_3x3: _AnyMatrix_3x3) -> _AxisAngle:...


def axis_angle_from_euler(yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                          order: _EulerAnglesOrders) -> _AxisAngle: ...


def euler_from_matrix_3x3(any_matrix_3x3: _AnyMatrix_3x3,
                          order: _EulerAnglesOrders) -> _Vector3: ...


def euler_from_quaternion(quaternion: _AnyVector4, order: _EulerAnglesOrders
                          ) -> _Vector3: ...


def euler_from_axis_angle(axis: _AnyVector3, angle: _Numbers,
                          order: _EulerAnglesOrders) -> _Vector3: ...


def euler_from_euler(yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                     input_order: _EulerAnglesOrders,
                     output_order: _EulerAnglesOrders) -> _Vector3: ...


############################## Vector4/Quaternion ##############################
def quaternion_identity() -> Tuple[
    Literal[0], Literal[0], Literal[0], Literal[1]]: ...


def quaternion_multiply(q1: _AnyVector4, q2: _AnyVector4) -> _Vector4: ...


def quaternion_mul_quaternions(*quaternions: _AnyVector4) -> _Vector4: ...


def quaternion_opposite(quaternion: _AnyVector4) -> _Vector4: ...


def quaternion_from_axis_angle(axis: _AnyVector3,
                               angle: _Numbers) -> _Vector4: ...


def quaternion_from_euler(yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                          order: _EulerAnglesOrders) -> _Vector4: ...


def quaternion_from_matrix_3x3(any_matrix_3x3: _AnyMatrix_3x3
                               ) -> _Vector4: ...


#################################### Matrix ####################################
# TODO add overload here
def matrix_getitem(any_matrix: _AnyMatrix,
                   index: Union[_AnyIndex, Tuple[_AnyIndex, _AnyIndex]]
                   ) -> Union[_Matrix, _Vector, _Numbers]: ...


def _matrix_setitem_from_index(
        any_matrix: _AnyMatrix, index: _AnyIndex,
        new_value: Union[_Numbers, _AnyVector, _AnyMatrix]) -> _Matrix: ...


def _matrix_setitem_from_tuple(
        any_matrix: _AnyMatrix, tuple_index: _Tuple2Index,
        new_value: Union[_Numbers, _AnyVector, _AnyMatrix]) -> _Matrix: ...


def matrix_setitem(any_matrix: _AnyMatrix,
    index: Union[_AnyIndex, _Tuple2Index],
    new_value: Union[_Numbers, _AnyVector, _AnyMatrix]) -> _Matrix: ...


def string_matrix(any_matrix: _AnyMatrix) -> str: ...


def string_format_matrix(any_matrix: _AnyMatrix, format_spec: str) -> str: ...


def size_matrix(any_matrix: Sequence[Sized]) -> Tuple[int, int]: ...


def trace_matrix(any_matrix: _AnyMatrix) -> _Numbers: ...


def determinant_matrix(any_matrix: _AnyMatrix) -> _Numbers: ...


def matrix_from_vector(vector: _AnyVector, size: _2Int) -> _Matrix: ...


def matrix_identity(n: int) -> _Matrix: ...


def matrix_adjugate(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_transpose(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_inv(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_round(any_matrix: _AnyMatrix, ndigits: Optional[int] = None
                 ) -> _Matrix: ...


def matrix_ceil(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_floor(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_negative(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_abs(any_matrix: _AnyMatrix) -> _Matrix: ...


def matrix_zero(size: _2Int) -> Iterable[List[Literal[0]]]: ...


############### Matrix Simple Operations
def matrix_add_matrices(*any_matrices: _AnyMatrix) -> _Matrix: ...


def matrix_sub_matrices(*any_matrices: _AnyMatrix) -> _Matrix: ...


def matrix_mul_matrix(matrix1: _AnyMatrix, matrix2: _AnyMatrix
                      ) -> _Matrix: ...


def matrix_mul_vector(any_vector: _AnyVector, any_matrix: _AnyMatrix
                      ) -> _Vector: ...


def matrix_mul_value(value: _Numbers, any_matrix: _AnyMatrix
                     ) -> _Matrix: ...


def matrix_truediv_matrix(any_matrix1: _AnyMatrix, any_matrix2: _AnyMatrix
                          ) -> _Matrix: ...


############################# Matrix 3x3
def matrix_3x3_from_x_rotation(angle: _Numbers, transpose: bool = False
                               ) -> _Matrix_3x3: ...


def matrix_3x3_from_y_rotation(angle: _Numbers, transpose: bool = False
                               ) -> _Matrix_3x3: ...


def matrix_3x3_from_z_rotation(angle: _Numbers, transpose: bool = False
                               ) -> _Matrix_3x3: ...


def matrix_3x3_from_euler(yaw: _Numbers, pitch: _Numbers, roll: _Numbers,
                          order: _EulerAnglesOrders) -> _Matrix_3x3: ...


def matrix_3x3_from_axis_angle(axis: _AnyVector3, angle: _Numbers
                               ) -> _Matrix_3x3: ...


def matrix_3x3_from_quaternion(quaternion: _AnyVector4) -> _Matrix_3x3:
    ...


def matrix_3x3_from_scale(scale_v3: _AnyVector3) -> _Matrix_3x3: ...


def matrix_3x3_from_direction_scale(direction_v3: _AnyVector3, scale: _Numbers
                                    ) -> _Matrix_3x3: ...


############################# Matrix 4x4
def matrix_4x4_look_at(eye: _AnyVector3, target: _AnyVector3, up: _AnyVector3,
                       transpose: bool = False) -> _Matrix_4x4: ...


def matrix_4x4_perspective_projection_bounds(left: _Numbers, right: _Numbers,
                                             bottom: _Numbers, top: _Numbers,
                                             near: _Numbers, far: _Numbers,
                                             transpose: bool = False
                                             ) -> _Matrix_4x4: ...


def matrix_4x4_perspective_projection(angle: _Numbers, aspect: _Numbers,
                                      near: _Numbers, far: _Numbers,
                                      transpose: bool = False
                                      ) -> _Matrix_4x4: ...


def matrix_4x4_from_translation(translation: _AnyVector3,
                                transpose: bool = False) -> _Matrix_4x4: ...


############################# Check Collisions 2D ##############################
def is_collision_point_line_2d(point: _AnyVector2,
    start_line: _AnyVector2, end_line: _AnyVector2) -> bool: ...


def is_collision_line_line_2d(
        start_line1: _AnyVector2, end_line1: _AnyVector2,
        start_line2: _AnyVector2, end_line2: _AnyVector2) -> bool: ...


def is_collision_point_circle_2d(point: _AnyVector2,
    circle_center: _AnyVector2, radius: _Numbers) -> bool: ...


def is_collision_line_circle_2d(
        start_line: _AnyVector2, end_line: _AnyVector2,
        circle_center: _AnyVector2, radius: _Numbers) -> bool: ...


def is_collision_circle_circle_2d(
        circle_center1: _AnyVector2, radius1: _Numbers,
        circle_center2: _AnyVector2, radius2: _Numbers) -> bool: ...


def is_collision_point_rect_2d(point: _AnyVector2,
    rect_topleft: _AnyVector2, rect_width: _Numbers, rect_height: _Numbers
                               ) -> bool: ...


def is_collision_line_rect_2d(start_line: _AnyVector2, end_line: _AnyVector2,
    rect_topleft: _AnyVector2, rect_width: _Numbers, rect_height: _Numbers
) -> bool: ...


def is_collision_circle_rect_2d(circle_center: _AnyVector2, radius: _Numbers,
    rect_topleft: _AnyVector2, rect_width: _Numbers, rect_height: _Numbers
) -> bool: ...


def is_collision_rect_rect_2d(
    rect_topleft1: _AnyVector2, rect_width1: _Numbers, rect_height1: _Numbers,
    rect_topleft2: _AnyVector2, rect_width2: _Numbers, rect_height2: _Numbers
) -> bool: ...


def is_collision_point_triangle_2d(point: _AnyVector2,
    p1_triangle: _AnyVector2, p2_triangle: _AnyVector2, p3_triangle: _AnyVector2
) -> bool: ...


def is_collision_line_triangle_2d(
    start_line: _AnyVector2, end_line: _AnyVector2,
    p1_triangle: _AnyVector2, p2_triangle: _AnyVector2, p3_triangle: _AnyVector2
) -> bool: ...


def is_collision_circle_triangle_2d(
    circle_center: _AnyVector2, radius: _Numbers,
    p1_triangle: _AnyVector2, p2_triangle: _AnyVector2, p3_triangle: _AnyVector2
) -> bool: ...


