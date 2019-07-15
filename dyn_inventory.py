#!/usr/bin/python
import argparse
import json
import suitable
import logging

output = {}

parser = argparse.ArgumentParser(description='Dynamic inventory for EDD.')
mg = parser.add_mutually_exclusive_group()
mg.add_argument('--list', action='store_true')
mg.add_argument('--host')
parser.add_argument("-v",'--verbose', action='store_true')

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

logging.debug("Commandline options: " + str(args))

# list of all *potential* hosts , colelcted from foreman, or whatever
all_hosts = ['edd00', 'edd01', 'edd03', 'srx-dev']

api = suitable.Api(all_hosts, ignore_unreachable=True)
r = api.ping()
available_hosts = r['contacted'].keys()

for i,h in enumerate(available_hosts):
    output['gpunode_{:03}'.format(i)] = {"hosts" : [h]}

logging.debug(" {} hosts known: {}".format(len(all_hosts), " ,".join(available_hosts)))
logging.debug(" {} hosts available: {}".format(len(available_hosts), " ,".join(available_hosts)))
if args.list: 
    print(output)
elif args.host:
    if args.host not in output.keys():
        print("Unknown host {}. Possible hosts are: {}".format(args.host, ", ".join(output.keys())) )
        exit(-1)
    print(output[args.host])





