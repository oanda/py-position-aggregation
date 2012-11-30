'''
Provides functionality for making requests to api-sandbox.oanda.com, and
aggregating positions held by a user across multiple accounts. See demo.py
for executing a demonstration of this code.
'''

import httplib, json

def sandbox_request(method, uri, body=None):
    ''' 
    Make a request to the OANDA api on api-sandbox.

    method - GET, POST, POST, or DELETE
    uri - request uri 
    body - optional body for POST requests
    ''' 
    conn = httplib.HTTPConnection("api-sandbox.oanda.com")
    if body is not None: conn.request(method,uri,body)
    else: conn.request(method,uri)
    r1 = conn.getresponse()
    data = r1.read()
    if r1.status == 200:
        return json.loads(data)
    else:
        raise httplib.HTTPException("Error in HTTP request (status: "+str(r1.status)+"):\n"+str(data))

def combine_positions_helper(pos1, pos2, multiplier):
    '''
    Return a new position that is the aggregation of pos1 and pos2. 

    multiplier - +1 if the positions are in the same direction, -1 otherwise. 
    
    (if multiplier is -1, pos1 must be the long position)
    ''' 

    # calculate the average price of the combined position
    # (this is the weighted average of the average prices of the two positions)
    total_price = pos1["units"] * pos1["avgPrice"] + pos2["units"] * pos2["avgPrice"]
    total_units = pos1["units"] + pos2["units"]
    avg_price = total_price / total_units
    
    # calculate the net number of units in the combined position
    # and the determine the direction of the combined position
    net_units = pos1["units"] + multiplier * pos2["units"]
    new_direction = pos1["direction"]
    if net_units < 0:
        new_direction = "short"    # since pos1 is assumed to be long

    # fill in the data for the new position
    new_pos = {}
    new_pos["direction"] = new_direction
    new_pos["units"] = abs(net_units)
    new_pos["avgPrice"] = avg_price
    new_pos["instrument"] = pos1["instrument"]
    return new_pos

def combine_positions(pos1, pos2):
    '''
    Return a new position that is the aggregation of pos1 and pos2. 
    ''' 
    if pos1["direction"] == pos2["direction"]:
        return combine_positions_helper(pos1, pos2, 1)
    elif pos1["direction"] == "long":
        return combine_positions_helper(pos1, pos2, -1)
    else:
        return combine_positions_helper(pos2, pos1, -1)


def aggregate_positions(username):
    ''' 
    Return the aggregate of all positions a user holds (across all accounts). 
    
    username - user whose positions are to be aggregated
    ''' 

    # retrieve the accounts owned by the given user
    accounts = sandbox_request("GET","/v1/accounts?username="+username)

    tmp_positions = {}          # for temporary storage of the aggregate positions

    # aggregate the positions across each account
    for elt in accounts:
        acctid = elt["id"]
        positions = sandbox_request("GET", "/v1/accounts/"+str(acctid)+"/positions")
        for pos in positions["positions"]:
            instrument = pos["instrument"]
            if tmp_positions.has_key(instrument):
                tmp_positions[instrument] = combine_positions(tmp_positions[instrument], pos)
            else:
                tmp_positions[instrument] = pos

    aggregated_pos = {}
    aggregated_pos["positions"] = []
    for instrument in tmp_positions:
        aggregated_pos["positions"].append(tmp_positions[instrument])

    return aggregated_pos
