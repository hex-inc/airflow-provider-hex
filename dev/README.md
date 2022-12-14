## Dev Environment Setup

This sets up an Airflow dev environment for local development and
testing.

Read here for more detailed information on how the environment is
configured: https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#customizing-the-quick-start-docker-compose

To start:

First, initialize the database. When you see:

```
make init
```

When you see:

```
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.3.4
start_airflow-init_1 exited with code 0
```

The database creation is complete. Now start the containers with

```
make dev
```

Once the healthchecks show ready, you can login using the
username/password: `airflow` at http://localhost:8080

Create a hex connection: http://localhost:8080/connection/add

* Connection ID: `hex_default`
* Connection Type: `Hex Connection`
* Host: `https://app.hex.tech`
* Hex API Token: `your-token-here`


## Deployment

To deploy to pypi, tag any commit with a valid version number, and then push the tag.
Versions are set in the VERSION.txt file and CircleCI will fail if a release doesn't
match the version specified in VERSION.txt

```shell
git add -u
git commit -m 'add some commit message'
git push
git tag -a 0.1.0 -m "Release 0.1.0 "
git push origin 0.1.0
```
