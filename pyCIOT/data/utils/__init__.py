import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable InsecureRequestWarning output to the terminal
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
