# api script for companies house company number search

## This script performs a registered address query using a company number.
## To change the type of query, change DomainURL, address array labels
## and the JSON Keys handle by temp address

import requests
import numpy as np
from numpy import genfromtxt
from pathlib import Path

# APIkey = ""
# Key removed from Git version
DomainURL = 'https://api.companieshouse.gov.uk/company/'
QueryTypeURL = '/registered-office-address' # to be changed if you want to make a different type of call
SearchQueries = Path("T:/BEN/Audit/search.csv") # import file path
SearchResults = Path("T:/BEN/Audit/Search_Results.csv") # export file path
address = np.array(['Companies House Number','address_line_1','address_line_2','locality','postal_code']) # create results array
z = 0 # Rate limit counter 
data = genfromtxt(SearchQueries, delimiter=',',dtype=str) # import csv as array

#Performs GET request on company number
#Auth is BASIC authentication, user name is APIkey, password is blank ('')
#
# Iterate through imported list of company numbers
for x in np.nditer(data):
    r = requests.get(DomainURL+str(x)+QueryTypeURL, auth = (APIkey,''))
    if r.status_code != 200: # This means something went wrong.
        print('The following API error code was receieved:')
        print(r.status_code) # Prints error code
        pass
    extract_dict = r.json() # load JSON into Py Dictionary
    TempAddress = str(x),extract_dict.get('address_line_1',''),extract_dict.get('address_line_2',''),extract_dict.get('locality',''),extract_dict.get('postal_code','') # extract keys into temp address object
    address = np.vstack([address,TempAddress])	# append latest api call to current array (vertical append, makes new row)
#    z = z+1 # adding to rate limit counter after each loop
#    if z == 590: # API rate limit is 600, ending loop early to avoid losing API account
#        print ('WARNING Rate limit reached. Please wait 5 minutes'.) #Last record returned: '+x+'. Number of rows processed = '+z)  commented out, fancyness not necessary and giving syntax error
#        np.savetxt(SearchResults,address,fmt='%s',delimiter=",") # saves and exits
#        break

np.savetxt(SearchResults,address,fmt='%s',delimiter=",") # save file to csv

print('Congratulations! Companies House search complete, number of records returned: '+str(z))
# print should now work
