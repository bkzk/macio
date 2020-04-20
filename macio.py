#!/usr/bin/env python3

import os,sys
import re
import requests
from requests.exceptions import HTTPError
requests.packages.urllib3.disable_warnings()

from optparse import OptionParser, OptionGroup

__author__ = "Bartosz Kozak <bakozak@cisco.com>"
__version__ = "1.0"
__prog__ = os.path.basename(sys.argv[0])

# from pprint import pprint as pp

class MACAddressIOAPI:
    def __init__(self, **kwargs):
        self.apikey = kwargs.get('apikey')
        self.search = kwargs.get('search')
        self.output = kwargs.get('output','json')
    def api_query(self):
        #https://api.macaddress.io/v1?apiKey={{ apiKey }}&output=json&search=44:38:39:ff:ef:57 
        url=f"https://api.macaddress.io/v1?search={self.search}"
        if self.output:
            url+=f"&output={self.output}"
        # print (f"> Querying {url} ..")

        if self.api_query:
            headers = {
               "X-Authentication-Token": self.apikey
            }
        else:
            print("Missing apikey")
            return
        try:
            r = requests.get(url=url, headers=headers, verify=False)
            # pp(r.json())

            if r.status_code == 200:
                if self.output == 'json':
                    return r.json()
                else:
                    return r.text
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

def main():

    parser = OptionParser(usage="usage: %prog [OPTIONS]",
                          version=__version__)

    # Input group options
    in_opt = OptionGroup( parser, 'Input Options' )


    # Connections TODO 
    in_opt.add_option( "-m","--mac-address", dest="mac", default=False, action='store',
                              help='mac address to lookup')

    in_opt.add_option( "-k","--api-key", dest="apikey", default=False, action='store',
                              help='API key to macaddress.io ')
    
    in_opt.add_option( "-o","--output", dest="output", default=False, action='store',
                              help='optional raw output [json|xml|csv|vendor]')

    in_opt.add_option( "-q","--quiet", dest="quiet", default=False, action='store_true',
                              help='only raw output, depend on above outputs') 
    # ©eneral option
    # parser.add_option("-v","--verbose", dest='verb', default=False, action='store_true',
    #                    help='show verbose messages')
    # parser.add_option("-D","--debug", dest='debug', default=False, action='store_true',
    #                    help='show debug messages and outputs')

    parser.add_option_group( in_opt )


    try:
        
        
        # Run the argument parser
        (opts,args) = parser.parse_args()
    
        margs = {}

        margs.setdefault('apikey', os.environ.get('MIO_APIKEY'))

        if len(sys.argv[1:]) < 1:
            parser.error("incorrect number of arguments")
            sys.exit(0)

        if opts.apikey:
            if margs.get('apikey'):
                print("Warning: API key found in both user env and command arguments")
                print(f"Choosing API key from CLI args: {opts.apikey}")
            margs['apikey'] = opts.apikey
        elif not margs.get('apikey'):
            print("API key is missing! To get one register at https://macaddress.io/api")
            print(f"Try {sys.argv[0]} -k [APIKEY] [OPTIONS]")
            sys.exit(0)

        if opts.output:
            if not opts.output in ['json', 'xml', 'csv', 'vendor']:
                print("Unknown output format. Supported formats are: json, xml, cs, vendor.")
                sys.exit(0)
            else:
                margs.setdefault('output',opts.output)

        if opts.mac:
            if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", opts.mac.lower()):
                parser.error(f"Provided MAC address doesn't seem to be correct: '{opts.mac}'' ")
            margs.setdefault('search',opts.mac)

            if not opts.quiet:
                print(f"Looking for MAC address {opts.mac} ..")

            mio = MACAddressIOAPI(**margs)
            rdata = mio.api_query()

            if isinstance(rdata,dict) and not opts.quiet:
                if rdata.get('vendorDetails'):
                    print("Vendor details:")
                    print("-"*80)
                    print(f"Company Name         : {rdata['vendorDetails'].get('companyName')}\n"
                          f"Company Address      : {rdata['vendorDetails'].get('companyAddress')}\n" 
                          f"Country Code         : {rdata['vendorDetails'].get('countryCode')}\n" 
                          f"OUI                  : {rdata['vendorDetails'].get('oui')}\n")
                if rdata.get('macAddressDetails'):
                    print("Mac address details:")
                    print("-"*80)
                    print(f"Administration Type  : {rdata['macAddressDetails'].get('administrationType')}\n"
                          f"Application          : {rdata['macAddressDetails'].get('application')}\n"
                          f"Transmission Type    : {rdata['macAddressDetails'].get('transmissionType')}\n"
                          f"Virtual Machine      : {rdata['macAddressDetails'].get('virtualMachine')}\n"
                          f"Wireshark Notes      : {rdata['macAddressDetails'].get('wiresharkNotes')}")


            else: # opts.output in ['json', 'xml', 'csv', 'vendor']:
                if not opts.quiet: 
                    print(f"Raw output in requested format: {opts.output}\n")
                if opts.output == 'json':
                    from json import dumps
                    print(dumps(rdata))
                else:
                    print(rdata) 



    except Exception as e:
        print(str(e))


if __name__  == '__main__':
    main()