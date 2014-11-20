#!/bin/sh
# 这个脚本的功能是将输入文件split成多个小文件，后缀名以日期来分隔

inputfile=$1
linecount=$2
prefix=$3
begintime=$4
timeunit=$5

# 把输入文件按行分割，前缀名为$tempprefix
tempprefix=".temp-smartsplit."
split -d -l $linecount -a 5 $inputfile $tempprefix

# 时间单位必须为 day 或者 hour
if [ "$timeunit" = "day" ] || [ "$timeunit" = "hour" ]; then
	echo ""
else
	timeunit=hour
fi

# 计算输入的begintime
d1=`date -d "$begintime" +%s`
d2=`date +%s`
if [ $timeunit = "day" ]; then
	diff=$(((d1-d2) / 86400))
elif [ $timeunit = "hour" ]; then
	diff=$(((d1-d2) / 3600))
else
	diff=0
fi
echo $diff

files=`ls $tempprefix?????`
count=`ls $tempprefix????? | wc -l`
for f in `seq 0 $((count-1))`
do
	suffix=`printf "%05d" $f`
	filename=${tempprefix}${suffix}
	let a=$diff+$f
	if [ "$timeunit" = "day" ]; then
		nsuffix=`date -d "$f days" +%Y%m%d%H`
	elif [ "$timeunit" = "hour" ]; then
		nsuffix=`date -d "$f hours" +%Y%m%d%H`
	fi
	mv $filename ${prefix}$nsuffix
done
