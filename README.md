
# Tax Buddy Pro

#### Open windows command line in project directory
#### Run the following commands:

Create a virtual environment using

```
py -m venv venv
```

activate venv using

```
venv\Scripts\activate
```

Install required packages with the following command

```
pip install -r requirements.txt
```

Run the migration commands

```
python manage.py makemigrations
python manage.py migrate
```

Craete a super user by the following command

```
python manage.py createsuperuser
```


Start the app using 

```
py manage.py runserver 0.0.0.0:8000
or
python manage.py runserver 0.0.0.0:8000
```

Then navigate to:

http://localhost:8000/
