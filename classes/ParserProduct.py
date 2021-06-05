from interfaces.iparser import iparser
from classes.Storage import Storage
import classes.ParserFactory
import pymysql.cursors


class ParserProduct(iparser):
    FirstRun = True

    def __init__(self, parent_id: int):
        super(ParserProduct, self).__init__(parent_id)
        return

    def parse(self, data: dict):
        if not ('name' in data.attrib):
            return False
        if not ('tags' in data.attrib):
            return False

        with Storage.connection.cursor() as cursor:
            # Lang
            lang_name = 'en'

            if 'lang' in data.attrib:
                lang_name = data.attrib['lang']

            lang = Storage.database.get_by_field('lang', 'name', lang_name)

            if not lang:
                sql = "INSERT INTO `lang` (`name`) VALUES (%s)"
                cursor.execute(sql, (lang_name))
                Storage.connection.commit()
                lang_id = Storage.database.last_insert_id('lang')
            else:
                lang_id = lang['id']

            # Product tags
            tags = data.attrib['tags'].split(',')
            params = []
            sql_params = []
            for tag in tags:
                params.append(tag)
                params.append(lang_id)
                sql_params.append("(%s, %s)")
            sql = "INSERT IGNORE INTO `tags` (`name`,`lang_id`) VALUES "+','.join(sql_params)
            cursor.execute(sql, params)

            # Product
            product_descr = ''
            if 'descr' in data.attrib:
                product_descr = data.attrib['descr']

            product_url = ''
            if 'url' in data.attrib:
                product_url = data.attrib['url']

            product_img = ''
            if 'img' in data.attrib:
                product_img = data.attrib['img']

            product_price = 0.00
            if 'price' in data.attrib:
                product_price = float(data.attrib['price'])

            sql = "INSERT INTO `products` (`marketplace_id`, `name`, `descr`, `url`, `img`, `price`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.parent_id, data.attrib['name'], product_descr, product_url, product_img, product_price))
            Storage.connection.commit()
            product_id = Storage.database.last_insert_id('products')

            # Products_tags
            params = []
            sql_params = []
            for tag in tags:
                params.append(tag)
                sql_params.append("%s")
            sql = "INSERT INTO `products_tags` SELECT "+str(product_id)+", id FROM `tags` WHERE name IN ("+','.join(sql_params)+")"
            cursor.execute(sql, params)
            Storage.connection.commit()


        return True

    def init_db(self):
        if ParserProduct.FirstRun:
            print('ParserProduct: initializing DB ... ')

            with Storage.connection.cursor() as cursor:
                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`products` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `marketplace_id` INT UNSIGNED NOT NULL,
  `name` VARCHAR(45) NULL,
  `price` float DEFAULT 0,
  `descr` TEXT NULL,
  `url` VARCHAR(50) NULL,
  `img` VARCHAR(50) NULL,
  PRIMARY KEY (`id`),
  INDEX `name` (`name` ASC) VISIBLE,
  INDEX `price` (`price` ASC) VISIBLE,
  INDEX `marketplace_id` (`marketplace_id` ASC) VISIBLE,
  CONSTRAINT `fk_products_1`
    FOREIGN KEY (`marketplace_id`)
    REFERENCES `worm`.`marketplace` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
                                        """
                cursor.execute(sql)
                Storage.connection.commit()

            with Storage.connection.cursor() as cursor:
                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`lang` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` CHAR(2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB;
                                        """
                cursor.execute(sql)
                Storage.connection.commit()

            with Storage.connection.cursor() as cursor:
                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`tags` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `lang_id` INT UNSIGNED NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE,
  INDEX `fk_tags_1_idx` (`lang_id` ASC) VISIBLE,
  CONSTRAINT `fk_tags_1`
    FOREIGN KEY (`lang_id`)
    REFERENCES `worm`.`lang` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
                                        """
                cursor.execute(sql)
                Storage.connection.commit()

            with Storage.connection.cursor() as cursor:
                sql = """
CREATE TABLE IF NOT EXISTS `worm`.`products_tags` (
  `products_id` INT UNSIGNED NOT NULL,
  `tags_id` INT UNSIGNED NOT NULL,
  INDEX `product` (`products_id` ASC) VISIBLE,
  INDEX `tag` (`tags_id` ASC) VISIBLE,
  UNIQUE INDEX `pt` (`products_id` ASC, `tags_id` ASC) VISIBLE,
  CONSTRAINT `fk_products_tags_1`
    FOREIGN KEY (`products_id`)
    REFERENCES `worm`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_products_tags_2`
    FOREIGN KEY (`tags_id`)
    REFERENCES `worm`.`tags` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
                                        """
                cursor.execute(sql)
                Storage.connection.commit()

            ParserProduct.FirstRun = False
            return True
        else:
            return False
