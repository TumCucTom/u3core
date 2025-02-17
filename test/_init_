import sys
import os

# obtain current location of `__init__.py` 
current_dir = os.path.dirname(os.path.abspath(__file__))

# obtain the root directory of the project
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# add root directroy of the project to `sys.path`，
if project_root not in sys.path:
    sys.path.insert(0, project_root)