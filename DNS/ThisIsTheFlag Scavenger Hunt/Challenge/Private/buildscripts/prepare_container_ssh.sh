#!/bin/bash
#This script should be run on a base centos image
#Demo file should not use in production should import known trusted rpm keys


BASEPATH="$(cd $(dirname "${BASH_SOURCE[0]}");pwd)"
cd "$BASEPATH"

yum -y install openssh-server
/usr/libexec/openssh/sshd-keygen ed25519
/usr/libexec/openssh/sshd-keygen ecdsa
/usr/libexec/openssh/sshd-keygen rsa

#This is user is added without password, in this puzzle we do not require to login, we only want to show the banner
useradd -m cyberwarrior

cp -vf "$BASEPATH"/etc/ssh/sshd_config /etc/ssh/sshd_config
cp -vf "$BASEPATH"/etc/issue /etc/issue