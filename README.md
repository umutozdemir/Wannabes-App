# Wannabes-App
Exercise&Diet tracking CRUD web application built with Python & Django & Bootstrap4
# Usage
Once you have cloned the repo, create a virtualenv and install the requirements by entering ```pip install -r requirements.txt``` <br/>
You must have mysql on your computer <br/>
Then, make the migrations for the Django DB ```python manage.py makemigrations python manage.py migrate``` <br/>
Then, run this scripts ```python load_exercises.py, python load_foods.py, python load_video_links.py```    <br/> 
Then, create daily users with this command ```python manage.py daily_routines```  <br/>
Finally, run the server python manage.py runserver  <br/>
The application will be running on http://localhost:8000  <br/>
# Screenshots
https://imgur.com/a/QmPbAYm
