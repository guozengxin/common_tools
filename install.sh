#!/bin/sh

cmd=install
if [ ! -z $1 ];then
	cmd=$1
fi

thisDir=`pwd`
installDir=/usr/local/bin/
apps="shell/ssh.exp  shell/ssh-keygen.exp  shell/ssh_trust_local.sh send_mail/send_mail.php send_mail/convert_html.py python/url.py python/iciba.py sohu_spider"
chmod +x $apps

if [ $cmd == "install" ]; then
	set -ux
	for app in $apps;do
		ln -fs $thisDir/$app /usr/local/bin/
	done
elif [ $cmd == "uninstall" ]; then
	set -ux
	for app in $apps;do
		unlink /usr/local/bin/`basename $app`
	done
else
	echo "$cmd not supported"
fi
