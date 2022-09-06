import requests
import shodan
import optparse
from termcolor import colored

print(colored('''
 ____  _               _             ____                      _     
/ ___|| |__   ___   __| | __ _ _ __ / ___|  ___  __ _ _ __ ___| |__  
\___ \| '_ \ / _ \ / _` |/ _` | '_ \\___ \ / _ \/ _` | '__/ __| '_ \ 
 ___) | | | | (_) | (_| | (_| | | | |___) |  __/ (_| | | | (__| | | |
|____/|_| |_|\___/ \__,_|\__,_|_| |_|____/ \___|\__,_|_|  \___|_| |_|

					by mohamed sayed @kanike99
''', 'green'))

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='target', help='target to get scan')
    parser.add_option('-a', '--api', dest='api', help='shodan api')
    (options, arguments) = parser.parse_args()
    
    
    if not options.target:
        parser.error('[-] Please Specify target, use --help to more info')
    elif not options.api:
        parser.error('[-] Please put your shodan api, use --help to more info')
        
    return options

def getIP():
    args = get_arguments() # calling the get_arguments() function which returns the values entered by the user
    myTarget = args.target # function().dest
    myApi = args.api

    myParams = {'hostnames': myTarget, 'key': myApi}
    r = requests.get('https://api.shodan.io/dns/resolve', params=myParams) # https://api.shodan.io/dns/resolve?hostnames=www.arrival.com&key=APIHERE

    hostIp = r.json()[myTarget] # r.json() will return a dictionary
    #like,  {'www.target.com': '105.18.25.245'}, in my case i just need the ip that's why [target] comes to access the value of the target key in the dictionary
    # print(hostIP)[myTarget]  --> 105.18.25.245
    return hostIp

shodan_api_key = get_arguments().api
shodanSearch = shodan.Shodan(shodan_api_key) # take an object of .Shodan class, and pass my api to it

hostIp = getIP()
result = shodanSearch.host(hostIp)


print(f"IP is: {result['ip_str']}")
print("Organization is: %s" %result.get('org', 'n\a'))
print("Operating System is: %s" %result.get('os', 'n\a'))

for item in result['data']:
    print("Port: %s" % item['port']) #print ports
    print("[+] Headers\n%s" % item['data']) # print the response headers (he calls it data)
