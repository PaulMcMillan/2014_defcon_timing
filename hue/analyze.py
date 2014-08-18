#!/usr/bin/env python
import pyshark
from decimal import Decimal
from collections import defaultdict
import math
import time
import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint
import os

DATA_DIR = 'data'
start_time = time.time()

results = defaultdict(list)
count = 0
stream = 0
loop_time = time.time()
while True:
    for filename in os.listdir(DATA_DIR):
        # this is terrible
        if not filename.endswith('.pcap'):
            continue
        in_filename = os.path.join(DATA_DIR, filename)
        out_filename = in_filename + '.parsed'
        if os.path.exists(out_filename):
            continue
        print "Analyzing ", in_filename
        data = pyshark.FileCapture(
            in_filename,
            keep_packets=False,
            display_filter="")
        outfile = open(out_filename, 'w')

        results = defaultdict(list)
        for p in data:
            if p.transport_layer == 'TCP':
                stream = p.tcp.stream
                if stream in results:  # already have a series going
                    if p.ip.src == results[stream][0]:  # only response packets
                        results[stream].append(p.sniff_timestamp)
                        if p.tcp.flags_fin == '1':  # the last response packet
                            outfile.write(','.join(results[stream]) + '\n')
                            if not int(stream) % 100:
                                print stream, time.time() - start_time
                            del results[stream]
                elif p.highest_layer == 'HTTP':
                    # we're starting a new query
                    if getattr(p.http, 'request_method', None) == 'GET':
                        results[stream].append(p.http.host)
                        results[stream].append(p.http.request_uri)
                        results[stream].append(p.sniff_timestamp)
    time.sleep(2)
