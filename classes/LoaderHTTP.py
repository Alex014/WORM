from interfaces.iloader import iloader
import pycurl
from io import BytesIO


class LoaderHTTP(iloader):

    def load(self, url: str):
        b_obj = BytesIO()
        crl = pycurl.Curl()

        crl.setopt(crl.URL, url)
        crl.setopt(crl.WRITEDATA, b_obj)
        crl.perform()
        crl.close()

        get_body = b_obj.getvalue()
        return get_body.decode('utf8')
