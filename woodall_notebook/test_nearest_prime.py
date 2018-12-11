#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hypothesis import given, strategies as st
from more_itertools import spy


def is_prime(z):
    """Takes an integer and returns whether that integer is prime. This
    particular implementation from http://stackoverflow.com/a/27946768
    Args:
        z (int): Integer the primality of which to ascertain
    Returns:
        (bool): Whether `z` is prime
    """
    if z <= 1:
        return False
    for n in range(2, int(z ** 0.5 + 1)):
        if not z % n:
            return False
    else:
        return True


def functional_is_prime(z):
    """Takes an integer and returns whether that integer is prime. This
    particular implementation from http://stackoverflow.com/a/27946768
    Args:
        z (int): Integer the primality of which to ascertain
    Returns:
        (bool): Whether `z` is prime
    """
    if z <= 1:
        return False
    try:
        next(filter(lambda n, z=z: not z % n,
                    range(2, int(z ** 0.5 + 1))))
    except StopIteration:
        return True
    else:
        return False


def primes():
    """ Sieve of Eratosthenes variation to generate primes
    """
    found = list()
    candidate = 2
    while True:
        # if not any(candidate % prime == 0 for prime in found):
        if all(candidate % prime for prime in found):
            yield candidate
            found.append(candidate)
        candidate += 1


def generate_primes_before_n(n):
    """ Generate all z in Z such that z is prime and z < `n`
    """
    p = primes()
    largest_so_far = next(p)
    while largest_so_far < n:
        yield largest_so_far
        largest_so_far = next(p)


def generate_primes_after_n(n):
    """ Generate all z in Z such that z is prime and z > `n`.
    WARNING: this is an infinite generator so consuming it
    will cause OutOfMemoryError
    """
    p = primes()
    largest_so_far = next(p)
    while largest_so_far < n:
        largest_so_far = next(p)

    yield largest_so_far
    while True:
        yield next(p)


def sequence():
    """ Generate the following sequence:
    0, 1, -2, 3, -4, 5, -6, 7, -8, ...
    """
    n = 1
    yield 0
    while True:
        yield n
        sign = -1 if n % 2 else 1
        n = sign * (abs(n) + 1)


def nearest_prime(z):
    """ Given integer, `z`, return the nearest prime(s) to `z`
    """
    if z <= 0:
        return (2,)
    elif is_prime(z):
        return (z,)
    z_, s = z, sequence()

    while not is_prime(z):
        z += next(s)
    else:
        nearest_away = z - z_

    # Is there another prime equidistant?
    return (z,) if not is_prime(z_ - nearest_away) else (z, z_ - nearest_away)


@given(st.integers(min_value=0))
def test_sequence(maximum):
    seq = sequence()
    if maximum == 0:
        assert next(seq) == 0
    elif maximum == 1:
        next(seq)
        assert next(seq) == 1
    else:
        s = spy(seq, maximum)[0]
        for i in range(1, len(s)):
            assert abs(s[i]) == abs(s[i-1]) + 1
            assert s[i] + s[i-1] in (1, -1)


@given(st.integers())
def test_nearest_prime(z):
    if z <= 0:
        assert nearest_prime(z) == (2,)
    elif is_prime(z):
        assert nearest_prime(z) == (z,)
    else:
        closest_before_z = max(generate_primes_before_n(z))
        closest_after_z = next(generate_primes_after_n(z))
        if abs(z - closest_before_z) == abs(z - closest_after_z):
            assert nearest_prime(z) == (closest_before_z, closest_after_z) or \
                nearest_prime(z) == (closest_after_z, closest_before_z)
        else:
            assert nearest_prime(z) == (min(closest_after_z, closest_before_z,
                                            key=lambda n, z=z: abs(z-n)),)
