# macio
macio provides MAC address and vendor detail information retrieved from macaddress.io API


## Instalation/Requirements
 

It runs on python 3 and requires the `requests` library. 

```
pip install requests
```



## SYNOPSIS 

```
./macio.py -h
Usage: macio.py [OPTIONS]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Input Options:
    -m MAC, --mac-address=MAC
                        mac address to lookup
    -k APIKEY, --api-key=APIKEY
                        API key to macaddress.io
    -o OUTPUT, --output=OUTPUT
                        optional raw output [json|xml|csv|vendor]
    -q, --quiet         only raw output, depend on above outputs
```

## Usage

API key can be set on shell environment or pass as an argument using the `-k` option. To get your API key register first at https://macaddress.io/api. Registration and usage up to 1000 req/day is free. 


Get MAC address details using API KEY from environment variable

```
MIO_APIKEY=at_y0uRapiK3yy0uRapiK3yy0uRapiK3y ./macio.py -m 44:38:39:ff:ef:57 
Looking for MAC address 44:38:39:ff:ef:57 ..
Vendor details:
--------------------------------------------------------------------------------
Company Name         : Cumulus Networks, Inc
Company Address      : 650 Castro Street, suite 120-245 Mountain View CA 94041 US
Country Code         : US
OUI                  : 443839

Mac address details:
--------------------------------------------------------------------------------
Administration Type  : UAA
Application          : None
Transmission Type    : unicast
Virtual Machine      : Not detected
Wireshark Notes      : No details
```


Get the XML output for further processing, skip additional prints:

```
./macio.py -m 44:38:39:ff:ef:57 -k at_y0uRapiK3yy0uRapiK3yy0uRapiK3y -o xml -q
<Response><vendorDetails><oui>443839</oui><isPrivate>false</isPrivate><companyName>Cumulus Networks, Inc</companyName><companyAddress>650 Castro Street, suite 120-245 Mountain View CA 94041 US</companyAddress><countryCode>US</countryCode></vendorDetails><blockDetails><blockFound>true</blockFound><borderLeft>443839000000</borderLeft><borderRight>443839FFFFFF</borderRight><blockSize>16777216</blockSize><assignmentBlockSize>MA-L</assignmentBlockSize><dateCreated>2012-04-08</dateCreated><dateUpdated>2015-09-27</dateUpdated></blockDetails><macAddressDetails><searchTerm>44:38:39:ff:ef:57</searchTerm><isValid>true</isValid><virtualMachine>Not detected</virtualMachine><applications><application>Multi-Chassis Link Aggregation (Cumulus Linux)</application></applications><transmissionType>unicast</transmissionType><administrationType>UAA</administrationType><wiresharkNotes>No details</wiresharkNotes><comment></comment></macAddressDetails></Response>
```


Get the JSON output for further processing, skip additional prints:

```
./macio.py -m 44:38:39:ff:ef:57 -k at_y0uRapiK3yy0uRapiK3yy0uRapiK3y -o json -q | json_pp
{
   "blockDetails" : {
      "dateCreated" : "2012-04-08",
      "borderLeft" : "443839000000",
      "blockSize" : 16777216,
      "assignmentBlockSize" : "MA-L",
      "blockFound" : true,
      "dateUpdated" : "2015-09-27",
      "borderRight" : "443839FFFFFF"
   },
   "macAddressDetails" : {
      "virtualMachine" : "Not detected",
      "applications" : [
         "Multi-Chassis Link Aggregation (Cumulus Linux)"
      ],
      "searchTerm" : "44:38:39:ff:ef:57",
      "wiresharkNotes" : "No details",
      "comment" : "",
      "transmissionType" : "unicast",
      "administrationType" : "UAA",
      "isValid" : true
   },
   "vendorDetails" : {
      "companyAddress" : "650 Castro Street, suite 120-245 Mountain View CA 94041 US",
      "countryCode" : "US",
      "oui" : "443839",
      "isPrivate" : false,
      "companyName" : "Cumulus Networks, Inc"
   }
}
```


Get just the vendor name: 

```
./macio.py -m 44:38:39:ff:ef:57 -k at_y0uRapiK3yy0uRapiK3yy0uRapiK3y -o vendor
Looking for MAC address 44:38:39:ff:ef:57 ..
Raw output in requested format: vendor

Cumulus Networks, Inc
```


## Docker 


In case you would like to test it in docker, the Dockerfile is found under the docker directory. 


```
cd docker && docker build --tag macio:v1.0 .
```

To make your life easier add below two line to your ~/.bashrc. Replace <YOUR_API_KEY> with the key you get from the macadress.io site.

```
export MIO_APIKEY=<YOUR_API_KEY>
alias macio="docker run --rm -e MIO_APIKEY --name macio macio:v1.0"
```

Remeber to reload the rc file

```
source ~/.bashrc
```

You can test it: 

```
type macio
macio is aliased to `docker run --rm -e MIO_APIKEY --name macio macio:v1.0'


macio -h
Usage: macio.py [OPTIONS]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Input Options:
    -m MAC, --mac-address=MAC
                        mac address to lookup
    -k APIKEY, --api-key=APIKEY
                        API key to macaddress.io
    -o OUTPUT, --output=OUTPUT
                        optional raw output [json|xml|csv|vendor]
    -q, --quiet         only raw output, depend on above outputs
```



That's all you need!

### Note 


BTW this tool was done as an excercise. The macaddress.io provides its own client library for [python](https://pypi.org/project/maclookup)
