from classes.Storage import Storage
from classes.ParserFactory import ParserFactory
import xml.etree.ElementTree as ET
import pymysql.cursors
import pprint


class Iteration:
    FirstRun = True

    def parse(self, name: str, data: str):
        size = len(data)
        try:
            data = ET.fromstring(data)
        except:
            return False

        if data.tag.lower() == 'worm':
            pfactory = ParserFactory()

            with Storage.connection.cursor() as cursor:
                sql = "SELECT * FROM `records` WHERE `uid`=%s AND `name`=%s ORDER BY id DESC LIMIT 1"
                cursor.execute(sql, (size, name))
                result = cursor.fetchone()

                if result:
                    record_id = result['id']
                else:
                    sql = "INSERT INTO `records` (`uid`, `name`) VALUES (%s, %s)"
                    cursor.execute(sql, (size, name))
                    Storage.connection.commit()

                    record_id = Storage.database.last_insert_id('records')

                    for element in data:
                        parser = pfactory.get_parser('worm', element.tag.lower(), record_id)
                        if parser:
                            parser.init_db()
                            parser.parse(element)

                        del parser

        return True

    def init_db(self):
        if Iteration.FirstRun:
            print('\nIteration: initializing DB ... ')

            with Storage.connection.cursor() as cursor:
                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`records` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `uid` VARCHAR(100) NULL,
  `name` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  INDEX `uid` (`uid` ASC) VISIBLE,
  INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB;
                """
                cursor.execute(sql)
                print("OK")
            Iteration.FirstRun = False
            return True
        else:
            return False
