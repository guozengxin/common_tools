#!/bin/sh

p=$1
echo $p
pid=`ps aux | grep "$p" | grep -v grep | grep -v killp | awk '{print $2}'`
echo $pid
kill -9 $pid
