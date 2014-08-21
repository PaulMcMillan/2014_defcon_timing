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
import click

@click.command()
@click.argument('in_files', type=click.File('rb'), nargs=-1)
@click.option('--reparse', is_flag=True, default=False)
def parse_file(in_files, reparse):
    start_time = time.time()
    for in_file in in_files:
        out_filepath = in_file.name + '.parsed'
        if not reparse and os.path.isfile(out_filepath):
            continue
        print "Parsing ", in_file.name
        data = pyshark.FileCapture(
            in_file,
            keep_packets=False,
            display_filter="")

        results = defaultdict(list)
        with open(out_filepath, 'w') as outfile:
            for p in data:
                if p.transport_layer == 'TCP':
                    stream = p.tcp.stream
                    if stream in results:  # already have a sequence going
                        if p.ip.src == results[stream][0]:  # only responses
                            results[stream].append(p.sniff_timestamp)
                            if p.tcp.flags_fin == '1':  # the last response
                                outfile.write(','.join(results[stream]) + '\n')
                                if not int(stream) % 300:
                                    print stream, time.time() - start_time
                                del results[stream]
                    elif p.highest_layer == 'HTTP':
                        # we're starting a new query
                        if getattr(p.http, 'request_method', None) == 'GET':
                            results[stream].append(p.http.host)
                            results[stream].append(p.http.request_uri)
                            results[stream].append(p.sniff_timestamp)


if __name__ == '__main__':
    parse_file()
