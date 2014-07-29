''' 
Demonstrates aggregating positions across multiple accounts. 

The demo method will create several trades for user fralcody in each
of his accounts and then output the aggregate positions list. 

To execute, run the command:

python demo.py [loglevel]

where loglevel is an optional argument. There are three valid loglevels:

1 - default log level, will only output aggregate positions list
2 - additionally output positions for each account 
3 - additionally output trades as they are created
'''

from aggregate_positions import aggregate_positions, sandbox_request
import sys
import json
import urllib
import random

instruments = ["EUR_USD","USD_CAD"]
directions = ["buy","sell"]

def pp_json(val):
    ''' pretty print json string '''
    return json.dumps(val, sort_keys=True,indent=4,separators=(',', ': '))


def demo(loglevel=1):
    '''
    loglevel - 1, 2, or 3 (as explained in module header)
    
    - create 3 accounts
    - open between 3 and 5 trades on each account  
    - print the positions list for each account
    - print the aggregate positions list across all accounts 
    '''
    account1 = (sandbox_request("POST", "/v1/accounts"))['accountId']
    account2 = (sandbox_request("POST", "/v1/accounts"))['accountId']
    account3 = (sandbox_request("POST", "/v1/accounts"))['accountId']
    accounts = [ account1, account2, account3 ]
    for accId in accounts:
        for i in range(random.randint(3,5)):
            body = urllib.urlencode({'instrument':instruments[random.randint(0,1)],
                'units':random.randint(100,1000), 'side':directions[random.randint(0,1)], 'type':'market'})
            trade = sandbox_request("POST","/v1/accounts/"+str(accId)+"/orders",body)
            if loglevel == 3: print "Created trade on account id "+str(accId)
            if loglevel == 3: print '-----------------------------------------' 
            if loglevel == 3: print pp_json(trade)
            if loglevel == 3: print '-----------------------------------------' 
        positions = sandbox_request("GET", "/v1/accounts/"+str(accId)+"/positions")
        if loglevel >= 2: print "Positions on account id "+str(accId)
        if loglevel >= 2: print '-----------------------------------------' 
        if loglevel >= 2: print pp_json(positions)
        if loglevel >= 2: print '-----------------------------------------' 
    print
    print
    print 'Aggregate positions across all accounts:'
    print '==========================================================' 
    print pp_json(aggregate_positions(accounts))
        
    

if __name__ == '__main__':
    
    argc = len(sys.argv)
    loglevel = 1
    if argc > 1: 
        loglevel = int(sys.argv[1])
    demo(loglevel)
