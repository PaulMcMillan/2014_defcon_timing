import pyshark
from decimal import Decimal

def foo(short=False):
    if short:
        d2 = pyshark.FileCapture('data2_short.pcap', keep_packets=False)
        d5 = pyshark.FileCapture('data5_short.pcap', keep_packets=False)
    else:
        d2 = pyshark.FileCapture('data2.pcap', keep_packets=False)
        d5 = pyshark.FileCapture('data5.pcap', keep_packets=False)

    results = []
    for pd2, pd5 in zip(d2, d5):
        r = Decimal(pd5.sniff_timestamp) - Decimal(pd2.sniff_timestamp)
        results.append(r)
        print r
    avg = sum(results) / len(results)
    print 'Avg: ', avg * 10 ** 3
    return avg

a = foo()
b = foo(short=True)
print "Diff:", (a - b) * 10 ** 3
