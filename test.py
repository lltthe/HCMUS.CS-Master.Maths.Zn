""" For testing and experiments

Generating data for visual demonstration...
For internal uses only!
"""

import random, time
from alive_progress import alive_bar

from zn import Zn, ZnNumber

FIN = 'tests_in.txt'
FOUT = 'tests_out.txt'

def generate():
    BITS = [32, 64, 128, 256, 512, 1024]
    N_SAMPLES = 10
    N = [2147483647, 67280421310721]

    with open(FIN, 'w') as f:
        for bit in BITS:
            f.write('%s ' % bit)
        f.write('\n%s\n' % N_SAMPLES)
        for n in N:
            f.write('%s ' % n)
        f.write('\n')

        for bit in BITS:
            for i in range(N_SAMPLES):
                a = random.getrandbits(bit)
                b = random.getrandbits(bit)
                f.write(str(a) + ' ' + str(b) + '\n')

def process_sample(a : ZnNumber, b : ZnNumber):
    res = [a.original, b.original, a.reduced, b.reduced, (a + b).reduced, (a - b).reduced, (a * b).reduced]

    res_time = []

    t = time.perf_counter()
    res += [a.mul_inv().reduced, b.mul_inv().reduced]
    t = time.perf_counter() - t
    t /= 2
    res_time.append(t)

    t = time.perf_counter()
    res += [a.mul_inv(mode = 'euler').reduced, b.mul_inv(mode = 'euler').reduced]
    t = time.perf_counter() - t
    t /= 2
    res_time.append(t)

    t = time.perf_counter()
    res.append((a ** b.original).reduced)
    t = time.perf_counter() - t
    res_time.append(t)

    return res, res_time

def process():
    fin = open(FIN, 'r')
    fout = open(FOUT, 'w')

    bits = [int(bit) for bit in next(fin).split(' ') if bit != '\n']
    n_samples = int(next(fin))
    ns = [int(n) for n in next(fin).split(' ') if n != '\n']
    total = n_samples * len(bits) * len(ns)
    
    ints = []
    for line in fin:
        a, b = [int(num) for num in line.split(' ')]
        ints.append((a, b))

    running_times = []
    with alive_bar(total) as bar:
        for n in ns:
            print('----- In Z_{} -----'.format(n))
            zn = Zn(n)
            mib = []
            mie = []
            me = []

            for a, b in ints:
                res, res_time = process_sample(zn.consider(a), zn.consider(b))
                res += res_time
                for r in res:
                    fout.write('%s ' % r)
                fout.write('\n')
                mib.append(res_time[0])
                mie.append(res_time[1])
                me.append(res_time[2])
                bar()

            sums = [0, 0, 0]
            for i in range(len(mib)):
                sums[0] += mib[i]
                sums[1] += mie[i]
                sums[2] += me[i]

                if i % n_samples == n_samples - 1:
                    avgs = [s / n_samples for s in sums]
                    for avg in avgs:
                        fout.write('%s ' % avg)
                    fout.write('\n')
                    sums = [0, 0, 0]

            fout.write('------------------------\n')
                            
    fin.close()
    fout.close()

#generate()
process()