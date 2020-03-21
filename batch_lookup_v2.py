"""
Look up batches of UTs in InCites API v2.

Run as:

$ python batch_lookup_v2.py sample_file.csv > outputfile.csv

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
ESCI = False  # Set to True to include ESCI in results
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
    if ESCI:
        params += '&esci=y'
    url = "{}?{}&ver=2".format(URL, params)
    q = Request(url)
    q.add_header('X-ApiKey', INCITES_KEY)
    rsp = urlopen(q)
    raw = json.loads(rsp.read().decode('utf-8'))
    data = [item for item in raw['api'][0]['rval']]
    return data


def main():

    # Define the fields for the output file. Journal category fields are
    # added as needed. Typically a journal can have up to 6 categories, but
    # occasionally there are more.
    fields = ["ACCESSION_NUMBER",
              "DOCUMENT_TYPE",
              "TIMES_CITED",
              "JOURNAL_EXPECTED_CITATIONS",
              "JNCI",
              "IMPACT_FACTOR",
              "HARMEAN_CAT_EXP_CITATION",
              "AVG_CNCI",
              "ESI_HIGHLY_CITED_PAPER",
              "ESI_HOT_PAPER",
              "IS_INTERNATIONAL_COLLAB",
              "IS_INSTITUTION_COLLAB",
              "IS_INDUSTRY_COLLAB",
              "OA_FLAG",
              "OA_TYPE"]

    found = []
    to_check = []
    with open(sys.argv[1]) as infile:
        for row in csv.DictReader(infile):
            d = {}
            for k, v in row.items():
                if k.lower().strip() == "ut":
                    to_check.append(v.strip().replace("WOS:", ""))

    all_found = []

    for idx, batch in enumerate(grouper(to_check, BATCH_SIZE)):
        eprint("Processing batch", idx + 1)
        try:
            found = get(batch)
        except Exception as e:
            found = []
            eprint(e)

        for grp in found:
            row_data = {}
            try:
                for field in grp:
                    if field in fields:
                        row_data[field] = grp[field]
                    elif field == "OPEN_ACCESS":
                        row_data["OA_FLAG"] = grp.get(
                                              'OPEN_ACCESS', {}).get('OA_FLAG')
                        if row_data["OA_FLAG"] == "1":
                            statuses = []
                            for type in grp['OPEN_ACCESS']['STATUS']:
                                statuses.append(type['TYPE'])
                            row_data["OA_TYPE"] = ', '.join(statuses)
                    elif field == "PERCENTILE":
                        for idx, cat in enumerate(grp['PERCENTILE']):
                            i = idx+1
                            if "CAT_{}".format(i) not in fields:
                                fields += ["CAT_{}".format(i),
                                           "CAT_{}_CODE".format(i),
                                           "CAT_{}_PERCENTILE".format(i),
                                           "CAT_{}_EXPECTED_CITATIONS".format(i),
                                           "CAT_{}_IS_BEST".format(i),
                                           "CAT_{}_CNCI".format(i)]

                            row_data["CAT_{}".format(i)] = cat.get('SUBJECT')
                            row_data["CAT_{}_CODE".format(i)] = cat.get('CODE')
                            row_data["CAT_{}_PERCENTILE".format(i)] = (
                                                   cat.get('CAT_PERC'))
                            row_data["CAT_{}_EXPECTED_CITATIONS".format(i)] = (
                                                   cat.get('CAT_EXP_CITATION'))
                            row_data["CAT_{}_IS_BEST".format(i)] = (
                                                   cat.get('IS_BEST'))
                            row_data["CAT_{}_CNCI".format(i)] = cat.get('CNCI')

                all_found.append(row_data)
            except Exception as e:
                eprint(e)
        time.sleep(.5)

    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for row in all_found:
        writer.writerow(row)


if __name__ == "__main__":
    main()
