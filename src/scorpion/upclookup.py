#!/usr/bin/env python
#
#

import sys
from xmlrpclib import ServerProxy, Error

from config import upc_database_key

rpc_key = upc_database_key

if __name__=='__main__':
	if len(sys.argv) != 2:
		print 'Usage: fetchupc.py <upc>'
		exit
	else:
		s = ServerProxy('http://www.upcdatabase.com/xmlrpc')
		params = { 'rpc_key': rpc_key, 'upc': sys.argv[1] }
		print s.lookup(params)



