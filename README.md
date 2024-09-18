English | [简体中文](./README_cn.md) 
# Audio-Record-WebPage
Record audio on the web page, store files locally, fill out forms, and store them in a structured database(MySQL). The two correspond by file name.

# Minimal Required Project Structure
only requires the following files.

```
root
└─main.py  # run flask server
└─ctmc_collect.py  # run CTM Collecting
└─myself.py  # personal website
└─templates
│    └─index.html  # front end HTML
│    └─tizhidiaocha.html  # front end HTML CTM
│    └─myself.html  # front end HTML Website
└─databasekits
     └─table_packets.py
```
The other files are not necessary.


# Run this Projects
run MySQL service.
```
[XXX@localhost]$ systemctl start mysqld
```

### Repository System Diagnosis through Cough Sound Collecting
run flask server.
```
python3 main.py
```
open index.html through 127.0.0.1:8000

then record your cough audio and fill out the form blocks, then submit it.

```
sudo mysql -uroot -p
>{root password}
>{root password}
> use {database name}
>select * from {tablename}
```

### CTM Collecting
run flask server.
```
python3 ctmc_collect.py
```
open tizhidiaocha.html through 127.0.0.1:5002

## Personal Website
run flask server.
```
python3 myself.py
```
open myself.html through 127.0.0.1:80

[Click to go to my personal website Ke Zhao](http://zkworkhome.top)

