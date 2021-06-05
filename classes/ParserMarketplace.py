from interfaces.iparser import iparser
from classes.Storage import Storage
import classes.ParserFactory
import pymysql.cursors


class ParserMarketplace(iparser):
    FirstRun = True

    def __init__(self, parent_id: int):
        super(ParserMarketplace, self).__init__(parent_id)
        return

    def parse(self, data: dict):
        pfactory = classes.ParserFactory.ParserFactory()

        with Storage.connection.cursor() as cursor:
            country_name = ''

            if 'country' in data.attrib:
                country_name = data.attrib['country']

            country = Storage.database.get_by_field('country', 'name', country_name)

            if not country:
                sql = "INSERT INTO `country` (`name`) VALUES (%s)"
                cursor.execute(sql, (country_name))
                Storage.connection.commit()
                country_id = Storage.database.last_insert_id('country')
            else:
                country_id = country['id']

            marketplace_name = None

            if 'name' in data.attrib:
                marketplace_name = data.attrib['name']

            marketplace_descr = None

            if 'descr' in data.attrib:
                marketplace_descr = data.attrib['descr']

            marketplace_url = None

            if 'url' in data.attrib:
                marketplace_url = data.attrib['url']

            marketplace_img = None

            if 'img' in data.attrib:
                marketplace_img = data.attrib['img']

            sql = "INSERT INTO `marketplace` " \
                  "(`record_id`, `country_id`, `name`, `descr`, `url`, `img`) " \
                  "VALUES " \
                  "(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                self.parent_id,
                country_id,
                marketplace_name,
                marketplace_descr,
                marketplace_url,
                marketplace_img))

            Storage.connection.commit()

            record_id = Storage.database.last_insert_id('marketplace')

        for element in data:
            if element.tag.lower() == 'product':
                parser = pfactory.get_parser('marketplace', 'product', record_id)
                if parser:
                    parser.init_db()
                    parser.parse(element)

                del parser

        return True

    def init_db(self):
        if ParserMarketplace.FirstRun:
            print('ParserMarketplace: initializing DB ... ')

            with Storage.connection.cursor() as cursor:
                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`country` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB;
                            """
                cursor.execute(sql)
                Storage.connection.commit()

                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`marketplace` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `record_id` INT UNSIGNED NOT NULL,
  `country_id` INT UNSIGNED NULL,
  `name` VARCHAR(45) NULL,
  `descr` TEXT NULL,
  `url` VARCHAR(50) NULL,
  `img` VARCHAR(50) NULL,
  PRIMARY KEY (`id`),
  INDEX `record_id` (`record_id` ASC) VISIBLE,
  INDEX `name` (`name` ASC) VISIBLE,
  INDEX `country_id` (`country_id` ASC) VISIBLE,
  CONSTRAINT `fk_marketplace_1`
    FOREIGN KEY (`record_id`)
    REFERENCES `worm`.`records` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_marketplace_2`
    FOREIGN KEY (`country_id`)
    REFERENCES `worm`.`country` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
                            """
                cursor.execute(sql)
                Storage.connection.commit()

                print("OK")

            ParserMarketplace.FirstRun = False
            return True
        else:
            return False
