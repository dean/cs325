import random
import time
import urllib2
import sys

class Line(object):
    def __init__(self, m, b):
        self.m = m
        self.b = b
        self.visible = True

    def __str__(self):
        return "<Line Object: %d, %d, %s>" % (self.m, self.b, self.visible)


def f(line, x):
    return line.m * x + line.b


def find_y_intersection(line1, line2):
    return line1.m * (line1.b - line2.b) + line1.b * (line2.m - line1.m)


def alg1(lines):
    for j, l1 in enumerate(lines):
        for i, l2 in enumerate(lines[j+1:], j+1):
            for k, l3 in enumerate(lines[i+1:], i+1):
                jk_y = find_y_intersection(l1, l3)
                i_y = l2.m * (l1.b - l3.b) + l2.b * (l3.m - l1.m)
                if jk_y > i_y:
                    l2.visible = False
    return lines


def alg2(lines):
    for j, l1 in enumerate(lines):
        for i, l2 in enumerate(lines[j+1:], j+1):
            for k, l3 in enumerate(lines[i+1:], i+1):
                if not l2.visible:
                    continue
                jk_y = find_y_intersection(l1, l3)
                i_y = l2.m * (l1.b - l3.b) + l2.b * (l3.m - l1.m)
                if jk_y > i_y:
                    l2.visible = False
    return lines


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print 'Usage: python assignment1.py [option]'
        print 'Options:'
        options = ['--test', '--time']
        print '\n'.join(map(lambda x:'\t'+ x, options))
        sys.exit()
    elif sys.argv[1] == '--test':
        test_set_url = 'http://web.engr.oregonstate.edu/~glencora/cs325/visibility/test_set.txt'
        test_sets = urllib2.urlopen(test_set_url).read().strip()
        for test_set in test_sets.split('\n'):
            test_set = '[' + test_set + ']'
            ms, bs, ans = eval(test_set)
            lines = sorted(map(lambda x: Line(*x), zip(ms, bs)), key=lambda x: x.m)
            alg1_lines = [line.visible for line in alg1(lines)]
            alg2_lines = [line.visible for line in alg2(lines)]
            # alg3_lines = [line.visible for line in alg3(lines)]
            assert(ans == alg1_lines)
            assert(ans == alg2_lines)
            # assert(ans == alg3_lines)
    elif sys.argv[1] == '--time':
        random.seed(931915823)
        print 'Size |   Alg 1   |   Alg2   |   Alg3   '
        timing_format = '{:<5} {:^11} {:^11} {:^11}'
        for size in xrange(100, 1001, 100):
            ms = [random.randint(0, 100) for x in xrange(size)]
            bs = [random.randint(0, 100) for x in xrange(size)]
            lines = sorted(map(lambda x: Line(*x), zip(ms, bs)), key=lambda x: x.m)
            timing = []
            for alg in [alg1, alg2]:
                start = time.clock()
                alg(lines)
                timing.append(time.clock() - start)
            timing = [size] + timing + [0]
            print timing_format.format(*timing)

        for size in xrange(2000, 9001, 1000):
            # alg3
            continue
