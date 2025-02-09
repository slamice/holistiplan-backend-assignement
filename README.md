# Start Project:
1. Create your venv:
```
pip install virtualenv
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Run migrations
```
./manage.py migrate
```

3. At least create a super user to test against:

```
./manage.py createsuperuser
```

4. Start django
```
./manage.py runserver
```

# Testing
run `pytest`

# Authentication
### 1. Basic Authentication
```
curl -u YOUR_USERNAME:YOUR_PASSWORD http://127.0.0.1:8000/snippets
```

### 2. Token Authorization:
```
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"}'
```

To test fetching with the token:
```
curl http://127.0.0.1:8000/snippets/ -H "Authorization: YOUR_TOKEN" -v
```

# Notes:
- With more time I'd like to break up and co-locate the tests, but it asked me to drop the tests in one file so I did 🙏
- Instead of making an Abstract User and extending the User Admin model, I created a new model and made a 1:1
  relationship to it. I think extending the User model soft delete is probably a better strategy, I ran into a few problems trying to resolve admin functions when using the managers. Given teh time limit I thought a simpler approach was better.
- Soft delete:
  - Admin can soft delete a user after going into a specific user and deleting them ( in teh interface)
  - Admin can see soft deleted users: `http://127.0.0.1:8000/users/?include_soft_deletes=True`
- Made AuditLog its own app, seems like a significant part of the system.
  - In reality there are many audit loggers. Would consider looking for an off the shelf one or creating a plugin for DRF to do this.
- I ran out of time to do more tests and JWT, but am confident I can do these!

