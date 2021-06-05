import os
import sys
import select
from classes.ConfigJSON import ConfigJSON
from classes.ConfigINI import ConfigINI
from classes.Storage import Storage
from classes.BlockchainEMC import BlockchainEMC
from classes.DatabaseMySQL import DatabaseMySQL
from classes.Iteration import Iteration
from classes.LoaderFactory import LoaderFactory

config = ConfigJSON()
conf = config.get_config(os.path.dirname(__file__)+os.path.sep+'config/config.json')
# config = ConfigINI()
# conf = config.get_config(os.path.dirname(__file__)+os.path.sep+'config/config.ini')
# pprint.pp(conf['blockchain'])

blk = BlockchainEMC(conf['blockchain']['host'], conf['blockchain']['port'], conf['blockchain']['user'], conf['blockchain']['password'])
db = DatabaseMySQL(conf['database']['host'], conf['database']['port'], conf['database']['user'], conf['database']['password'], conf['database']['database'])
Storage.blockchain = blk
Storage.database = db
Storage.connection = db.check()

print("Press [Q] and hit [RETURN] to stop the script")

if blk.check() and Storage.connection:

    while True:
        print('.', end='')

        records = blk.loadDirectData()
        print('.', end='')
        for record in records['result']:
            resource = blk.show_resource(record['name'])['result']

            itr = Iteration()
            itr.init_db()
            itr.parse(record['name'], resource['value'])

            del itr

        print('.', end='')

        records = blk.loadUrlData()
        print('.', end='')
        for record in records['result']:
            parts = record['name'].split(':')
            del parts[0]
            url = ":".join(parts)

            lf = LoaderFactory()
            loader = lf.get_loader(url)

            itr = Iteration()
            itr.init_db()
            itr.parse(record['name'], loader.load(url))

            del loader
            del itr

        FirstRun = False

        i, o, e = select.select([sys.stdin], [], [], 5)

        if i:
            input_string = sys.stdin.read(1).strip().lower()
            if input_string == 'q':
                print("STOPPED")
                break
            print(input_string)
