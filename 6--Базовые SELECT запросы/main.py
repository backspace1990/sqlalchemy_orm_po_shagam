import os
import sys
import asyncio
#from queries.core import create_tables, insert_data1, insert_data
#from queries.orm import create_tables, insert_data, asyn_insert_data
from queries.core import SyncCore
from queries.orm import SyncORM


sys.path.insert(1, os.path.join(sys.path[0], '..'))


#SyncCore.select_workers()
#SyncCore.update_worker()
#SyncCore.update_worker_sqlal_po_func()


#SyncORM.create_tables()
#SyncORM.insert_data() 
#SyncORM.select_workers() 
#SyncORM.update_workers()
#SyncORM.insert_resumes()
SyncORM.select_resumes_avg_compensation()