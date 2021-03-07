from zn import Zn, ZnNumber
from ui import ConsoleUI

if __name__ == '__main__':
    ConsoleUI().run()

'''
# Test các giải thuật

if __name__ == '__main__':
    # Test +, -, *
    n = 39
    a = ZnNumber(5, n)
    b = ZnNumber(-7, n)
    print(a) # Override hàm print dùng riêng cho ZnNumber
    print(b)
    print(a + b) # Dùng được dấu +, -, * như số bình thường
    c = a
    c -= b # Dùng kết hợp với dấu =
    print(c)
    print(a * b * a * b) # Chain liên tục

    # Test nghịch đảo nhân
    n = 39
    a = ZnNumber(5, n)
    print(a.mul_inv()) # Nên ra 8 vì 5 * 8 = 40 = 1 trong Z_39

    # Test luỹ thừa nhanh 
    # Kiểm tra đáp án dùng web này (hoặc google hoặc chỗ nào tính được số lớn):
    # https://www.mtholyoke.edu/courses/quenell/s2003/ma139/js/powermod.html
    n = 39
    a = ZnNumber(11, n)
    print(a ** 23) # 11 ^ 23 xấp xỉ 8.95e23, = 32 trong Z_39
'''

'''
# Chỗ test tào lao, xin đừng quan tâm

if __name__ == '__main__':
    s = '-5 + (3 - 8) + 4 * 13 + 2'

    import re

    #s = re.sub(r'\s+', '', s)
    r = re.split(r'([+-]?[0-9]+)', s)
    print(r)
    a = 'res = '
    c = ''
    j = 0
    g = {}
    for i in r:
        if i != '':
            if re.match(r'^[-]?[0-9]+$', i):
                b = 'a' + str(j)
                g[b] = ZnNumber(int(i), 39)
                c += b + '=ZnNumber(' + i + ',39);'
                j += 1
                a += b
            else:
                a += i
    g['res'] = None
    print(a)
    exec(a, g)
    print(g['res'])
    
'''

