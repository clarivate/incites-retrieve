"""
Look up batches of UTs in InCites.

Run as:

$ python batch_lookup.py sample_file.csv outputfile.csv

"""
from __future__ import print_function

import csv
import json
import os
import sys
import time

# Python 2 or 3
PYV = sys.version_info
if PYV > (3, 0):
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    from itertools import zip_longest as zipl
else:
    from urllib2 import urlopen, Request
    from urllib import urlencode
    from itertools import izip_longest as zipl


URL = "https://api.clarivate.com/api/incites/DocumentLevelMetricsByUT/json"
INCITES_KEY = os.environ['INCITES_KEY']
# Number of UTs to send to InCites at once - 100 is limit set by API.
BATCH_SIZE = 100


def grouper(iterable, n, fillvalue=None):
    """
    Group iterable into n sized chunks.
    See: http://stackoverflow.com/a/312644/758157
    """
    args = [iter(iterable)] * n
    return zipl(*args, fillvalue=fillvalue)


def eprint(*args, **kwargs):
    """
    Utility for printing to stderr.
    http://stackoverflow.com/a/14981125/758157
    """
    print(*args, file=sys.stderr, **kwargs)


def get(batch):
    data = []
    params = urlencode({'UT': ",".join([b for b in batch if b is not None])})
    url = "{}?{}".format(URL, params)
    q = Request(url)
    q.add_header('X-ApiKey', INCITES_KEY)
    rsp = urlopen(q)
    raw = json.loads(rsp.read().decode('utf-8'))
    data = [item for item in raw['api'][0]['rval']]
    return data


def main():

    found = []
    to_check = []
    with open(sys.argv[1]) as infile:
        for row in csv.DictReader(infile):
            d = {}
            for k, v in row.items():
                if k.lower().strip() == "ut":
                    to_check.append(v.strip().replace("WOS:", ""))

    found = []

    writer = csv.writer(sys.stdout)
    first = True
    for idx, batch in enumerate(grouper(to_check, BATCH_SIZE)):
        eprint("Processing batch", idx)
        found = get(batch)
        for grp in found:
            if first is True:
                # write header
                writer.writerow(grp.keys())
                first = False
            writer.writerow(grp.values())
        time.sleep(.5)


if __name__ == "__main__":
    main()
