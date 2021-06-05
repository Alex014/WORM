from interfaces.iparser import iparser


class ParserUnknown(iparser):

    def parse(self, url: str):
        return url
