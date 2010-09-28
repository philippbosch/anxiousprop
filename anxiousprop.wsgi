import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

activate_this = '/home/pb/.virtualenvs/anxiousprop/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from anxiousprop import app as application
