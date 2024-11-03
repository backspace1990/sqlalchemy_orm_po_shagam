import os
import sys
import asyncio
#from queries.core import create_tables, insert_data1, insert_data
from queries.orm import create_tables, insert_data, asyn_insert_data


sys.path.insert(1, os.path.join(sys.path[0], '..'))


#create_tables()
#insert_data()


create_tables()
asyncio.run(asyn_insert_data())