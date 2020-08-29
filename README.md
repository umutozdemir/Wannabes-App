# Wannabes-App
Exercise&Diet tracking CRUD web application built with Python & Django & Bootstrap4
# Usage
Once you have cloned the repo, create a virtualenv and install the requirements by entering ```pip install -r requirements.txt```
You must have mysql on your computer
Then, make the migrations for the Django DB ```python manage.py makemigrations python manage.py migrate```
Then, run this scripts ```python load_exercises.py, python load_foods.py, python load_video_links.py```
Then, create daily users with this command ```python manage.py daily_routines```
Finally, run the server python manage.py runserver
The application will be running on http://localhost:8000
# Screenshots
https://imgur.com/a/QmPbAYm
