#!/bin/sh

function GetUsernameAndPassword {
	echo -e "Please input username: \c" 
	read username

	echo -e "Please input password: \c"
	read -s password
}

dailybuild_file=
url=
while getopts "d:u:" arg #选项后面的冒号表示该选项需要参数
do
	case $arg in
		 d)
			dailybuild_file=$OPTARG
			shift; shift
			;;
		 u)
			url=$OPTARG
			shift; shift
			;;
		 ?)  
			echo "unkonw argument"
			exit 1
			;;
	esac
done

if [ -z "$dailybuild_file" ] && [ -z "$url" ]; then
	echo "-d dailybuild_file OR -u url"
	exit 1
fi

if [ -n "$dailybuild_file" ] && [ -n "$url" ]; then
	echo "-d and -u must indicate one!"
	exit 1
fi

GetUsernameAndPassword

if [ -n "$dailybuild_file" ]; then
	if [ ! -e "$dailybuild_file" ]; then
		echo "$dailybuild_file not exist!"
		exit 1
	fi
	maindir=$1
	if [ -z $maindir ]; then
		echo "maindir must indicated!"
		exit 1
	fi
	start=0
	dir_count=0
	while read line; do
		if [ $start -eq 0 ]; then
			findline=`echo $line | grep 'main.svn'`
			if [ -n "$findline" ]; then
				start=1
			fi
		else
			name=${line%%=*}
			url=${line##*=}
			if echo $name | grep ^#; then
				continue
			fi
			if echo $url | grep http; then
				null=
			else
				continue
			fi
			if [ $name == "." ]; then
				svn co --username $username --password $password $url $maindir
			else
				let dir_count=$dir_count+1
				name_array[$dir_count]=$name
				url_array[$dir_count]=$url
			fi 
		fi 
	done < $dailybuild_file
	cd $maindir
	for (( i=1; i<=$dir_count; i++ )); do
		name=${name_array[$i]}
		url=${url_array[$i]}
		svn co --username $username --password $password $url $name
	done
	cd ..
fi

if [ -n "$url" ]; then
	maindir=$1
	svn co --username $username --password $password $url $maindir
fi
