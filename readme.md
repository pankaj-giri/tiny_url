# TinyUrl
This repository uses a simple idea of generating a tiny url, to create a scalable system on AWS cloud. 

Uses python backend, and Cassandra database, with the python service hosted in AWS EC2 instances behind a load balancer, and Cassandra installed on a cluster of 2 AWS EC2 instances. 

# Working with cassandra (Virtualbox)


## Cassandra setup
Source : https://phoenixnap.com/kb/install-cassandra-on-ubuntu

conda activate python3.8<p>

You can start cassandra CLI using the command - 
<p>cqlsh<p>
but for some weird reason it works only on python3.7, so set environment python3.7 for using cassandra cli

alter keyspace bigcassandra with replication = {'class':'SimpleStrategy', replication_factor:1} and Durable_writes=false;

keyspace can be thought of a database in SQL parlence

use bigcassandra;

## Create table
create table emp(emp_id int PRIMARY KEY, emp_name text, emp_city text, emp_sal varint, emp_phone varint);

Insert into table
Insert into emp(emp_id, emp_name, emp_city, emp_sal, emp_phone) Values(1, 'test', 'test_city', 500000, 12345);


## Create the actual table for url shortening
Create table UrlMap(tiny_url text PRIMARY KEY, url text);

Insert into UrlMap(tiny_url, url) Values ('http://mytinyurl.com/abcd', 'https://www.google.com')

## You can use curl command to test the api

curl -i -X POST -H "Content-Type: application/json" -d '{"url":"www.test.com"}' http://localhost:5000/add

## Ensure the name of the cassandra table in Python model is all small letters - Phewww!!! resulted in a lot of time in debugging

## If the service runs in VirtualBox, how do you access this externally?

In that case start the VM in the bridged networking mode. This causes an independent ip address to be assigned to this. You can use that IP address to access this service