## InCites Retrieve

This code supports batch retrieval of metrics from the [InCites Benchmarking and Analytics](https://clarivate.com/products/incites/) [API](https://developer.clarivate.com/apis/incites).

Please see the Product/Service terms on the Clarivate [Terms of business](https://clarivate.com/legal/terms-of-business/) page for details on how the data retrieved using this service can be used, including which fields may be shown on third party public-facing pages.
For more information about web services for the Web of Science, please review this [data integration](https://clarivate.com/products/data-integration/) website.

# Getting started

### Requirements
* Python 3.5+ (Python 2.7+ may work, but success not guaranteed)
* Access to the [InCites API](https://developer.clarivate.com/apis/incites)

### Install

* Download or clone this repository by clicking on the "Clone or download" button in the top right corner
* Set an environment variable with your API Key.
 * INCITES_KEY

#### Setting environment variables

On a Mac or Linux system:

~~~
$ export INCITES_KEY="mykey"
~~~

On Windows, open a command window:

~~~
set INCITES_KEY="mykey"
~~~

#### Running a script

Run the script with the incoming csv data as the first parameter. The output will be printed as CSV to the console. It can be redirected to a file for saving. For example:

~~~
$ python batch_lookup_v2.py myfile.csv > output.csv
~~~

#### Available files
batch_lookup_v2.py: Calls version 2 of the InCites API, which provides additional open access and subject category data 
batch_lookup_v1.py: Calls version 1 of the InCites API, provided here only for posterity 

#### ESCI
By default, results do not include the Emerging Sources Citation Index. To include ESCI, edit the setting in Python.
~~~
ESCI = False  # Set to True to include ESCI in results
~~~

#### Disclaimer

These scripts are provided to allow InCites users to perform common operations with the AMR web service. The scripts and uses cases may change over time. No direct support is provided. 

Please contact your Clarivate account manager or [technical support](https://support.clarivate.com/s/) with questions regarding API access.

## Use Cases

### Retrieve InCites metrics for a set of documents

With a CSV file containing a `ut` column, lookup each item via InCites and save retrieved metrics to a file.

#### incoming data
|ut|
|----|
|WOS:000259986300005
|WOS:000235983900007
|WOS:000253436400011

#### matched data

ISI_LOC|NCI|IMPACT_FACTOR|AVG_EXPECTED_RATE|...
---|---|---|---|---|
000259986300005|6.59|8.166|21.2582|...
000235983900007|.87|4.155|34.3393|...
000253436400011|2.42|5.153|24.3601|...

Partial output. See full output in the [API documentation](https://developer.clarivate.com/apis/incites).


 

