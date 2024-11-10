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
- Instead of making an Abstract User and extending the User Admin model, I created a new model and made a 1:1
  relationship to it. I think extending the User model soft delete is probably a better strategy, I ran into a few problems trying to resolve admin functions when using the managers. Given teh time limit I thought a simpler approach was better.