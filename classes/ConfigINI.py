from interfaces.iconfig import iconfig
import configparser
import os


class ConfigINI(iconfig):

    def get_config(self, filename: str) -> dict:

        if os.path.exists(filename):
            cp = configparser.ConfigParser()
            cp.read(filename)

            config = {}

            for section in cp.sections():
                config[section] = {}
                for key in cp[section]:
                    config[section][key] = cp[section][key]
            return config
        else:
            return {}

