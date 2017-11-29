#------------------------------------------------------------------------------
#Imports modules to be used within the script
#------------------------------------------------------------------------------
import json
import requests

#Allows the API Call to Authenticate with username/password
from requests.auth import HTTPBasicAuth

#Allows you to ignore the Security warning associated with unsecured certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Build Variables to be used within the VMAX API Call
#------------------------------------------------------------------------------
username="<User ID>"
password="<Password>"
vmax_ip="<VMAX IP>"
vmax_sid="<VMAX SID>"
number = 0

#Calls for all Volumes which are true tdevs (customer facing)
#NOTE: Use the specific Univmax version API Calls that you have installed on the VMAX
#(Ex: I use '83' API Calls because we are running UniVMAX 8.3)
url = 'https://' + vmax_ip + ':8443/univmax/restapi/83/sloprovisioning/symmetrix/' + vmax_sid + '/volume?tdev=true'

#Initialize WebHook URL to Post to Slack (The Key is given when setting up the WebHook Integration in Slack)
webhook_url = 'https://hooks.slack.com/services/XXXXXXXXX/YYYYYYYYY/ZZZZZZZZZZZZZZZZZZZZZZZZ'

headers = {'content-type': 'application/json', 'accept': 'application/json'}
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

#Send Complete Message to Slack
slack_message = "----------------------------------------------------- \n " \
                "Getting Started! \n" \
                "-----------------------------------------------------"

#Loop thru each of the LUNs and pull the relevant data for reporting purposes
for i in lun_list.get('result'):
    lun_id=i.get('volumeId')
    print ('-----------------------------------------------------------------')
    print ('Volume ID: ' + lun_id)
    print ('-----------------------------------------------------------------')

    # Grab each LUNs relevant data for reporting purposes
    url = 'https://' + vmax_ip + ':8443/univmax/restapi/83/sloprovisioning/symmetrix/' + vmax_sid + '/volume/' + lun_id
    response = session.request('GET', url=url, timeout=60)
    data = response.json()
    lun_name = data['volume'][0]['volume_identifier']
    lun_cap = data['volume'][0]['cap_gb']
    lun_used_pct = data['volume'][0]['allocated_percent']
    lun_used_cap = (lun_cap * lun_used_pct) / 100
    print('LUN Name: ' + lun_name)
    print('LUN Capacity: ' + str(lun_cap))
    print('LUN % Used: ' + str(lun_used_pct))
    print('LUN Used Capacity: ' + str(lun_used_cap))
    print('-----------------------------------------------------------------')
    print('')

    #Only report on LUNs that are over 50% Full
    if lun_used_pct >= 50:
        #Setup WebHook Variables to make the call and post results to Slack Channel
        slack_message = slack_message + "\n" \
                        "######################\n" \
                        "LUN Name: " + lun_name + "\n" \
                        "LUN Capacity: " + str(lun_cap) + "\n" \
                        "LUN % Used: " + str(lun_used_pct) + "\n" \
                        "LUN Used Capacity: " + str(lun_used_cap) + "\n" \
                        "######################\n"

    #Keep Track of Number of LUNs processed
    number = number + 1
#------------------------------------------------------------------------------

#Add Complete Message to Slack
slack_message = slack_message + "\nAll is done and Looks good! :thumbsup: \n " \
                                "-----------------------------------------------------"

#------------------------------------------------------------------------------
#Make the Call to Post results to the SlackOps Slack Channel
#------------------------------------------------------------------------------
slack_data = {'text': slack_message}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)

if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
#------------------------------------------------------------------------------