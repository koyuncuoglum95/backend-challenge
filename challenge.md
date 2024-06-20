# Task Management System

## Setup Instructions

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run migrations: `python manage.py makemigrations` and `python manage.py migrate`.
5. Create a superuser: `python manage.py createsuperuser`.
6. Start the development server: `python manage.py runserver`.

## User Credentials

### Admin Users

- **Admin User 1:**
  - Username: `admin1`
  - Password: `password1`
- **Admin User 2:**
  - Username: `admin2`
  - Password: `password2`

## Testing

To run the tests, use the following command:

```bash
python manage.py test tasks
```


## API Authentication

To obtain an authentication token, use the following endpoint:

```http
POST /api-token-auth/


{
  "username": "admin1",
  "password": "password1"
}

{
  "token": "your_token_here"
}


Authorization: Token your_token_here
```

## Sample Data
```
py manage.py shell
```

```
from django.contrib.auth.models import User
from tasks.models import Task, Label

# Create admin1 and admin2 users
admin1 = User.objects.create_user(username='admin1', password='password1')
admin1.is_staff = True
admin1.save()

admin2 = User.objects.create_user(username='admin2', password='password2')
admin2.is_staff = True
admin2.save()

# Create labels for admin1
label1_admin1 = Label.objects.create(name='Work', owner=admin1)
label2_admin1 = Label.objects.create(name='Personal', owner=admin1)

# Create labels for admin2
label1_admin2 = Label.objects.create(name='Urgent', owner=admin2)
label2_admin2 = Label.objects.create(name='Home', owner=admin2)

# Create tasks for admin1
task1_admin1 = Task.objects.create(title='Task 1 for Admin1', description='Description for Task 1', completed=False, owner=admin1)
task1_admin1.labels.add(label1_admin1)

task2_admin1 = Task.objects.create(title='Task 2 for Admin1', description='Description for Task 2', completed=True, owner=admin1)
task2_admin1.labels.add(label2_admin1)

# Create tasks for admin2
task1_admin2 = Task.objects.create(title='Task 1 for Admin2', description='Description for Task 1', completed=False, owner=admin2)
task1_admin2.labels.add(label1_admin2)

task2_admin2 = Task.objects.create(title='Task 2 for Admin2', description='Description for Task 2', completed=True, owner=admin2)
task2_admin2.labels.add(label2_admin2)

print("Sample data created successfully!")
```

