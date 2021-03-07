from utils import int_check_strict, bezout, gcd

ZN_ERR_MSG_N = 'Z_n structure requires n to be integer >= 2'
ZN_COND_N = lambda n : n >= 2
ZN_ERR_MSG_NUM = 'Z_n structure only works with integers'
ZN_ERR_MSG_BASE = 'Numbers are not considered in the same Z_n structure (having different base n)'
ZN_ERR_MSG_EXP = 'Only consider integer exponent >= 0'
ZN_COND_EXP = lambda m : m >= 0
ZN_ERR_MSG_INV = '{a} is not multiplicative inversible in Z_{n} because ({a}, {n}) = {gcd} > 1'

def totient(n): # Hàm phi Euler
    n = int_check_strict(n, ZN_ERR_MSG_N, ZN_COND_N)
    phi = n
    for i in range(2, int(n ** .5) + 1):
        if n % i == 0:
            phi -= phi / i
            while n % i == 0:
                n //= i
    if n > 1:
        phi -= phi / n
    return int(phi)

class ZnNumber:
    def __init__(self, val, base_n):
        self.n = base_n
        self.original = val
        self.reduced = ZnNumber.reduce(val, base_n)

    @staticmethod
    def reduce(val, base_n):
        n = int_check_strict(base_n, ZN_ERR_MSG_N, ZN_COND_N)
        val = int_check_strict(val, ZN_ERR_MSG_NUM)        
        return val % n

    @staticmethod
    def is_same_base(a, b):
        return a.n == b.n

    @staticmethod
    def is_same_base_strict(a, b):
        if not ZnNumber.is_same_base(a, b):
            raise ValueError(ZN_ERR_MSG_BASE)
        return True

    @staticmethod
    def totient(n):
        return totient(n)

    def __add__(self, x):
        ZnNumber.is_same_base_strict(self, x)
        return ZnNumber(self.original + x.original, self.n)

    def __neg__(self):
        return ZnNumber(-self.original, self.n)

    def __sub__(self, x):
        return self.__add__(-x)

    def __mul__(self, x):
        ZnNumber.is_same_base_strict(self, x)
        return ZnNumber(self.original * x.original, self.n)

    def __str__(self):
        if self.original == self.reduced:
            return '{} in Z_{}'.format(self.reduced, self.n)
        return '{} = {} in Z_{}'.format(self.original, self.reduced, self.n)

    def __pow__(self, m):
        m = int_check_strict(m, ZN_ERR_MSG_EXP, ZN_COND_EXP)

        n = self.n
        a = self.reduced
        result = 1

        while m > 0:
            if m % 2 == 1:
                result *= a
                if result >= n:
                    result %= n
            m //= 2
            a *= a
            if a >= n:
                a %= n

        return ZnNumber(result, n)

    def mul_inv(self, mode = 'bezout'):
        n = self.n
        a = self.reduced

        g = gcd(a, n)
        if g > 1:
            return ZN_ERR_MSG_INV.format(a = self.original, n = n, gcd = g)

        if mode == 'bezout':
            _, inv, _ = bezout(a, n)
            return ZnNumber(inv % n, n)
        elif mode == 'euler':
            return self ** (ZnNumber.totient(n) - 1)
        else:
            raise ValueError

# Có thể hoạt động độc lập với class ZnNumber ở trên
# Mỗi class đều đủ để giả lập Z_n
class Zn:
    def __init__(self, n):
        n = int_check_strict(n, ZN_ERR_MSG_N, ZN_COND_N)
        self.n = n

    def reduce(self, num):
        num = int_check_strict(num, ZN_ERR_MSG_NUM)        
        return num % self.n

    def add_int(self, a, b):
        a = int_check_strict(a, ZN_ERR_MSG_NUM)
        b = int_check_strict(b, ZN_ERR_MSG_NUM)
        original_sum = a + b
        return self.reduce(original_sum), original_sum

    def sub_int(self, a, b):
        return self.add_int(a, -b)

    def mul_int(self, a, b):
        a = int_check_strict(a, ZN_ERR_MSG_NUM)
        b = int_check_strict(b, ZN_ERR_MSG_NUM)
        original_product = a * b
        return self.reduce(original_product), original_product

    def pow_int(self, a, m):
        a = int_check_strict(a, ZN_ERR_MSG_NUM)
        m = int_check_strict(m, ZN_ERR_MSG_EXP, ZN_COND_EXP)

        n = self.n
        a %= n
        result = 1

        while m > 0:
            if m % 2 == 1:
                result *= a
                if result >= n:
                    result %= n
            m //= 2
            a *= a
            if a >= n:
                a %= n
        
        return result

    def mul_inv_int(self, num, mode = 'bezout'):
        num = int_check_strict(num, ZN_ERR_MSG_NUM)
        n = self.n

        g = gcd(num, n)
        if g > 1:
            return ZN_ERR_MSG_INV.format(a = num, n = n, gcd = g)

        if mode == 'bezout':
            _, inv, _ = bezout(num % n, n)
            return inv % n
        elif mode == 'euler':
            return self.pow_int(num, self.totient() - 1)
        else:
            raise ValueError

    def __str__(self):
        return 'Z_{}'.format(self.n)

    def totient(self):
        return totient(self.n)

    # Các hàm bên dưới giúp kết hợp với class ZnNumber
    # Chỉ nhằm sử dụng cho trực quan hơn

    def consider(self, num):
        return ZnNumber(num, self.n)

    def add(self, a : ZnNumber, b : ZnNumber):
        return a + b

    def sub(self, a : ZnNumber, b : ZnNumber):
        return a - b

    def mul(self, a : ZnNumber, b : ZnNumber):
        return a * b

    def pow(self, a : ZnNumber, m : ZnNumber):
        return a ** m

    def mul_inv(self, a : ZnNumber, mode = 'bezout'):
        return a.mul_inv(mode)