#! /bin/bash

#Quick configuration of nginx front-end and apache back-end on archlinux
#apache
pacman -Syu apache
cp httpd.conf /etc/httpd/conf/httpd.conf
systemctl start httpd
#Database
pacman -S mariadb
mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
systemctl start mariadb
mysql_secure_installation
#php   
pacman -S php php-apache

#nginx
pacman -S nginx
cp nginx.conf /etc/nginx/nginx.conf
systemctl start nginx

systemctl enable httpd mariadb nginx
systemctl restart httpd mariadb nginx

# Default: nginx index files in /ust/share/nginx/html with port 80, 
# apache index file is in /srv/http with port 8080