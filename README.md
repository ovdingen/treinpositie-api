# spoorpositie-api

## Available functions

`GET /v1/trein/<trein_nr>`

Returns latest positions for `trein_nr`. Returns one position for every train unit.

`GET /v1/mat/<mat_nr>`

Returns position for one specific train unit (by material number)

`GET /v1/total`

Returns positions of ALL trains. 


## Setting up

###This is a unchanged copy from the ovfiets-api docs. Watch out for pitfalls when directly copypasting this

(We use gunicorn and systemd in this example. It's up to you to use something else.)

1) Create a new user called (i.e.) `ovfiets-api` which will run the HTTP api and the data collector.

# `adduser --disabled-login --disabled-password --shell /bin/false --home $CLONE_DIR --no-create-home $USER_NAME`

2) Create a directory, grant permission to the newly created user and clone this project.

$ `mkdir $CLONE_DIR && chown $USER_NAME:$USER_NAME $clone_dir && sudo -u $USER_NAME git clone $CLONE_URL`

3) Copy conf/daemon.json.dist to conf/daemon.json and change any necessary settings. We recommend using [universal-pubsub](https://github.com/StichtingOpenGeo/universal) as middleware between the OpenOV ZMQ server and the OVFiets API.

4) Install requirements.

# `pip install -r requirements.txt`

5) Install gunicorn. 

# `pip install gunicorn`

6) Copy `data/db.sqlite.dist` to `data/db.sqlite`.

7) Create a unit file for the data gatherer. Here is a example:

```
[Unit]
Description=OVFiets API data gatherer daemon
After=syslog.target network.target

[Service]
User=ovfiets-api
WorkingDirectory=/opt/ovfiets-api/
ExecStart=/usr/bin/python /opt/ovfiets-api/api-daemon.py conf/daemon.json

[Install]
WantedBy=multi-user.target
```

8) Create a unit file for Gunicorn. Here is a example:

```
[Unit]
Description=OVFiets API HTTP Gunicorn application
After=syslog.target network.target

[Service]   
User=ovfiets-api
WorkingDirectory=/opt/ovfiets-api/
ExecStart=/usr/local/bin/gunicorn -b 127.0.0.1:9000 http:app

[Install]
WantedBy=multi-user.target
```

Please note that the above is just a example, and not an extensive guide.

