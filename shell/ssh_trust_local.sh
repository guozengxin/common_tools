#! /bin/sh
#####################################################################
# �ڱ�����ǰ�û����ͻ�������Զ����������������֮�佨��rsa���ι�ϵ
# usage: sh ssh_trust_local.sh remotehost remoteuser remotepasswd 
# �������ֱ�������������룬����-p����
#####################################################################

ssh_exp=/search/guozengxin/tools/shell/ssh.exp

usage()
{
	echo "usage: sh ssh_trust_local.sh remotehost remoteuser remotepasswd"
	echo "������ֱ�������������룬����-p����"
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
		echo -n "������Զ����������������������: "
		read -s remotepasswd
		echo
	fi
}

keygen()
{
	if [ -e $local_rsa_pub ]; then
		echo "��Կ���ڣ�����Ҫ����"
	else
		echo "��Կ�����ڣ���ʼ����..."
		./ssh-keygen.exp default
	fi
}

keycopy()
{
	hn=`hostname`
	remote_keyname=id_rsa.pub."$hn"
	echo "����Կ������Զ��������λ�ã�~/.ssh/"$remote_keyname"..."
	$ssh_exp put $remotehost 22 $remoteuser $remotepasswd '~/.ssh/'$remote_keyname $local_rsa_pub 
	echo "����Կ���뵽Զ�������ļ���~/.ssh/authorized_keys..."
	$ssh_exp exec $remotehost 22 $remoteuser $remotepasswd "cd ~/.ssh/ && cat $remote_keyname >> authorized_keys"
	echo "����Զ������authorized_keys�ļ�Ȩ�ޣ�600..."
	$ssh_exp exec $remotehost 22 $remoteuser $remotepasswd "cd ~/.ssh/ && chmod 600 authorized_keys"
}

local_rsa_pub=~/.ssh/id_rsa.pub
arg_parse "$@"
keygen
keycopy
