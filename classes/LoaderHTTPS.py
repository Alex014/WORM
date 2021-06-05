from interfaces.iloader import iloader
import os
import requests
import warnings


class LoaderHTTPS(iloader):

    def load(self, url: str):
        warnings.filterwarnings("ignore")
        response = requests.get(url, verify=False)
        warnings.filterwarnings("default")

        get_body = response.content

        return get_body.decode('utf8')
