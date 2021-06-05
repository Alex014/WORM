from interfaces.iblockchain import iblockchain
import requests
import json


class BlockchainEMC(iblockchain):

    def __init__(self, host, port, user, password):
        self.url = host
        self.port = port
        self.login = user
        self.password = password
        return

    def get_info(self):
        return self.__method("getinfo", [])

    def check(self):
        try:
            self.get_info()
        except Exception:
            print('No connection to blockchain')
            return False

        return True

    def show_resource(self, name):
        return self.__method("name_show", [name, '', 'base64'])

    def __method(self, method, params):
        url = self.__get_url()

        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "1.0",
            "id": 0,
        }

        response = requests.post(url, json=payload).json()
        return response

    def __parse_record(self, data_json_str):
        return json.loads(data_json_str)

    def __pack_record(self, data):
        return json.dumps(data)

    def __get_url(self):
        return "http://{}:{}@{}:{}/".format(self.login, self.password, self.url, self.port)

    def loadDirectData(self):
        return self.__method("name_filter", ['^worm:.+', 0, 0, 0, '', ''])

    def loadUrlData(self):
        return self.__method("name_filter", ['^worm-url:.+', 0, 0, 0, '', ''])