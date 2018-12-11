from hypothesis import given, strategies as st


def is_woodall(z):
    """ Is there an int, k, such that
    `z` = k * 2**k - 1?
    """
    if z < 1:
        return False
    w = z + 1
    woodall = lambda k, w=w: k * 2 ** k == w
    range_of_k_to_check = range(1, 4) if z < 64 else \
        range(1, int(pow(w, 1/3)) + 1)  # 1,..., floor of cube root of z + 1
    return any(map(woodall, range_of_k_to_check))


def naive_is_woodall(z):
    """An implementation of the "naive"
    algorithm to determine Woodallity of z"""
    k = 1
    w = z + 1
    candidate = k*2**k
    while candidate <= w:
        if w == candidate:
            return True
        k += 1
        candidate = k*2**k
        continue
    else:
        return False


@given(st.integers(max_value=7.6e9))
def test_is_woodall_1(z):
    woodalls = \
        {1, 7, 23, 63, 159, 383, 895,
         2047, 4607, 10239, 22527,
         49151, 106495, 229375, 491519,
         1048575, 2228223, 4718591,
         9961471, 20971519, 44040191,
         92274687, 192937983, 402653183,
         838860799, 1744830463, 3623878655, 7516192767}
    if z not in woodalls:
        assert not is_woodall(z)
    else:
        assert is_woodall(z)


@given(st.integers(max_value=1e15))  # for brevity's sake
def test_is_woodall_2(z):
    if z < 1:
        assert not is_woodall(z)
    if naive_is_woodall(z):
        assert is_woodall(z)
    else:
        assert not is_woodall(z)