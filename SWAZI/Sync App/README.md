### Create a virtualEnv
``` sh
 python3 -m venv venv
```

### Activate the Virtual Environment

``` sh
source venv/bin/activate`
```

### Install Dependencies
``` sh
pip install fastapi uvicorn jinja2 pyodbc requests`
```

### Spin the server

``` sh
uvicorn dhis2_sync_service:app --reload`
```