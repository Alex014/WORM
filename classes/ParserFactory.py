from interfaces.iparser import iparser
from classes.ParserMarketplace import ParserMarketplace
from classes.ParserProduct import ParserProduct


class ParserFactory:

    def get_parser(self, parent_tag: str, tag_name: str, parent_id: int) -> iparser:
        if parent_tag == 'worm' and tag_name == 'marketplace':
            return ParserMarketplace(parent_id)
        elif parent_tag == 'marketplace' and tag_name == 'product':
            return ParserProduct(parent_id)

        return False
