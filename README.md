An Orwellian web application for document sharing between teachers and students. 

Teachers are able to create classrooms and share documents with students within each class. Students can view documents after facial recognition verifies their id. While they view a document, an eye-tracking library tracks whether they are actually looking at the document.
## Features
* Document sharing
* Facial recognition
* Eye tracking
* Data visualisation (chart.js)
* Federated identity (google sign-in)
* REST API for CRUD operations with the database
## Technologies
* Django
* SQLite
## Installation
* Make sure you have python3 installed
* Create and source a virtual environment
* `cd` to the directory: `document-sharing-django-app/web_app/`
* Run `cat requirements.txt | xargs -n 1 pip install`
* `cd` to `document-sharing-django-app/web_app/mysite/`
* Run `python manage.py runserver --noreload --nothreading`
    * These options are necessary for facial recognition to work.
* Go to `http://127.0.0.1:8000/read/` (port may be different)
