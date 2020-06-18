#!/usr/bin/env python

import argparse
from acq400_hapi import intSIAction
from acq400_hapi import intSI

import numpy as np
import math


'''
acq2106_181 Receiver:0 nrx:3511 cur:5:37771587 ts:5:38557949 adj:5:38557949 diff:19659050 OK
acq2106_200 Receiver:0 nrx:3511 cur:5:37773457 ts:5:38557949 adj:5:38557949 diff:19612300 OK
acq2106_172 Receiver:0 nrx:3511 cur:5:37772467 ts:5:38557949 adj:5:38557949 diff:19637050 OK
acq2106_182 Receiver:0 nrx:3512 cur:6:37766554 ts:6:38558156 adj:6:38558156 diff:19790050 OK
'''


def mmm(stats, base):
    max = -999999999
    min = 999999999
    sum = 0
    sumsq = 0
    nsum = 0

#    print("mmm len {} {}".format(len(stats), stats))
#    print("{} {} {} {}".format(max, min, sum, sumsq))

    for xx in stats:
        delta = base-xx
        if delta > max:
            max = delta
        if delta < min:
            min = delta
        if delta > 0:
            sum += delta
            sumsq += delta*delta
            nsum += 1
# scale to usecs
    rc = (min, max, sum/nsum, math.sqrt(sumsq/nsum))
    rc = [int(x/1000) for x in rc]
#    print(rc)
    return rc

def analyse(args):
    uuts = {}
    with open(args.log[0]) as f:
        for line in f:
            try:
                (uut, rx, nrx, cur, ts, adj, diff, stat) = line.split(' ')
                if not uut in uuts.keys():
                    uuts[uut] = {}
                uuts[uut][int(nrx.split(':')[1])] = { 'diff': int(diff.split(':')[1]), 'stat': stat }
                #print(uuts[uut][int(nrx.split(':')[1])])
            except ValueError:
                pass

    for u, samples in uuts.items():
        m1, m2, m3, m4 = mmm([samples[i]['diff'] for i in samples.keys()], float(args.wrtd_delta_ns))
        print("{} min:{:4d} max:{:4d} mean:{:4d} rms:{:4d} usec".format(u, m1, m2, m3, m4))



def run_main():
    parser = argparse.ArgumentParser(description='wrtd_analysis')
    parser.add_argument('--verbose', default=0, type=int)
    parser.add_argument('--wrtd_delta_ns', default='50M', action=intSIAction, help="set delay NS")
    parser.add_argument('log', nargs='+', help="log files")
    analyse(parser.parse_args())

# execution starts here

if __name__ == '__main__':
    run_main()