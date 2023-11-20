#! /usr/bin/env python3

import sys, os, dotenv


dotenv.load_dotenv()
try: 
  sys.path.append(os.environ['PROJECT_ROOT'])
except:
  sys.path.append(os.path.expanduser('~')+'/Desktop/task_management/')

