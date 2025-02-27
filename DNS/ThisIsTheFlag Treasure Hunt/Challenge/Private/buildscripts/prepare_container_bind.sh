#!/bin/bash
#This script should be run on a base centos image
#Demo file should not use in production should import known trusted rpm keys


BASEPATH="$(cd $(dirname "${BASH_SOURCE[0]}");pwd)"
cd "$BASEPATH"

yum -y install bind bind-utils

ZONE="thisistheflag.be"
ZONEFOLDER=${ZONE}


#ephemeral config
cp -vf "$BASEPATH"/named.conf /etc/


#Dnssec config
install -d  -o named -g named -Z named_cache_t /var/named/dynamic/${ZONEFOLDER}/
install -o named -g named -Z named_cache_t "$BASEPATH"/${ZONEFOLDER}.zone.unsigned /var/named/dynamic/${ZONEFOLDER}/
install -d -o named -g named -Z named_cache_t /var/named/dynamic/${ZONEFOLDER}/keys

#Create ZSK
#dnssec-keygen -r /dev/urandom -a RSASHA256 -b 1024 -3 -K "/var/named/dynamic/${ZONEFOLDER}/keys/" $ZONE
#Create KSK dummy key
#dnssec-keygen -r /dev/urandom -a RSASHA256 -b 2048 -3 -K "/var/named/dynamic/${ZONEFOLDER}/keys/" -fk $ZONE
cp -vr "$BASEPATH"/keys/* /var/named/dynamic/${ZONEFOLDER}/keys/


chown -Rv named. /var/named/dynamic/${ZONEFOLDER}/keys/



SIGVALIDITYNORMAL=10000
SIGVALIDITYNORMALSEC=$(( ${SIGVALIDITYNORMAL} * 24 * 3600 ))
dnssec-signzone -v 3 -S -K /var/named/dynamic/${ZONEFOLDER}/keys/ -x -T 86400 -a -o $ZONE -3 1A4E9B6C -H 5 -A -X now+3456000 -e now+${SIGVALIDITYNORMALSEC} -j 259200 -I text -O text -f /var/named/dynamic/${ZONEFOLDER}/${ZONEFOLDER}.zone /var/named/dynamic/${ZONEFOLDER}/${ZONEFOLDER}.zone.unsigned

#Just copy over do not sign
#cp -av /var/named/dynamic/${ZONEFOLDER}/${ZONEFOLDER}.zone.unsigned /var/named/dynamic/${ZONEFOLDER}/${ZONEFOLDER}.zone 

/usr/libexec/generate-rndc-key.sh
