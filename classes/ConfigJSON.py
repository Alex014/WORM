from interfaces.iconfig import iconfig
import json
import os


class ConfigJSON(iconfig):

    def get_config(self, filename: str) -> dict:

        if os.path.exists(filename):
            f = os.open(filename, os.O_RDONLY)
            dt = os.read(f, os.path.getsize(filename))
            config = json.loads(dt)
            os.close(f)
            return config
        else:
            return {}

