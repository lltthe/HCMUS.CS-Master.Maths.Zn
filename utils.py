""" Useful functions to use in need
"""

def int_check(num):
    """ Checking if a value is an integer
    Accepting integer value initially stored as float
    """
    if isinstance(num, int):
        return True, num
    elif isinstance(num, float) and num.is_integer():
        return True, int(num)
    else:
        return False, num

def int_check_strict(num, msg = None, condition = lambda x : True):
    """ Checking if a value is an integer satisfying some condition
    Raising excepting if not
    """
    is_num_int, num = int_check(num)
    if not (is_num_int and condition(num)):
        raise ValueError(msg) if msg else ValueError
    return num

def bezout(a, b):
    """ Using extended Euclidean algorithm on 2 integers a & b to find:
    * Greatest common divisor: gcd
    * Bezout coefficients: x & y
    satisfying: ax + by = gcd
    """
    PARAM_ERR_MSG = 'Consider using Bezout for integers >= 0 only'
    PARAM_COND = lambda x : x >= 0
    a = int_check_strict(a, PARAM_ERR_MSG, PARAM_COND)
    b = int_check_strict(b, PARAM_ERR_MSG, PARAM_COND)

    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = egcd(b % a, a)
            return gcd, y - (b // a) * x, x

    return egcd(a, b)

def gcd(a, b):
    """ Finding greatest common divisors of 2 integers a & b
    """
    PARAM_ERR_MSG = 'Consider finding greatest common divisor for integers only'
    a = int_check_strict(a, PARAM_ERR_MSG)
    b = int_check_strict(b, PARAM_ERR_MSG)

    def _gcd(a, b):
        if a == 0:
            return b
        return _gcd(b % a, a)

    return _gcd(a, b)