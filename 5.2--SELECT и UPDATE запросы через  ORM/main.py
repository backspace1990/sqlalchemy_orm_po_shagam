import os
import sys

from queries.orm import SyncORM


sys.path.insert(1, os.path.join(sys.path[0], '..'))


SyncORM.create_tables()
SyncORM.insert_data()
SyncORM.select_workers()
SyncORM.update_workers()