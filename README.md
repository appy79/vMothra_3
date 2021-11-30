# vMothra

## Setup

### Make a virtual environment
```
python -m venv venv
```

### Install dependencies
```
pip install -r requirements.txt
```

### Create a file named .env
```
touch .env
```

### Get the parameters expected from .env.example file to the .env file and fill the values

    1) Secret key can be any random string.(String Value)
    2) Attempts are the number of attempts that a person will get for each stage.(Integer Value)
    3) Godzillas are the roll number swhich when registered will become admins of the application. Give space separated values. Example (GODZILLAS=205120010 205120034)
    4) Upgrades are the names of all the ranks that are possible. For now only 9 can be assigned. Example (UPGRADES=born noob unknown amateur average working famous creator wip)

### Create migrations
```
flask db init
```
```
flask db migrate
```
```
flask db upgrade
```
### Run the application
```
python app.py
```