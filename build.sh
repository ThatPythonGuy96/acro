#! /usr/bin/env bash

set -o errexit   #  exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations users
python manage.py makemigrations music
python manage.py migrate --no-input

echo "=== Creating initial data ==="
python manage.py shell << END
from users.models import User
import os

user, _ = User.objects.get_or_create(
    email='admin@gmail.com',
    username='admin',
    is_superuser=True,
    is_staff=True,
    is_active=True,
    is_admin=True
)
user.set_password('admin123')
user.save()

print("Initial data setup completed")
END

echo "=== Build completed successfully! ==="
