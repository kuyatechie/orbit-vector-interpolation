# orbit-vector-interpolation
A demo project to show timeseries database capabilities to interpolate missing orbital data

## methodology
Interpolation is done using timescaleDB time bucket gapfill + interpolation method.
The estimation method is done using linear average.
Precision is automatically estimated depending on the given interpolation datetime and the threshold of the time bucket
i.e. if the gap between the time bucket is < 30 mins then the precision is SECONDS, but if > 30 mins then the precision is per minute
Django Rest Framework is used to serve web API.
TimescaleDB + GIS is used to run hyperfunction queries.

![alt text](image.png)

## how to install
### prerequisite
Linux, Docker, Docker Compose

### how to build
Package can be built smoothly using docker compose
```
$ arvin@Omen:~/workspace/orbit-vector-interpolation$ docker compose build
[+] Building 1.3s (17/21)                                                 docker:default
 => [web internal] load build definition from Dockerfile                            0.0s
 => => transferring dockerfile: 316B                                                0.0s
 => [migrate internal] load build definition from Dockerfile                        0.0s
 => => transferring dockerfile: 316B                                                0.0s
 => [migrate internal] load metadata for docker.io/library/python:3.11-bookworm     1.0s
 => [migrate auth] library/python:pull token for registry-1.docker.io               0.0s
 => [web internal] load .dockerignore                                               0.0s
 => => transferring context: 2B                                                     0.0s
 => [migrate internal] load .dockerignore                                           0.0s
 => => transferring context: 2B                                                     0.0s
 => [migrate 1/5] FROM docker.io/library/python:3.11-bookworm@sha256:3cdce69fd5663  0.0s
 => [web internal] load build context                                               0.0s
 => => transferring context: 5.03kB                                                 0.0s
 => [migrate internal] load build context                                           0.0s
 => => transferring context: 5.03kB                                                 0.0s
 => CACHED [migrate 3/5] RUN apt-get update &&     apt-get -y install gdal-bin pyt  0.0s
 => CACHED [migrate 2/5] COPY requirements.txt /app/requirements.txt                0.0s
 => [migrate 4/5] ADD app /app                                                      0.0s
 => [migrate 5/5] WORKDIR /app                                                      0.0s
 => [web] exporting to image                                                        0.0s
 => => exporting layers                                                             0.0s
 => => writing image sha256:6410f4946c140277eb9c253615ccbe0bbbe5cc921297f1e6b12f73  0.0s
 => => naming to docker.io/library/orbit-vector-interpolation-web                   0.0s
 => [migrate] exporting to image                                                    0.1s
 => => exporting layers                                                             0.0s
 => => writing image sha256:b674b2fc15c95afad4427fef2a89d089ace9d0a77d0abf944d2a48  0.0s
 => => naming to docker.io/library/orbit-vector-interpolation-migrate               0.0s
 => [web] resolving provenance for metadata file                                    0.0s
 => [migrate] resolving provenance for metadata file                                0.0s
 ```

### how to run
Run using docker compose
```
arvin@Omen:~/workspace/orbit-vector-interpolation$ docker compose up
[+] Running 4/2
 ✔ Network orbit-vector-interpolation_default      Created                          0.0s
 ✔ Container orbit-vector-interpolation-tsdb-1     Created                          0.1s
 ✔ Container orbit-vector-interpolation-web-1      Created                          0.0s
 ✔ Container orbit-vector-interpolation-migrate-1  Created                          0.0s
Attaching to migrate-1, tsdb-1, web-1
tsdb-1     | The files belonging to this database system will be owned by user "postgres".
tsdb-1     | This user must also own the server process.
tsdb-1     |
tsdb-1     | The database cluster will be initialized with locale "C.UTF-8".
tsdb-1     | The default database encoding has accordingly been set to "UTF8".
tsdb-1     | The default text search configuration will be set to "english".
tsdb-1     |
tsdb-1     | Data page checksums are disabled.
tsdb-1     |
tsdb-1     | fixing permissions on existing directory /home/postgres/pgdata/data ... ok
tsdb-1     | creating subdirectories ... ok
tsdb-1     | selecting dynamic shared memory implementation ... posix
tsdb-1     | selecting default max_connections ... 100
tsdb-1     | selecting default shared_buffers ... 128MB
tsdb-1     | selecting default time zone ... Etc/UTC
tsdb-1     | creating configuration files ... ok
tsdb-1     | running bootstrap script ... ok
tsdb-1     | performing post-bootstrap initialization ... ok
tsdb-1     | initdb: warning: enabling "trust" authentication for local connections
tsdb-1     | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
tsdb-1     | syncing data to disk ... ok
tsdb-1     |
tsdb-1     |
tsdb-1     | Success. You can now start the database server using:
tsdb-1     |
tsdb-1     |     pg_ctl -D /home/postgres/pgdata/data -l logfile start
tsdb-1     |
tsdb-1     | waiting for server to start....2024-10-09 18:08:25.530 UTC [35] LOG:  starting PostgreSQL 15.2 (Ubuntu 15.2-1.pgdg22.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0, 64-bit
tsdb-1     | 2024-10-09 18:08:25.532 UTC [35] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
tsdb-1     | 2024-10-09 18:08:25.537 UTC [38] LOG:  database system was shut down at 2024-10-09 18:08:24 UTC
tsdb-1     | 2024-10-09 18:08:25.540 UTC [35] LOG:  database system is ready to accept connections
tsdb-1     | 2024-10-09 18:08:25.541 UTC [41] LOG:  TimescaleDB background worker launcher connected to shared catalogs
tsdb-1     |  done
tsdb-1     | server started
tsdb-1     | CREATE DATABASE
tsdb-1     |
tsdb-1     |
tsdb-1     | /docker-entrypoint.sh: sourcing /docker-entrypoint-initdb.d/000_install_timescaledb.sh
tsdb-1     | WELCOME TO
tsdb-1     |  _____ _                               _     ____________
tsdb-1     | |_   _(_)                             | |    |  _  \ ___ \
tsdb-1     |   | |  _ _ __ ___   ___  ___  ___ __ _| | ___| | | | |_/ /
tsdb-1     |   | | | |  _ ` _ \ / _ \/ __|/ __/ _` | |/ _ \ | | | ___ \
tsdb-1     |   | | | | | | | | |  __/\__ \ (_| (_| | |  __/ |/ /| |_/ /
tsdb-1     |   |_| |_|_| |_| |_|\___||___/\___\__,_|_|\___|___/ \____/
tsdb-1     |                Running version 2.10.2
tsdb-1     | For more information on TimescaleDB, please visit the following links:
tsdb-1     |
tsdb-1     |  1. Getting started: https://docs.timescale.com/timescaledb/latest/getting-started
tsdb-1     |  2. API reference documentation: https://docs.timescale.com/api/latest
tsdb-1     |  3. How TimescaleDB is designed: https://docs.timescale.com/timescaledb/latest/overview/core-concepts
tsdb-1     |
tsdb-1     | Note: TimescaleDB collects anonymous reports to better understand and assist our users.
tsdb-1     | For more information and how to disable, please see our docs https://docs.timescale.com/timescaledb/latest/how-to-guides/configuration/telemetry.
tsdb-1     |
tsdb-1     | CREATE EXTENSION
tsdb-1     |
tsdb-1     | /docker-entrypoint.sh: running /docker-entrypoint-initdb.d/001_timescaledb_tune.sh
tsdb-1     | Using postgresql.conf at this path:
tsdb-1     | /home/postgres/pgdata/data/postgresql.conf
tsdb-1     |
tsdb-1     | shared_buffers = 3971MB
tsdb-1     | effective_cache_size = 11914MB
tsdb-1     | maintenance_work_mem = 1985MB
tsdb-1     | work_mem = 2541kB
tsdb-1     | timescaledb.max_background_workers = 16
tsdb-1     | max_worker_processes = 35
tsdb-1     | max_parallel_workers_per_gather = 8
tsdb-1     | max_parallel_workers = 16
tsdb-1     | wal_buffers = 16MB
tsdb-1     | min_wal_size = 512MB
tsdb-1     | default_statistics_target = 500
tsdb-1     | random_page_cost = 1.1
tsdb-1     | checkpoint_completion_target = 0.9
tsdb-1     | max_locks_per_transaction = 128
tsdb-1     | autovacuum_max_workers = 10
tsdb-1     | autovacuum_naptime = 10
tsdb-1     | effective_io_concurrency = 256
tsdb-1     | timescaledb.last_tuned = '2024-10-09T18:08:26Z'
tsdb-1     | timescaledb.last_tuned_version = '0.14.3'
tsdb-1     | Writing backup to:
tsdb-1     | /tmp/timescaledb_tune.backup202410091808
tsdb-1     |
tsdb-1     | Recommendations based on 15.51 GB of available memory and 16 CPUs for PostgreSQL 15
tsdb-1     | Saving changes to: /home/postgres/pgdata/data/postgresql.conf
tsdb-1     |
tsdb-1     | /docker-entrypoint.sh: running /docker-entrypoint-initdb.d/010_install_timescaledb_toolkit.sh
tsdb-1     | CREATE EXTENSION
tsdb-1     | CREATE EXTENSION
tsdb-1     | CREATE EXTENSION
tsdb-1     |
tsdb-1     | waiting for server to shut down....2024-10-09 18:08:26.358 UTC [35] LOG:  received fast shutdown request
tsdb-1     | 2024-10-09 18:08:26.360 UTC [35] LOG:  aborting any active transactions
tsdb-1     | 2024-10-09 18:08:26.360 UTC [62] FATAL:  terminating background worker "TimescaleDB Background Worker Scheduler" due to administrator command
tsdb-1     | 2024-10-09 18:08:26.360 UTC [41] FATAL:  terminating background worker "TimescaleDB Background Worker Launcher" due to administrator command
tsdb-1     | 2024-10-09 18:08:26.360 UTC [53] FATAL:  terminating background worker "TimescaleDB Background Worker Scheduler" due to administrator command
tsdb-1     | 2024-10-09 18:08:26.361 UTC [35] LOG:  background worker "logical replication launcher" (PID 42) exited with exit code 1
tsdb-1     | 2024-10-09 18:08:26.361 UTC [35] LOG:  background worker "TimescaleDB Background Worker Launcher" (PID 41) exited with exit code 1
tsdb-1     | 2024-10-09 18:08:26.362 UTC [35] LOG:  background worker "TimescaleDB Background Worker Scheduler" (PID 62) exited with exit code 1
tsdb-1     | 2024-10-09 18:08:26.362 UTC [35] LOG:  background worker "TimescaleDB Background Worker Scheduler" (PID 53) exited with exit code 1
tsdb-1     | 2024-10-09 18:08:26.362 UTC [36] LOG:  shutting down
tsdb-1     | 2024-10-09 18:08:26.363 UTC [36] LOG:  checkpoint starting: shutdown immediate
tsdb-1     | 2024-10-09 18:08:26.887 UTC [36] LOG:  checkpoint complete: wrote 2180 buffers (13.3%); 0 WAL file(s) added, 0 removed, 1 recycled; write=0.010 s, sync=0.509 s, total=0.526 s; sync files=498, longest=0.004 s, average=0.002 s; distance=15728 kB, estimate=15728 kB
tsdb-1     | 2024-10-09 18:08:26.891 UTC [35] LOG:  database system is shut down
tsdb-1     |  done
tsdb-1     | server stopped
tsdb-1     |
tsdb-1     | PostgreSQL init process complete; ready for start up.
tsdb-1     |
tsdb-1     | 2024-10-09 18:08:27.019 UTC [1] LOG:  starting PostgreSQL 15.2 (Ubuntu 15.2-1.pgdg22.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0, 64-bit
tsdb-1     | 2024-10-09 18:08:27.019 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
tsdb-1     | 2024-10-09 18:08:27.019 UTC [1] LOG:  listening on IPv6 address "::", port 5432
tsdb-1     | 2024-10-09 18:08:27.022 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
tsdb-1     | 2024-10-09 18:08:27.026 UTC [97] LOG:  database system was shut down at 2024-10-09 18:08:26 UTC
tsdb-1     | 2024-10-09 18:08:27.031 UTC [1] LOG:  database system is ready to accept connections
tsdb-1     | 2024-10-09 18:08:27.031 UTC [100] LOG:  TimescaleDB background worker launcher connected to shared catalogs
web-1      | Watching for file changes with StatReloader
web-1      | Performing system checks...
web-1      |
migrate-1  | Operations to perform:
migrate-1  |   Apply all migrations: admin, auth, contenttypes, data, sessions
migrate-1  | Running migrations:
migrate-1  |   Applying contenttypes.0001_initial... OK
web-1      | System check identified no issues (0 silenced).
migrate-1  |   Applying auth.0001_initial... OK
web-1      |
web-1      | You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, data, sessions.
web-1      | Run 'python manage.py migrate' to apply them.
migrate-1  |   Applying admin.0001_initial... OK
web-1      | October 09, 2024 - 18:08:31
web-1      | Django version 5.1.1, using settings 'app.settings'
web-1      | Starting development server at http://0.0.0.0:8000/
web-1      | Quit the server with CONTROL-C.
web-1      |
migrate-1  |   Applying admin.0002_logentry_remove_auto_add... OK
migrate-1  |   Applying admin.0003_logentry_add_action_flag_choices... OK
migrate-1  |   Applying contenttypes.0002_remove_content_type_name... OK
migrate-1  |   Applying auth.0002_alter_permission_name_max_length... OK
migrate-1  |   Applying auth.0003_alter_user_email_max_length... OK
migrate-1  |   Applying auth.0004_alter_user_username_opts... OK
migrate-1  |   Applying auth.0005_alter_user_last_login_null... OK
migrate-1  |   Applying auth.0006_require_contenttypes_0002... OK
migrate-1  |   Applying auth.0007_alter_validators_add_error_messages... OK
migrate-1  |   Applying auth.0008_alter_user_username_max_length... OK
migrate-1  |   Applying auth.0009_alter_user_last_name_max_length... OK
migrate-1  |   Applying auth.0010_alter_group_name_max_length... OK
migrate-1  |   Applying auth.0011_update_proxy_permissions... OK
migrate-1  |   Applying auth.0012_alter_user_first_name_max_length... OK
migrate-1  |   Applying data.0001_initial... OK
migrate-1  |   Applying sessions.0001_initial... OK
migrate-1 exited with code 0
```

## how to use
### API Map
#### POST /orbit/
##### POST /orbit/ with 0 values
POST /orbit/
```
{
  "time": "2024-10-10T00:00:00",
  "posx": 0,
  "posy": 0,
  "posz": 0,
  "velx": 0,
  "vely": 0,
  "velz": 0
}
```
Response HTTP 201 CREATED

##### POST /orbit/ with positive values
Sampling another input so we have a time bucket with lower and higher datetime threshold.

POST /orbit/
```
{
  "time": "2024-10-11T00:00:00",
  "posx": 0,
  "posy": 1,
  "posz": 2,
  "velx": 30,
  "vely": 30,
  "velz": 60
}
```
Response HTTP 201 CREATED

#### GET /orbit/interpolate?time=<ISO_DATETIME>
Caveat when running the GET command in the browser, the : symbol should be translated to Unicode equivalent %3A


##### GET /orbit/interpolate?time=2024-10-10T11%3A59%3A00
Sample for time=2024-10-10 11:59:00
```
{
  "time": "2024-10-10 11:59:00",
  "posx": 0,
  "posy": 0.5,
  "posz": 1,
  "velx": 15,
  "vely": 15,
  "velz": 30
}
```
Response HTTP 200 OK

##### GET /orbit/interpolate?time=2024-10-10%2015%3A00%3A00
Sample for time=2024-10-10 15:00:00
```
{
  "time": "2024-10-10 15:00:00",
  "posx": 0,
  "posy": 0.6666666666666666,
  "posz": 1.3333333333333333,
  "velx": 20,
  "vely": 20,
  "velz": 40
}
```
Response HTTP 200 OK

### swagger
Swagger Page is provided to see available APIs and easily sample data.
On your browser, go to http://localhost:8000/

![alt text](image-1.png)

Alternatively, you can also make use of the debug tool in POST
http://localhost:8000/orbit/

![alt text](image-2.png)

## known limitation
1. The application cannot predict movement if the time bucket threshold (both upper and lower) is not present. 

##### GET /orbit/interpolate?time=2011-10-10%2000%3A00%3A00
Sample for time=2011-10-10 00:00:00
```
{
  "Error": "Insufficient data."
}
```
Response HTTP 404 Not Found

##### GET /orbit/interpolate?time=2026-10-10%2000%3A00%3A00
Sample for time=2026-10-10 00:00:00
```
{
  "Error": "Insufficient data."
}
```
Response HTTP 404 Not Found

2. The application cannot handle wrong datetime format

##### GET /orbit/interpolate?time=2024-10-10T00%3A00%3A00Y
Sample for time=2026-10-10 00:00:00Y
```
{
  "Error": "Invalid datetime format. Please use %Y-%m-%dT%H:%M:%S."
}
```
Response HTTP 404 Not Found

3. Auto precision leveling might introduce significant margin of error. Details on how this work can be found on util.py.
