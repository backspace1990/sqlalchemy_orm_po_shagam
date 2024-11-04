import os
import sys

from queries.core import SyncCore


sys.path.insert(1, os.path.join(sys.path[0], '..'))


SyncCore.select_workers()
SyncCore.update_worker()
SyncCore.update_worker_sqlal_po_func()