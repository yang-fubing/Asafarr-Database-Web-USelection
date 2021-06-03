create database dbpj;

alter database dbpj default character set utf8;

create user 'guest'@'%' identified by '123123';
grant select on dbpj.* to 'guest'@'%';
grant all privileges on dbpj.django_session to 'guest'@'%';
flush privileges;

SET GLOBAL innodb_file_per_table=ON;
