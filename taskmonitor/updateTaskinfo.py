#!/usr/bin/env python
# encoding=utf8

import sys
import time
import MySQLdb

dbName = 'taskmonitor'
host = '127.0.0.1'
user = 'web'
passwd = 'web'


def currentDate():
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return timeStr


def insert(name):
    db = MySQLdb.connect(host, user, passwd, dbName)
    cursor = db.cursor()
    sqlstring = 'insert into taskinfo (taskname, starttime) values (%s, %s);'
    cursor.execute(sqlstring, [name, currentDate()])
    sqlstring = 'select last_insert_id();'
    cursor.execute(sqlstring)
    rows = cursor.fetchall()
    print rows[0][0]
    cursor.close()
    db.close()


def update(recordId, issucceed, info):
    db = MySQLdb.connect(host, user, passwd, dbName)
    cursor = db.cursor()
    sqlstring = 'update taskinfo set endtime = %s, is_succeed = %s, run_info = %s where id = %s;'
    cursor.execute(sqlstring, [currentDate(), issucceed, info, recordId])
    cursor.close()
    db.close()


def usage(mainName):
    print >> sys.stderr, \
        '''usage:
 1. python mainName insert <taskName>
    print: record ID
 2. python mainName update <id> <is_succeed> <run_info>
    print: None
        '''


def main(argv):
    if len(argv) != 3 and len(argv) != 5:
        usage(sys.argv[0])
        sys.exit()

    if argv[1] == 'insert':
        name = argv[2]
        recordId = insert(name)
    elif argv[1] == 'update':
        recordId = int(argv[2])
        issucceed = int(argv[3])
        info = argv[4]
        recordId = update(recordId, issucceed, info)


if __name__ == '__main__':
    main(sys.argv)
