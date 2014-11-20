#!/bin/sh
# ����ű��Ĺ����ǽ������ļ�split�ɶ��С�ļ�����׺�����������ָ�

inputfile=$1
linecount=$2
prefix=$3
begintime=$4
timeunit=$5

# �������ļ����зָǰ׺��Ϊ$tempprefix
tempprefix=".temp-smartsplit."
split -d -l $linecount -a 5 $inputfile $tempprefix

# ʱ�䵥λ����Ϊ day ���� hour
if [ "$timeunit" = "day" ] || [ "$timeunit" = "hour" ]; then
	echo ""
else
	timeunit=hour
fi

# ���������begintime
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
