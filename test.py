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

print("Importing test data")

url = conf['test']['url']

lf = LoaderFactory()
loader = lf.get_loader(url)

itr = Iteration()
itr.init_db()
itr.parse('test-data', loader.load(url))
