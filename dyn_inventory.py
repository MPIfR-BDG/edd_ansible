#!/usr/bin/python
from __future__ import print_function
from __future__ import division 

import argparse
import json
import logging
import subprocess
#import ansible.parsing.dataloader
#import ansible.inventory.manager
import multiprocessing

if __name__ == "__main__":
    #######################################################################
    parser = argparse.ArgumentParser(description='Dynamic inventory for EDD.')
    mg = parser.add_mutually_exclusive_group()
    mg.add_argument('--list', action='store_true')
    mg.add_argument('--host')
    parser.add_argument("-v",'--verbose', action='store_true')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug("Commandline options: " + str(args))

    ########################################################################
    #all_hosts = ['edd00', 'edd01']
    #Ansible directory reader gets confused as global context is used??
    #loader = ansible.parsing.dataloader.DataLoader()
    #inventory = ansible.inventory.manager.InventoryManager(loader=loader, sources='all_nodes.yml')
    #all_hosts = [host.get_name() for host in inventory.list_hosts()]
    inventory = json.loads(subprocess.check_output('ansible-inventory -i site.yml --list'.split()))
    all_hosts = inventory['gpu_server']['children']

    logging.debug(" {} hosts known: {}".format(len(all_hosts), " ,".join(all_hosts)))

    ########################################################################
    # Check available hosts
    def ping_host(hostname):
        process = subprocess.Popen(['ping', '-c1', '-W1',  hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        logging.debug(output)
        return process.returncode == 0
    pool = multiprocessing.Pool(processes=10)
    available_hosts = [host for host, pr in zip(all_hosts, pool.map(ping_host, all_hosts)) if pr]
    logging.debug(" {} hosts available: {}".format(len(available_hosts), " ,".join(available_hosts)))

    ########################################################################
    # create meta groups
    output = {}
    for i,h in enumerate(available_hosts):
        output['gpunode_{:03}'.format(i)] = {"hosts" : [h]}

    if args.list:
        print(output)
    elif args.host:
        if args.host not in output.keys():
            print("Unknown host {}. Possible hosts are: {}".format(args.host, ", ".join(output.keys())) )
            exit(-1)
        print(output[args.host])
