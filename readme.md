# TinyUrl
This repository uses a simple idea of generating a tiny url, to create a scalable system on AWS cloud. 

Uses python backend, and Cassandra database, with the python service hosted in AWS EC2 instances behind a load balancer, and Cassandra installed on a cluster of 2 AWS EC2 instances. 

# Working with cassandra (Virtualbox)


## Cassandra setup
Source : https://phoenixnap.com/kb/install-cassandra-on-ubuntu

conda activate python3.8<p>

## On WSL2
Had some issues getting cassandra to work on WSL. 
To use cqlsh you'll need to use
```
cqlsh localhost --cqlversion="3.4.5"
```

You can start cassandra CLI using the command - 
```
cqlsh
```

but for some weird reason it works only on python3.7, so set environment python3.7 for using cassandra cli

## Create a keyspace
` create keyspace bigcassandra with replication = {'class':'SimpleStrategy', 'replication_factor':3};`

`use bigcassandra;`

List all tables in bigcassandra..

`describe tables;`

`alter keyspace bigcassandra with replication = {'class':'SimpleStrategy', replication_factor:1} and Durable_writes=false;`

keyspace can be thought of a database in SQL parlence

## Create table
`create table emp(emp_id int PRIMARY KEY, emp_name text, emp_city text, emp_sal varint, emp_phone varint);`

`Insert into table
Insert into emp(emp_id, emp_name, emp_city, emp_sal, emp_phone) Values(1, 'test', 'test_city', 500000, 12345);
`


## Create the actual table for url shortening
Create table UrlMap(tiny_url text PRIMARY KEY, url text);

Insert into UrlMap(tiny_url, url) Values ('http://mytinyurl.com/abcd', 'https://www.google.com')

## You can use curl command to test the api

`curl -i -X POST -H "Content-Type: application/json" -d '{"url":"www.test.com"}' http://localhost:5000/add`

## Ensure the name of the cassandra table in Python model is all small letters - Phewww!!! resulted in a lot of time in debugging

## If the service runs in VirtualBox, how do you access this externally?

In that case start the VM in the bridged networking mode. This causes an independent ip address to be assigned to this. You can use that IP address to access this service

This service is containerized into a docker container..

# Troubleshooting connectivity issues between docker and cassandra

You could run into issues connecting the backend running within the docker container and cassandra which is hosted in the base machine.

What finally works is that you need to start the docker, such that it uses the host network --
`sudo docker run --network=host -p 5000:5000 -it 0296699de4d4 /bin/bash`

Tried various other things.. but nothing works..
(Got the solution in https://stackoverflow.com/questions/54876879/connecting-cassandra-container-using-another-container)

## Some debugging tips

Check if you can access a service from docker..

Run
`nc -l 9999` in the base machine

Try to access the service from docker using

`curl 127.0.0.1:9999` .... This will not work, as you cannot access the base machine from docker using the 127 addressing.

Check the ip of the docker using

`ip addr show docker0`

The ip shown there something like `172.17.0.1`, is the ip of the machine that docker can see. Now try accessing the base machine using this IP.

`curl 172.17.0.1:9999` ... This will work. Now change the cassandra connection ip from `127.0.0.1` to `172.17.0.1`

Show the ip of the docker..

`docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>`

# Multi-stage docker

Using a multi-staged docker container build to cut down on the docker build runtime..


`FROM python:3.8-slim as base_image`

`WORKDIR /app`

`COPY requirements.txt ./`
`RUN pip install --no-cache-dir -r requirements.txt`

`FROM base_image AS app_build`

`COPY . ./`

`CMD [ "python", "app.py" ]`

Building the container

`sudo docker build --target app_build -t system_design:tiny_url .`

# Running the test cases
Testing the API

`pytest tests/test_api.py -s`

To run some stress tests on the api's use the following command. This checks how long it takes to insert 10000 URLs and retrieve them. Test on this system shows..

```
(python3.7) pankaj@LAPTOP-1LSIP1HC:~/tiny_url$ pytest tests/test_load_api.py -s
======================================================================== test session starts ========================================================================
platform linux -- Python 3.8.5, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
rootdir: /home/pankaj/tiny_url
collected 1 item                                                                                                                                                    

100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10000/10000 [01:08<00:00, 145.62it/s]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10000/10000 [00:37<00:00, 270.21it/s]
Inserting and retrieving 10000 url took 105.68551993370056 seconds
.

=================================================================== 1 passed in 105.80s (0:01:45) ===================================================================
```


`pytest tests/test_load_api.py`

# Cassandra on EC2 instance
Install cassandra as per the instructions on the above link on an Ubuntu EC2 instance.

Edit `/etc/cassandra/cassandra.yaml` with the following configurations..

Replace localhost with the private ip of the ec2 instance (in this case `172.31.30.180`)

``
seed_provider:
    # Addresses of hosts that are deemed contact points. 
    # Cassandra nodes use this list of hosts to find each other and learn
    # the topology of the ring.  You must change this if you are running
    # multiple nodes!
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "172.31.30.180:7000"
          #- seeds: "127.0.0.1:7000"
rpc_address: 172.31.30.180
listen_address: 172.31.30.180
``

Restart cassandra `sudo systemctl restart cassandra`

Connect to the cassandra instance
`cqlsh 172.31.30.180` and create a keyspace `create keyspace bigcassandra with replication = {'class':'SimpleStrategy', 'replication_factor':3};`

Create a table 
`Create table UrlMap(tiny_url text PRIMARY KEY, url text);`

Run the test case in your local `pytest tests/test_api.py -s`