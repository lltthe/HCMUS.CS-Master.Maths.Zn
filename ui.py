import sys
import argparse as ap

from zn import Zn, ZnNumber, ZN_COND_N
from utils import int_check_strict

class ConsoleUI():
    def __init__(self):
        pass

    def input_int(self, msg, err_msg, cond = lambda x: True):
        while True:
            try:
                x = float(input(msg))
                x = int_check_strict(x, None, cond)
            except ValueError:
                print(err_msg)
                continue
            else:
                print('--- Received: {}'.format(x))
                return x

    def run(self):
        if len(sys.argv) == 1:
            print('======= Z_n STRUCTURE EMULATOR =======\n')

            while True:
                n = self.input_int('Let n = ', 'Sorry! Please input an integer n >= 2...', ZN_COND_N)
                self.zn = Zn(n)

                a = self.input_int('Please input a number "a" to calculate: ', 'Sorry! Please input a valid integer...')
                self.a = self.zn.consider(a)

                b = self.input_int('And a second number "b": ', 'Sorry! Please input a valid integer...')
                self.b = self.zn.consider(b)

                if not self.exec():
                    return
   
        else:
            parser = ap.ArgumentParser(description = 'Z_n STRUCTURE EMULATOR', epilog = 'Demonstrating calculations e.g. +, -, *, finding multiplicative inverse, and fast modular exponentiation!\n')
            parser.add_argument('n', action = 'store', type = int, help = 'Base n for Z_n structure')
            parser.add_argument('a', action = 'store', type = int, help = 'A number to calculate')
            parser.add_argument('b', action = 'store', type = int, help = 'And a second number')

            try:
                args = parser.parse_args()
            except:
                parser.print_help()
                return

            if not ZN_COND_N(args.n):
                print('ERROR: n must be >= 2! Exitting...')
            else:
                self.zn = Zn(args.n)
                self.a, self.b = self.zn.consider(args.a), self.zn.consider(args.b)
                self.exec(False)

    # A good website to compare result: https://defuse.ca/big-number-calculator.htm
    def exec(self, to_loop = True):
        a, b, zn = self.a, self.b, self.zn

        print('\n---- Considering {} ----\n'.format(zn))

        print('a = {}'.format(a))
        print('b = {}'.format(b))
        print()

        print('a + b = {}'.format(a + b))
        print('a - b = {}'.format(a - b))
        print('a * b = {}'.format(a * b))
        print()

        def mul_inv_proc(num : ZnNumber):
            res = num.mul_inv()
            if isinstance(res, ZnNumber):
                print('Multiplicative inverse of {}:'.format(num.original))
                print('--- using Bezout\'s Identity through extended Euclidean algorithm: {}'.format(res))
                print('--- using Euler\'s Theorem and fast modular exponentiation: {}'.format(num.mul_inv(mode = 'euler')))
            else:
                print(res)

        mul_inv_proc(a)
        mul_inv_proc(b)
        print()

        EXPANDER = 1024
        print('a ^ ({} * b) using fast modular exponentiation = {}'.format(EXPANDER, a ** (b.reduced * EXPANDER)))
        print('\n--------------------\n')

        if not to_loop:
            return

        while True:
            loop = input('Continue? [y/n] ').lower()
            if loop == 'y':
                return True
            elif loop == 'n':
                return False        