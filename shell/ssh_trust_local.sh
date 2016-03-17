#! /bin/sh
#####################################################################
# 在本机当前用户（客户机）与远程主机（服务器）之间建立rsa信任关系
# usage: sh ssh_trust_local.sh remotehost remoteuser remotepasswd 
# 如果不想直接输入明文密码，可用-p代替
#####################################################################

ssh_exp=~/tools/common_tools/shell/ssh.exp

usage()
{
	echo "usage: sh ssh_trust_local.sh remotehost remoteuser remotepasswd"
	echo "果不想直接输入明文密码，可用-p代替"
}

arg_parse()
{
	remotehost=$1
	remoteuser=$2
	remotepasswd=$3
	if [ -z $remotehost ] || [ -z $remoteuser ] || [ -z $remotepasswd ]; then
		usage 
		exit -1
	fi
	if [ $remotepasswd == "-p" ]; then
		echo -n "请输入远程主机（服务器）的密码: "
		read -s remotepasswd
		echo
	fi
}

keygen()
{
	if [ -e $local_rsa_pub ]; then
		echo "公钥存在，不需要创建"
	else
		echo "公钥不存在，开始创建..."
		./ssh-keygen.exp default
	fi
}

keycopy()
{
	hn=`hostname`
	remote_keyname=id_rsa.pub."$hn"
	echo "将公钥拷贝到远程主机，位置：~/.ssh/"$remote_keyname"..."
	$ssh_exp put $remotehost 22 $remoteuser $remotepasswd '~/.ssh/'$remote_keyname $local_rsa_pub 
	echo "将公钥加入到远程主机文件：~/.ssh/authorized_keys..."
	$ssh_exp exec $remotehost 22 $remoteuser $remotepasswd "cd ~/.ssh/ && cat $remote_keyname >> authorized_keys"
	echo "设置远程主机authorized_keys文件权限：600..."
	$ssh_exp exec $remotehost 22 $remoteuser $remotepasswd "cd ~/.ssh/ && chmod 600 authorized_keys"
}

local_rsa_pub=~/.ssh/id_rsa.pub
arg_parse "$@"
keygen
keycopy

