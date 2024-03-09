English | [简体中文](./README_cn.md) 
# Audio-Record-WebPage
 Recording audio on the web page and store it in the database.

run MySQL service.
```
[XXX@localhost]$ systemctl start mysqld
```

run flask server.
```
python3 main.py
```

open index.html through 127.0.0.1:8000

then record your cough audio and input table blocks, then submit.

```
sudo mysql -uroot -p
>{root password}
>{root password}
> use {database name}
>select * from {tablename}
```

# file structure
```
root
└─main.py  # run flask server
└─audio.py  # audio segment object
└─templates
│    └─index.html  # front end HTML
└─databasekits
│    └─test_conn.py
│    └─table_packets.py
│    └─sqlscripts
│    │    └─SQL file, create databse, create teble
```
