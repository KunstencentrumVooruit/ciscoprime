import requests

class LoginFailure(Exception):
    pass

class Client:
    def __init__(self, host, username, password):
        self.base = "https://%s/webacs/" % host
        self.username = username
        self.password = password
        self.s = requests.Session()
        self.s.verify=False
        self.login()

    def login(self):
        data = {
            'action': 'login',
            'hasCorrectFlashVersion': 'true',
            'spring-security-redirect': '/pages/common/index.jsp?&flashVersion=9.0.124.0&hasCorrectFlashVersion=true',
            'username': self.username,
            'j_username': self.username,
            'password': self.password,
            'j_password': self.password,
        }
        r = self.s.post(self.base + "j_spring_security_check", data=data)
        r.raise_for_status()
        if 'loginAction.do' in r.text:
            raise LoginFailure()
        return True

    def search_client(self, mac_or_ip_or_name):
	# Set proper headers
 	headers = {"Accept":"application/json"}
        params = {
            'searchType': 'macOrIpOrName',
            'searchText': mac_or_ip_or_name,
            'lastDetected': 1440,
            'json': 'true',
            'isAscending': 'false',
            'orderByColumn': 'lastSessionTime',
            'sort':  'lastSessionTime',
        }
        r = self.s.get(self.base + "searchClientAction.do", params=params)
        return r.json()['items']
    def getAlarms(self, query):
	# Set proper headers
 	headers = {"Accept":"application/json"}
	params = {
#		'acknowledgementStatus': 'true',
		'severity': 'CRITICAL'
	}
	r = self.s.get(self.base + "api/v1/data/Alarms/", params=params, headers=headers)
        #return r.json()['queryResponse']['entity'][0]['alarmsDTO']['message']
        return r.json()

