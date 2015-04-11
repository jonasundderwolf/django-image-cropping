import os

if 'TRAVIS' in os.environ:
    from example.conf.travis import *
else:
    from example.conf.tests import *
