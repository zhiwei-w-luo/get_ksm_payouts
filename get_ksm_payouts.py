#!/usr/bin/python3

# PolkaDot Hackathon Challenge
# https://gitcoin.co/issue/Polkadot-Network/hello-world-by-polkadot/5/100023931
# Author: zhiwei-w-luo

# Connects to local sidecar and queries sidecar api to find the pending payouts

# Usage:
#   get_payouts.py [-a <address>] [-d <depth>] [-e <era>]
#       <address> : stake account address, default uses last block's
#       <depth> : the number of eras to query for payouts of (default is 5)
#       <era> : `era`: The era to query at. 
# Note for the era: 
# Must specify era and depth such that era - (depth - 1) is less than or equal to
# current_era - history_depth.


import sys
import getopt
import requests
import json

def get_arguments(argv):
    address = ""
    depth = ""
    era = ""
    try:
        opts, args = getopt.getopt(argv,"ha:d:e:",["address=","depth=","era="])
    except getopt.GetoptError:
        print ('get_payouts.py -a <address> -d <depth> -e <era>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('payout_reader.py -a <address> -d <depth> -e <era>')
            sys.exit()
        elif opt in ("-a", "--address"):
            address = arg
        elif opt in ("-d", "--depth"):
            depth = arg
        elif opt in ("-e", "--era"):
            era = arg
    return address, depth, era

def get_last_block_author():
        return requests.get('http://127.0.0.1:8080/blocks/head').json()['authorId']

def get_payout_info(address, depth, era):
    if address == "":
        address = get_last_block_author()
    print("Requesting Pending Payouts of Address:" + address)
    print('\n')
    side_url = f'http://127.0.0.1:8080/accounts/{address}/staking-payouts?depth={depth}' \
        '&unclaimedOnly=true'
    if era != "":
        side_url += f'&era={era}'
    return requests.get(side_url).json()

def total_pending_payouts(payout):
    sum_pending_payouts = 0
    for era in payout['erasPayouts']:
        # sometimes payouts array can be empty
        if era['payouts']:
            for validator in era['payouts']:
                # since we sent unclaimedOnly=True, "claimed" : false
                # so we add up all these values for pending payouts
                sum_pending_payouts += int(validator['nominatorStakingPayout'])
    return sum_pending_payouts 

def main(argv):
    address, depth, era = get_arguments(argv)
    payout_info = get_payout_info(address, depth, era)
    print(f'Returned Payouts Info:{json.dumps(payout_info)}')
    print('\n')
    pending_payouts = total_pending_payouts(payout_info)
    convert_ksm = pending_payouts/(10**12)
    print(f'{pending_payouts} Planc ({convert_ksm} KSM) pending payouts for account {address}')

if (__name__ == '__main__'):
    main(sys.argv[1:])

