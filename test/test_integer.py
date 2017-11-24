from decimal import Decimal
import fractions
from hypothesis import given, strategies as st
from integer import is_prime, Integer
import math
import operator
import pytest as pt
import string


# INIT TEST #
@given(st.integers())
def test_init_integer(z):
    assert Integer(z).num == z


@given(st.floats(allow_nan=False,
                 allow_infinity=False))
def test_init_non_nan_non_inf_float(z):
    assert Integer(z).num == int(z)


@given(st.just(float("NaN")))
def test_init_nan_float_raises_value_error(z):
    with pt.raises(ValueError):
        Integer(z)


@given(st.just(float("inf")))
def test_init_inf_float_raises_value_error(z):
    with pt.raises(ValueError):
        Integer(z)


@given(st.decimals(allow_nan=False,
                   allow_infinity=False))
def test_init_non_nan_non_inf_decimal(z):
    assert Integer(z).num == int(z)


@given(st.just(Decimal("inf")))
def test_init_inf_decimal_raises_value_error(z):
    with pt.raises(ValueError):
        Integer(z)


@given(st.just(Decimal("NaN")))
def test_init_nan_decimal_raises_value_error(z):
    with pt.raises(ValueError):
        Integer(z)


@given(st.text(alphabet=string.digits,
               min_size=1))
def test_init_numeric_string(z):
    assert Integer(z).num == int(z)


@given(st.one_of([st.nothing(),
                  st.complex_numbers(),
                  st.text(alphabet=string.ascii_letters),
                  st.dates(),
                  st.none()]))
def test_init_raises_type_error(z):
    with pt.raises(ValueError):
        Integer(z)


# REPR TEST #
@given(st.integers())
def test_repr(z):
    assert Integer(z).__repr__() == "Integer({!r})".format(z)


# DUNDER METHOD TESTS #
@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_addition(z1, z2):
    assert z1 + z2 == Integer(z1) + Integer(z2)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_subtraction(z1, z2):
    assert z1 - z2 == Integer(z1) - Integer(z2)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_modulo(z1, z2):
    assert z1 % z2 == Integer(z1) % Integer(z2) == \
        z1 % Integer(z2) == Integer(z1) % z2


@given(st.integers(min_value=1))
def test_negative(z):
    assert -z == -Integer(z)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_multiplication(z1, z2):
    assert z1 * z2 == Integer(z1) * Integer(z2) == \
        z1 * Integer(z2) == z2 * Integer(z1)


@given(st.integers(max_value=1e15),
       st.integers(max_value=1e15))
def test_division(z1, z2):
    if z2 == 0:
        with pt.raises(ZeroDivisionError):
            Integer(z1) / z2
        with pt.raises(ZeroDivisionError):
            z1 / Integer(z2)
    else:
        assert (z1 / z2) == (Integer(z1) / Integer(z2)) == \
            (z1 / Integer(z2)) == (Integer(z1) / z2)


@given(st.integers(max_value=1e15),
       st.integers(max_value=5))
def test_exponentiation(z1, z2):
    assert (z1 ** z2 == Integer(z1) ** Integer(z2) and
            isinstance(Integer(z1) ** Integer(z2), Integer))


@given(st.integers(), st.integers())
def test_less_than(z1, z2):
    assert (z1 < z2) == (Integer(z1) < Integer(z2))


@given(st.integers(), st.integers())
def test_less_than_or_equal(z1, z2):
    assert (z1 <= z2) == (Integer(z1) <= Integer(z2))


@given(st.integers(), st.integers())
def test_greater_than(z1, z2):
    assert (z1 > z2) == (Integer(z1) > Integer(z2))


@given(st.integers(), st.integers())
def test_greater_than_or_equal(z1, z2):
    assert (z1 >= z2) == (Integer(z1) >= Integer(z2))


@given(st.integers(), st.integers())
def test_not_equal(z1, z2):
    assert (z1 != z2) == (Integer(z1) != Integer(z2))


# STATIC METHOD TEST #
@given(st.integers(), st.integers())
def test_gcd(a, b):
    assert Integer.gcd(a, b) == fractions.gcd(a, b)
    # if a == 0:
    #     assert Integer.gcd(a, b) == b
    # if b == 0:
    #     assert Integer.gcd(a, b) == a
    # else:
    #     assert max(Integer(a).divisors & Integer(b).divisors) \
    #         == Integer.gcd(a, b)


# METHOD TEST #
@given(st.integers(max_value=1e9), st.integers(max_value=10))
def test_is_perfect_power(z, k):
    if k <= 0:
        with pt.raises(ValueError):
            Integer(z).is_perfect_power(k)
    elif k == 1:
        assert Integer(z).is_perfect_power(k)
    else:
        if (z ** (1./k)).is_integer():
            assert Integer(z).is_perfect_power(k)
        else:
            assert not Integer(z).is_perfect_power(k)


@given(st.integers(max_value=1e5), st.integers())
def test_is_power_of(z, n):
    if z < 0:
        with pt.raises(NotImplementedError):
            Integer(z).is_power_of(n)
    elif z == 0:
        assert not Integer(z).is_power_of(n)
    elif z == 1:
        assert Integer(z).is_power_of(n)
    else:
        if n < 0:
            with pt.raises(ValueError):
                Integer(z).is_power_of(n)
        elif n == 0:
            assert not Integer(z).is_power_of(n)
        elif n == 1:
            assert not Integer(z).is_power_of(n)
        else:
            f = math.log(z, n)
            if f.is_integer():
                assert Integer(z).is_power_of(n)
            else:
                assert not Integer(z).is_power_of(n)


# PRIMALITY TEST #
@given(st.integers(max_value=1e15).filter(lambda x: x % 2 == 0))
def test_is_prime_false_for_any_even_integer(z):
    assert not is_prime(z)


# PROPERTY TEST #
@given(st.integers())
def test_binary(z):
    assert Integer(z).binary == bin(z)


@given(st.integers(max_value=1e8))
def test_decomposition(z):
    assert isinstance(Integer(z).decomposition, dict)
    assert z == reduce(lambda x, y: x * y,
                       (z for z in (k**v for k, v in
                                    Integer(z).decomposition.iteritems())))


@given(st.integers(max_value=1e5))
def test_divisors(z):
    # Using itertools, take Integer.decomposition and get every
    # combination of key ** value for every key and every 0, ..., value
    # THIS IS A SUFFICIENCY PROOF, BUT NOT NECESSESITY PROOF
    assert all(z % f == 0 for f in Integer(z).divisors)

    # THIS IS A COPOUT: COPYING THE LOGIC OF THE PROPERTY
    assert Integer(z).divisors == {x for x in xrange(1, z/2 + 1)
                                   if z % x == 0}


@given(st.integers(max_value=1e4))
def test_euler_totient(z):
    # Euler's product formula
    if z < 0:
        assert not Integer(z).euler_totient
    else:
        assert Integer(z).euler_totient == \
            int(reduce(operator.mul,
                       ((1 - 1. / k) for k in Integer(z).decomposition.keys()),
                       z))


@given(st.integers(max_value=1e3))
def test_factorial(z):
    if z < 0:
        with pt.raises(ValueError):
            Integer(z).factorial
    elif z == 0:
        assert Integer(z).factorial == 1
    else:
        assert Integer(z).factorial == math.factorial(z)


@given(st.integers(max_value=1e5))
def test_factorization(z):
    assert Integer(z).factorization == \
        ' * '.join((''.join((str(k), '^', str(v)))
                    for k, v in Integer(z).decomposition.iteritems()
                    ))
