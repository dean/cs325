import os
import random
import sys
import time
import urllib2

class Line(object):
    def __init__(self, m, b):
        self.m = m
        self.b = b
        self.visible = True

    def __repr__(self):
        return str(self)

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


def alg3(lines):
    visible = []
    for to_comp in lines:
        visible.append(to_comp)
        # Reduce the set of lines to only visible lines
        filter_covered(visible)
    return lines


def filter_covered(visible):
    if len(visible) <= 2:
        return visible
    l1, l2, to_comp = visible[-3:]
    y_intersect = find_y_intersection(l1, l2)
    to_comp_intersect = to_comp.m * (l1.b - l2.b) + to_comp.b * (l2.m - l1.m)
    if y_intersect < to_comp_intersect:
        # Modify reference so we can return a list of T/F
        l2.visible = False
        # Get rid of l2 
        visible.pop(-2)
        return filter_covered(visible)
    else:
        return visible


def alg4(lines):
    vis_lines = alg4_helper(lines)
    for line in lines:
        if line not in vis_lines:
            line.visible = False
    return lines


def alg4_helper(lines):
    if len(lines) <= 1:
        return lines

    half = len(lines)//2
    left = alg4_helper(lines[:half])
    right = alg4_helper(lines[half:])
    vis_lines = merge_visible_lines(left, right)
    return vis_lines


def merge_visible_lines(left, right):
    right = right[::-1] # Reverses so it's easier to index
    i, j = 1, 1
    check_left, check_right = len(left) > 1, len(right) > 1
    while (i < len(left) and check_left) or (j < len(right) and check_right):
        if check_left and i < len(left):
            to_comp = left[i]
            left_right_y = find_y_intersection(left[i-1], right[j-1])
            comp_y = to_comp.m * (left[i-1].b - right[j-1].b) + to_comp.b * (right[j-1].m - left[i-1].m)
            if left_right_y > comp_y:
                check_left = False
            else:
                i += 1
                if j - 2 >= 0:  # Ensure we don't cover the other side's recent line
                    to_comp = right[j-1]
                    new_intersect_y = find_y_intersection(left[i-1], right[j-2])
                    comp_y = to_comp.m * (left[i-1].b - right[j-2].b) + to_comp.b * (right[j-2].m - left[i-1].m)
                    if new_intersect_y > comp_y:
                        check_right = False
                        j-=1

        if check_right and j < len(right):
            to_comp = right[j]
            left_right_y = find_y_intersection(left[i-1], right[j-1])
            comp_y = to_comp.m * (left[i-1].b - right[j-1].b) + to_comp.b * (right[j-1].m - left[i-1].m)
            if left_right_y > comp_y:
                check_right = False
            else:
                j += 1
                if i - 2 >= 0:  # Ensure we don't cover the other side's recent line
                    to_comp = right[i-1]
                    new_intersect_y = find_y_intersection(left[i-2], right[j-1])
                    comp_y = to_comp.m * (left[i-2].b - right[j-1].b) + to_comp.b * (right[j-1].m - left[i-2].m)
                    if new_intersect_y > comp_y:
                        check_left = False
                        j+=1

    vis_lines = left[:i] + right[:j+1]
    return vis_lines


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print 'Usage: python assignment1.py [option]'
        print 'Options:'
        options = ['--test', '--time', '--solve']
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
            alg3_lines = [line.visible for line in alg3(lines)]
            alg4_lines = [line.visible for line in alg4(lines)]
            assert(ans == alg1_lines)
            assert(ans == alg2_lines)
            assert(ans == alg3_lines)
            assert(ans == alg4_lines)
    elif sys.argv[1] == '--time':
        random.seed(931915823)
        print 'Size |   Alg 1   |   Alg2   |   Alg3   |   Alg4   '
        timing_format = '{:<5} {:^11} {:^11} {:^11} {:^11}'
        for size in xrange(100, 1001, 100):
            ms = [random.randint(0, 100) for x in xrange(size)]
            bs = [random.randint(0, 100) for x in xrange(size)]
            lines = sorted(map(lambda x: Line(*x), zip(ms, bs)), key=lambda x: x.m)
            timing = []
            results = []
            for alg in [alg1, alg2, alg3, alg4]:
                start = time.clock()
                results.append(alg(lines))
                timing.append(time.clock() - start)
            # Check to make sure all algorithms have same output!
            a1, a2, a3, a4 = [[r.visible for r in result] for result in results]
            assert(a1 == a2 == a3 == a4)
            timing = [size] + timing
            print timing_format.format(*timing)
        for size in xrange(2000, 9001, 1000):
            ms = [random.randint(-9000, 9000) for x in xrange(size)]
            bs = [random.randint(-9000, 9000) for x in xrange(size)]
            lines = sorted(map(lambda x: Line(*x), zip(ms, bs)), key=lambda x: x.m)
            timing = []
            results = []
            for alg in [alg3, alg4]:
                start = time.clock()
                results.append(alg(lines))
                timing.append(time.clock() - start)
            # Check to make sure all algorithms have same output!
            a3, a4 = [[r.visible for r in result] for result in results]
            assert(a3 == a4)
            timing = [size, '', ''] + timing + [0]
            print timing_format.format(*timing)
    elif sys.argv[1] == '--solve':
        test_set_url = 'http://web.engr.oregonstate.edu/~glencora/cs325/visibility/solve_these.txt'
        test_sets = urllib2.urlopen(test_set_url).read().strip()
        ans = []
        for test_set in test_sets.split('\n'):
            test_set = '[' + test_set + ']'
            ms, bs = eval(test_set)
            lines = sorted(map(lambda x: Line(*x), zip(ms, bs)), key=lambda x: x.m)
            alg1_lines = [line.visible for line in alg1(lines)]
            alg2_lines = [line.visible for line in alg2(lines)]
            alg3_lines = [line.visible for line in alg3(lines)]
            alg4_lines = [line.visible for line in alg3(lines)]
            assert(alg1_lines == alg2_lines == alg3_lines == alg4_lines)
            ans.append(','.join((str(l) for l in alg1_lines)))

        with open('solve_these_answers.txt', 'w') as f:
            f.write('\n'.join(ans))
