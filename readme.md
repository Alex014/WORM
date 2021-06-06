# WORM
## The idea
WORM is a shortcut for World Object MaRkup language, a markup language to describe all real world objects (product, hotel, article, drone, ... ) needed to be found.
In other words WORM is an HTML for searchable objects.
WORM is an XML extension.
In a larger scale it's a search system, which consists of 4 things
1. A WORM file.
2. A blockchain with a link to a WORM file or including WORM file.
3. A Data Collector, which collects data through blockchain and puts the data into database.
4. Frontend for selecting, sorting and displaying the data to the user.

Data Collector together with the Frontend is a Search Engine.
There can be many Search Engines for different types of objects.
In our case we have a Search Engine specialized in products.
It's not a final solution, but a technology demo.

This is a backend part of a search system - a Data Collector
## Diagram
```
  [SITE 1]  [SITE 2]  [SITE 3]  ...  [SITE n]
  
     ||        ||        ||             ||
     ||        ||        ||             ||
     \/        \/        \/             \/
     
     =====================================
              [[[ BLOCKCHAIN  ]]]
     =====================================
  
      ||             ||                ||
      ||             ||                ||
      \/             \/                \/
     
   [SEARCH]      [SEARCH]           [SEARCH]
   [ENGINE]      [ENGINE]           [ENGINE]
   [  1   ]      [  2   ]           [  n   ]
                                       ||
                    ||=================||
                    ||      
                    \/                                 
             {DATA COLLECTOR}
                    ||
                    ||
                    \/      
                {DATABASE}
                    ||
                    ||
                    \/
                {FRONTEND}    
```
## WORM language
```xml
<worm>
    <!-- Products -->
    <marketplace name="Marketplace 1" descr="[DESCRIPTION]" lang="en" country="" url="[URL]" img="[IMAGE-URL]">
        <product name="Product 1" price="466.15" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag3,Subtag333,SSR"/>
        <product name="Product 2" price="997.62" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag3,Subtag33,SSQ"/>
        <product name="Product 3" price="946.44" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag5,Subtag555,SSMMM"/>
        <product name="Product 4" price="25.54" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag4,Subtag444,Subtag444"/>
        <product name="Product 5" price="729.14" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag4,Subtag4444,SSB"/>
        <product name="Product 6" price="622.39" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag1,Subtag1,SS3"/>
        <product name="Product 7" price="679.47" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag1,Subtag3,SS13"/>
        <product name="Product 8" price="510.4" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag2,Subtag22,SSA"/>
        <product name="Product 9" price="386.17" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag4,Subtag444,SSC"/>
        <product name="Product 10" price="693.5" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag4,Subtag4444,SSB"/>
    </marketplace>
    <!-- News -->
    <newsfeed name="Marketplace 1" descr="[DESCRIPTION]" lang="en" country="" url="[URL]" img="[IMAGE-URL]">
        <news title="Title" descr="[DESCRIPTION]" date="000-00-00 00:00" url="[URL]" img="[IMAGE-URL]" author="First Last Name" tags="tag1,tag2,tag3"/>
    </newsfeed>
    <!-- Social Network -->
    <social name="Decentaspeak" descr="[DESCRIPTION]" lang="en" country="" url="[URL]" img="[IMAGE-URL]">
        <author name="First Last Name or nickname" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" friends="Friend 1,Friend 2,Author 3" tags="tag1,tag2,tag3">
            <post title="Title" descr="[DESCRIPTION]" date="000-00-00 00:00" url="[URL]" img="[IMAGE-URL]" likes="666" tags="tag1,tag2,tag3"/>
        </author>
    </social>
    <!-- Blog -->
    <blog name="Marketplace 1" descr="[DESCRIPTION]" lang="en" country="" url="[URL]" img="[IMAGE-URL]">
        <article title="Title" descr="[DESCRIPTION]" date="000-00-00 00:00" url="[URL]" img="[IMAGE-URL]" author="First Last Name" tags="tag1,tag2,tag3"/>
    </blog>
    <!-- Delivery -->
    <delivery name="Food delivery kebab 1" descr="[DESCRIPTION]" country="" url="[URL]" img="[IMAGE-URL]" tags="tag1,tag2,tag3"/>
    <!-- Workshop -->
    <workshop name="Workshop 1" descr="[DESCRIPTION]" country="" url="[URL]" img="[IMAGE-URL]">
        <service title="Repair 123" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" tags="tag1,tag2,tag3"/>
    </workshop>
    <!-- Source code -->
    <hub name="Super Source Hub" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]">
        <repository title="Title" descr="[DESCRIPTION]" url="[URL]" img="[IMAGE-URL]" author="First Last Name or nickname" lang="c++" tags="tag1,tag2,tag3"/>
    </hub>
</worm>
```
Only `<marketplace>` tag is implemented
## Blockchain
Launch Emercoin wallet and go to "Manage Names" section
There are two kinds of records
1. `worm:record-name` The record with the WORM file inside blockchain record
2. `worm-url:[URL]`  The record with URL link to WORM file (record contents are ignored)
Currently the Data Collector supports two protocols [HTTP] and [HTTPS].
## Installation
### Dependencies
* `pip install pycurl`
* `pip install requests`
* `pip install warnings`
* Emercoin wallet at https://emercoin.com
MySQL database
### Configuration
The configuration is available in two formats: .ini and .json, and by default is located in `confid/config.json` directory of Data Collector
```json
{
  "blockchain": {"host": "localhost", "port": 8332, "user": "user", "password": "hpe74xjkd"},
  "database": {"host": "localhost", "port": 3306, "user": "root", "password": "root",
    "database": "worm"
  },
  "test": {
    "url": "http://wf.zxc/test-data.php"
  }
}
```
* blockchain - settings for blockchain connection
* database - settings for database connection
* test - test environment settings
  * url - URL with test data generated by frontend
#### Data Collector
Once launched the Data Collector works in eternal cycle and looks for a new records in blockchain, it also looks if the new size of existing records differs from old size.
Currently the Data Collector supports two protocols [HTTP] and [HTTPS].
##### Database
The tables in database gets generated automaticaly by Data Collector.
The main table is `records` table, all other tables are connected to this table
Table `records` has two main columns
* uid - size of WORM file
* name - name of WORM record in blockchain.
The name is unique for each WORM file record, but if the size of new variant of WORM file differs from previous one, than a new record in table `records` is made and new variant of data gets generated.
#### Emercoin wallet
Put the following lines in `emercoin.conf` file:
```
rpcuser=user
rpcpassword=hpe74xjkd
rpcallowip=127.0.0.1
rpcport=8332
```
This file is located in `~/.emercoin` directory in Linux systems and in `Application Data/emercoin` directory on Windows systems
## Test run
Test works without the blockchain
* Launch frontend environment and make sure, that *test url* (in our case `http://wf.zxc/test-data.php`)  is available
* Execute `python test.py`
If everything is OK, than test data should be generated and collected by Data Collector.
## Production
Production needs blockchain to run
Execute `python main.py`
It is recomended to run tests in Emercoin testnet environment.
## Donations
* Bitcoin bc1qfw0aadqdxeqmuaqxxelracfnvw0la0h2d870al
* Emercoin ELdkWCGkU1dkUME41ksNVy4nXijf3BsnB9
## Contacts
Email: chosenone111@protonmail.com