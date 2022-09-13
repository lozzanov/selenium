# Create 3 Docker containers. 

 - selenium-grid 
 - python-app
 - database



```console

$ sudo docker-compose ps 
    Name                   Command               State                                         Ports                                       
-------------------------------------------------------------------------------------------------------------------------------------------
database        docker-entrypoint.sh tail  ...   Up      0.0.0.0:3306->3306/tcp,:::3306->3306/tcp                                          
python-app      tail -f /dev/null                Up                                                                                        
selenium-grid   /opt/bin/entry_point.sh          Up      0.0.0.0:4444->4444/tcp,:::4444->4444/tcp, 0.0.0.0:5900->5900/tcp,:::5900->5900/tcp

```

From python-app trigger test script.

```console

$ sudo docker-compose exec python-app bash 
root@python:/# python tests/start_test.py 
```

Unittest added

```console

# python tests/test_version.py
```

From VNC Viewer monitor the performing test.

VNC client is monitoring 172.20.20.2:5900 selenium-grid.




