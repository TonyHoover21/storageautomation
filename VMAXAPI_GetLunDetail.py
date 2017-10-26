#------------------------------------------------------------------------------
#Imports modules to be used within the script
#------------------------------------------------------------------------------
#Allows API Calls to be made to the VMAX
import requests

#Allows the API Call to Authenticate with username/password
from requests.auth import HTTPBasicAuth

#Allows you to ignore the Security warning associated with unsecured certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Build Variables to be used within the API Call
#------------------------------------------------------------------------------
username="<User ID>"
password="<Password>"

#Calls for all Volumes which are true tdevs (customer facing)
#NOTE: Use the specific Univmax version API Calls that you have installed on the VMAX
#(Ex: I use '83' API Calls because we are running UniVMAX 8.3)
url = 'https://<VMAX IP>:8443/univmax/restapi/83/sloprovisioning/symmetrix/<VMAX SID>/volume?tdev=true'

headers = {'content-type': 'application/json',
            'accept': 'application/json'}
verifySSL=False
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Build the Session to make the API call to the VMAX
#------------------------------------------------------------------------------
session = requests.session()
session.headers = headers
session.auth = HTTPBasicAuth(username, password)
session.verify = verifySSL
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Make a GET request to the VMAX for a list of LUNs/TDEVs
#------------------------------------------------------------------------------
lun_id_get = session.request('GET', url=url, timeout=60).json()
lun_list = lun_id_get.get('resultList')

#Loop thru each of the LUNs and pull the relevant data for reporting purposes
for i in lun_list.get('result'):
    lun_id=i.get('volumeId')
    print ('-----------------------------------------------------------------')
    print ('Volume ID: ' + lun_id)
    print ('-----------------------------------------------------------------')

    # Grab each LUNs relevant data for reporting purposes
    url = 'https://<VMAX IP>:8443/univmax/restapi/83/sloprovisioning/symmetrix/<VMAX SID>/volume/' + lun_id
    response = session.request('GET', url=url, timeout=60)
    data = response.json()
    lun_name = data['volume'][0]['volume_identifier']
    lun_cap = data['volume'][0]['cap_gb']
    lun_used = data['volume'][0]['allocated_percent']
    print('LUN Name: ' + lun_name)
    print('LUN Capacity: ' + str(lun_cap))
    print('LUN Used: ' + str(lun_used))
    print('-----------------------------------------------------------------')
    print('')
#------------------------------------------------------------------------------