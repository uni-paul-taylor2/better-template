# Template
Basic auth and user model ready to go, time to wrap over CRUD


# Flask Starter Template
A template for simple fastapi projects.

# Creating a virtual environment

```
$ python -m venv venv
```

# Activating the virtual environment

#### On Mac / Linux
```bash
$ source venv/bin/activate
```
#### On Windows
```
$ venv\Scripts\activate
```


# Installing Dependencies
```
$ pip install -e .
```


# Running the Project
```
$ fastapi dev
```

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. (If python doesn't work, python3)

```
$ python app/cli.py initialize
```