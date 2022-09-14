# Selenium Automation Test

### This project creates three Docker containers. 

 - selenium-grid 
 - python-app
 - database

**python-app** container is used for management and performing tests. A python script creates remote connection to the webdriver in **selenium-grid** and performs Selenium Automation Test. The test is to navigate to website python.org and fetch some data. 
This data is structured in a list of dictionaries and inserted in the MariaDB database in **database** container.


In order to monitor the Chrome browser activities in the **selenium-grid** container a VNC client is used. VNC Viewer from the Host machine is connected to the exposed port of the **selenium-grid** container. All containers have static IP addresses configured in docker-compose.yml in order to be easily accessed. VNC Viewer from the Host is connected to 172.20.20.2:5900 to the **selenium-grid** . 
**python-app** container inserts the test data to 172.30.30.2 in **database** .

The network between **selenium-grid** and **python-app** is *selenium_grid_net* 
and  between **python-app** and **database** is used *db_net* .



### CLI Commands

From the Host machine with *docker-compose* containers are controlled. 

```console

$ sudo docker-compose ps 
    Name                   Command               State                                         Ports                                       
-------------------------------------------------------------------------------------------------------------------------------------------
database        docker-entrypoint.sh tail  ...   Up      0.0.0.0:3306->3306/tcp,:::3306->3306/tcp                                          
python-app      tail -f /dev/null                Up                                                                                        
selenium-grid   /opt/bin/entry_point.sh          Up      0.0.0.0:4444->4444/tcp,:::4444->4444/tcp, 0.0.0.0:5900->5900/tcp,:::5900->5900/tcp

```

From **python-app**  tests are started.

```console

$ sudo docker-compose exec python-app bash
 
root@python:/# ls tests/start_test.py 
start_test.py    test_version.py  

```

```console 

root@python:/# python tests/start_test.py 
Test Started
Status Code from Selenium Grid: 200
Connecting to Selenium Grid
Data saved to file
Connecting to Database
Create table
Insert data
Test Finished
root@python:/# 

```

Unit test to assert existing/non-existing python versions

```console

sudo docker-compose exec python-app bash

root@python:/# ls tests/
output           start_test.py    test_version.py  

```

```console

root@python:/# python tests/test_version.py 
//tests/test_version.py:6: ResourceWarning: unclosed file <_io.TextIOWrapper name='/tests/output' mode='r' encoding='UTF-8'>
  self.assertNotIn('3.11', open("/tests/output").read())
ResourceWarning: Enable tracemalloc to get the object allocation traceback
.
----------------------------------------------------------------------
Ran 1 test in 0.006s

OK


```

Verification of the successful insertion of data in **database** .

```console

$ sudo docker-compose exec database bash
 
root@mariadb:~# mysql
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 40
Server version: 10.3.34-MariaDB-0ubuntu0.20.04.1 Ubuntu 20.04

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

 
MariaDB [(none)]> use versions;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [versions]> select * from tbl_versions;
+----------------+--------------------+----------------+----------------+------------------+
| Python version | Maintenance status | First released | End of support | Release schedule |
+----------------+--------------------+----------------+----------------+------------------+
| 3.10           | bugfix             | 2021-10-04     | 2026-10        | PEP 619          |
| 3.9            | security           | 2020-10-05     | 2025-10        | PEP 596          |
| 3.8            | security           | 2019-10-14     | 2024-10        | PEP 569          |
| 3.7            | security           | 2018-06-27     | 2023-06-27     | PEP 537          |
| 2.7            | end-of-life        | 2010-07-03     | 2020-01-01     | PEP 373          |
+----------------+--------------------+----------------+----------------+------------------+
5 rows in set (0.001 sec)


```
### Notes

File 50-server.cnf is used for configuring MariaDB server. A single change is done in this file compare to the original one. Commenting the line :

```console

#bind-address            = 127.0.0.1

```

This way the database is exposed for access outside of localhost and can be accessed from other containers.

```console

netstat -anop | grep 3306
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      -                    off (0.00/0/0)
tcp6       0      0 :::3306                 :::*                    LISTEN      -                    off (0.00/0/0)


```

