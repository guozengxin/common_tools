#!/bin/sh

p=$1
echo $p
pid=`ps aux | grep "$p" | grep -v grep | grep -v killp | awk '{print $2}'`
echo "killing "$pid
kill -9 $pid
