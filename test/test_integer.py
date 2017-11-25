from decimal import Decimal
import fractions
from hypothesis import given, strategies as st
from integer import is_prime, Integer
import itertools as it
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


@given(st.integers(max_value=1e4), st.integers())
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


@given(st.integers(max_value=1e4))
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


@given(st.integers(max_value=1e4))
def test_factorization(z):
    assert Integer(z).factorization == \
        ' * '.join((''.join((str(k), '^', str(v)))
                    for k, v in Integer(z).decomposition.iteritems()
                    ))


@given(st.integers(max_value=1e3))
def test_goldbach_partitions(z):
    expected = set()
    if z % 2:
        assert Integer(z).goldbach_partitions == expected
    else:
        expected = set(it.ifilter(lambda x: is_prime(x[0]) and is_prime(x[1]),
                                  it.izip(xrange(z/2+1),
                                          (z - x for x in xrange(z/2+1)))))
        assert Integer(z).goldbach_partitions == expected


@given(st.integers(max_value=1e4))
def test_is_mersenne(z):
    if z <= 0:
        assert not Integer(z).is_mersenne
    else:
        if math.log(z+1, 2).is_integer():
            assert Integer(z).is_mersenne
        else:
            assert not Integer(z).is_mersenne


@given(st.integers(max_value=1e4))
def test_is_mersenne_prime(z):
    if z <= 0:
        assert not Integer(z).is_mersenne_prime
    else:
        if math.log(z+1, 2).is_integer() and is_prime(z):
            assert Integer(z).is_mersenne_prime
        else:
            assert not Integer(z).is_mersenne_prime


@given(st.integers(max_value=1e4))
def test_is_perfect(z):
    Z = Integer(z)
    if sum(Z.divisors) == Z.num:
        assert Z.is_perfect
    else:
        assert not Z.is_perfect


@given(st.integers(max_value=1e4))
def test_is_woodall(z):
    # THIS IS A COPOUT SO THAT THE TEST WILL RUN QUICKLY
    if z not in {1, 7, 23, 63, 159, 383, 895, 2047, 4607, 10239, 22527, 49151}:
        assert not Integer(z).is_woodall
    else:
        assert Integer(z).is_woodall


@given(st.integers(max_value=1e4))
def test_is_woodall_prime(z):
    # THIS IS A COPOUT SO THAT THE TEST WILL RUN QUICKLY
    if z not in {7, 23, 383}:
        assert not Integer(z).is_woodall_prime
    else:
        assert Integer(z).is_woodall_prime


@given(st.integers(max_value=1e4))
def test_nearest_prime(z):
    if z <= 1:
        assert Integer(z).nearest_prime == (2,)
    elif z == 9:
        assert Integer(z).nearest_prime == (7, 11)
    elif is_prime(z):
        assert Integer(z).nearest_prime == (z,)
    else:
        # THIS IS A COPOUT SO THAT THE TEST WILL RUN QUICKLY
        pass


@given(st.integers(max_value=1e4))
def test_Omega(z):
    assert Integer(z).Omega == sum(Integer(z).decomposition.itervalues())


@given(st.integers(max_value=1e4))
def test_omega(z):
    Z = Integer(z)
    assert Z.omega == sum(1 for _ in
                          it.ifilter(lambda x: is_prime(x) and not z % x,
                                     xrange(0, z+1)))


@given(st.integers(max_value=1e4))
def test_parity(z):
    if z % 2:
        assert Integer(z).parity == 'Odd'
    else:
        assert Integer(z).parity == 'Even'


@given(st.integers(max_value=1e4))
def test_pi(z):
    assert Integer(z).pi == sum(1 for x in xrange(2, z + 1) if is_prime(x))


@given(st.integers(max_value=1e4))
def test_primality(z):
    if is_prime(z):
        assert Integer(z).primality == "Prime"
    else:
        assert Integer(z).primality == "Composite"


@given(st.integers(max_value=1e4))
def test_sigma(z):
    Z = Integer(z)
    assert Z.sigma == sum(it.ifilterfalse(lambda x: z % x,
                                          xrange(1, z / 2 + 1)))


@given(st.integers(max_value=1e4))
def test_tau(z):
    if z <= 0:
        assert Integer(z).tau == 0
    elif z == 1:
        assert Integer(z).tau == 1
    else:
        Z = Integer(z)
        assert Z.tau == reduce(operator.mul,
                               (z + 1 for z in Z.decomposition.itervalues()))


@given(st.integers(max_value=1e4))
def test_totatives(z):
    assert isinstance(Integer(z).totatives, set)
    if z <= 0:
        assert not Integer(z).totatives
    else:
        assert Integer(z).totatives == {x for x in xrange(1, z + 1)
                                        if Integer.gcd(z, x) == 1}
