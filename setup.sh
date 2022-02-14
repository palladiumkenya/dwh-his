#!/bin/bash
set -e
echo "${0}: Dumping data into tables in DB created."
service mysql start
#systemctl start mysqld
echo "initialize database"
mysql < /mysql/mfldbdump.sql
#mysql < /mysql/mfldbdump.sql
service mysql stop
echo "${0}: Successfully dumped DB"