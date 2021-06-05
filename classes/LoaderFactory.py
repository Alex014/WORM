from interfaces.iloader import iloader
from classes.LoaderHTTP import LoaderHTTP
from classes.LoaderHTTPS import LoaderHTTPS
import re


class LoaderFactory:

    def get_loader(self, url: str) -> iloader:
        regex = r"((.+):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)"
        result = re.findall(regex, url)
        proto = result[0][1]

        if proto == 'http':
            return LoaderHTTP()
        elif proto == 'https':
            return LoaderHTTPS()
