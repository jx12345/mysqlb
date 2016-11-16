#!/usr/bin/env python2.7
import os
import time
import MySQLdb
import sqlite3

dbs = list()
dbs.append({
  'name'    : '', 
  'rhost'   : '',
  'ruser'   : '',
  'rpwd'    : '',
  'rdb'   : '',
  'backup_path' : '',
})

lhost = 'localhost'
luser = 'root'
lpwd = ''

for i, db in enumerate(dbs):
  print i, db['name']

db_no = int(raw_input("Which db do you want to backup? "))
db = dbs[db_no]
filename = db['backup_path'] +  db['name'] + '_' + time.strftime('%Y-%m-%d_%H:%M:%S') + '.sql' 

str = 'mysqldump -u ' + db['ruser'] + ' -p' + "'" + db['rpwd'] + "'" + ' -h ' + db['rhost'] + ' ' + db['rdb'] + ' > ' + filename

print str
n = raw_input("Ok going to run backup. Hit return when ready...")
os.system(str)

print "Backup should be complete to [%s]:" % filename
os.system ("ls -la " + filename)

do_import = raw_input("\nImport into local db [%s], db will created if not exists (y/N): " % db['name'])

if do_import == 'y':
  enter_name = raw_input("Enter new database name or just enter to keep name as %s: " % db['name'])
  if enter_name != '':
    db['name'] = enter_name
  
  mysqldb = MySQLdb.connect(lhost, luser, lpwd)
  cursor = mysqldb.cursor()
  sql = "CREATE DATABASE IF NOT EXISTS `" + db['name'] + "`;"
  print sql
  cursor.execute(sql)
  mysqldb.close()

  str = 'mysql -u ' + luser + ' -p' + "'" + lpwd + "' " + db['name'] + ' < ' + filename
  print "Ok, attempting import with command %s" % str
  os.system(str)
else:
  print "Ok, no import."

print "My work is done."

