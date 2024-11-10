# holistiplan-be

# Start Django
Create your venv:
```
pip install virtualenv
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Start django
```
./manage.py migrate
./manage.py runserver
```

At least create a super user to test against:

```
./manage.py createsuperuser
```



# Testing
run `pytest`

# Notes:

- With more time I'd like to break up and co-locate the tests, but it asked me to drop the tests in one file so I did 🙏