from log import LOG
import socket
import sys
from common import *
import MySQLdb

host = sys.argv[1]
port = int(sys.argv[2])

'''
检查mysql 连接是否ok
'''
try:
    conn = MySQLdb.connect(host=host, user='root',passwd='root', db='test', port=port, connect_timeout=10)
    conn.close()
    LOG.info('MySQL server {}:{} is OK'.format(host, port))
except MySQLdb.Error as e:
    LOG.error('Can not connect to MySQL server {}:{}. error={}'.format(host, port, str(e)))

