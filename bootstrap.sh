#!/usr/bin/env bash

service mysql start
mysql -u root < /root/dbinit.sql
exec supervisord -n
