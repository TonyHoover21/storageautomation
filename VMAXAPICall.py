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
username="username"
password="password"
url = 'https://<array_ip>:8443/univmax/restapi/sloprovisioning/symmetrix/<symmetrix_id>/volume/<volume_id>'
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

#Make a GET request to the VMAX for a list of Alerts
response = session.request('GET', url=url, timeout=60)

#Print the JSON formatted response of the API Call
print(response.json())