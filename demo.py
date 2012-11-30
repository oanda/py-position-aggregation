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

instruments = ["EUR/USD","USD/CAD"]
directions = ["long","short"]

def pp_json(val):
    ''' pretty print json string '''
    return json.dumps(val, sort_keys=True,indent=4,separators=(',', ': '))


def demo(loglevel=1):
    '''
    loglevel - 1, 2, or 3 (as explained in module header)
    
    - query user fralcody for his accounts (there should be 3)
    - open between 3 and 5 trades on each account  
    - print the positions list for each account
    - print the aggregate positions list across all accounts 
    '''
    accounts = sandbox_request("GET","/v1/accounts?username=fralcody")
    for elt in accounts:
        acctid = elt["id"]
        for i in range(random.randint(3,5)):
            body = urllib.urlencode({'instrument':instruments[random.randint(0,1)],
                    'units':random.randint(100,1000), 'direction':directions[random.randint(0,1)]})
            trade = sandbox_request("POST","/accounts/"+str(acctid)+"/trades",body)
            if loglevel == 3: print "Created trade on account id "+str(acctid)
            if loglevel == 3: print '-----------------------------------------' 
            if loglevel == 3: print pp_json(trade)
            if loglevel == 3: print '-----------------------------------------' 
        positions = sandbox_request("GET", "/v1/accounts/"+str(acctid)+"/positions")
        if loglevel >= 2: print "Positions on account id "+str(acctid)
        if loglevel >= 2: print '-----------------------------------------' 
        if loglevel >= 2: print pp_json(positions)
        if loglevel >= 2: print '-----------------------------------------' 
    print
    print
    print 'Aggregate positions across all accounts owned by fralcody:'
    print '==========================================================' 
    print pp_json(aggregate_positions('fralcody'))
        
    

if __name__ == '__main__':
    
    argc = len(sys.argv)
    loglevel = 1
    if argc > 1: 
        loglevel = int(sys.argv[1])
    demo(loglevel)


