Chronotools
-----------

This is a suite of tools designed to assist with the development and
exploitation of network-based timing attacks.

This happens with 3 distinct components:
 * Generate - Interact with the target
 * Collect - Collect data about your interactions
 * Analyze - Filter, extract features, and statistically analyze your data


Generate
--------

A simple wrapper to generate traffic to be monitored. This can help
handle creating multiple sample groups.

Generate can (but is not required to) trigger collect.

Collect
-------

Collect packet logs of the interactions that come from the generate stage.

Roughly a wrapper around `tcpdump -j adapter -I eth0 -w outfile`.

It will check your network adapter settings, warn you if any are
problematic, and tell you how to optimize them.

Collect is not required to be run from the same machine that is
running generate, but it is usually convenient to do so.


Analyze
-------

The key thing that analyze does is run through the captured data from
collect, and extract timing information. It does this by searching the
contents of packets for a user-defined trigger, then looking for a
response packet (with an optional search parameter). In the case of
simple TCP flows, it is usually simplest to take the next reply packet
in the flow. Once these two packets are selected, the time difference
is computed and the measurement is assigned into a sampling category.

Analyze contains tools to help you understand your data, and optimize
your data collection techniques.

Generally speaking, we don't want to run analyze at the same time that
we're generating data.

Analyze results can feed back into generator [somehow].