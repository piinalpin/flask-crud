# CRUD Application With Flask and SQLAlchemy (Python 3)

Tutorial for building Create, Read, Update and Delete Website Application With Flask and SQLAlchemy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you have installed Python 3 on your device

### Project structure
```
* flask-project/
  |--- app/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- templates/ (html file)
  |    |--- __init__.py
  |--- venv/
  |--- run.py
```

### Step to create flask project

A step by step series of examples that tell you how to get a development env running

1. Install virtual environment
```
pip install virtualenv
```
2. Create virtual environment and activate inside your flask-project directory according the above structure
```
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . env/bin/activate
```
3. Install some third party librares on your virtual environment with pip
```
pip install flask sqlalchemy flask-sqlalchemy
```
4. Create `run.py` directory inside flask-project according the above structure
```python
from app import app
app.run(debug=True, host='127.0.0.1', port=5000)
```
5. Create `controller.py` according the abpove structure `flask-crud/app/module/`
```python
from flask import render_template, request
from app import app

@app.route('/')
def index():
    return "My CRUD Flask App"
```
6. Create `__init__.py` inside app directory according the above structure `flask-crud/app/`
```python
from flask import Flask

app = Flask(__name__)

from app.module.controller import *
```
7. Run first this application to make sure can running with terminal or command promt
```
python run.py
```
9. Access `localhost:5000` according port that created in `run.py`

![Sample 1](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-1.PNG)

10. Create an input form called `home.html` inside `templates` directory according the above structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Crud</title>
</head>
<body>
<h3>Form Add Mahasiswa</h3>
<form action="/" method="POST">
    <table>
        <tr>
            <td>Nama Lengkap</td>
            <td>:</td>
            <td><input type="text" name="name"></td>
        </tr>
        <tr>
            <td>Nomor Induk Mahasiswa</td>
            <td>:</td>
            <td><input type="text" name="nim"></td>
        </tr>
        <tr>
            <td><button type="submit">Save</button></td>
        </tr>
    </table>
</form>
</body>
</html>
```
11. Change `return "My CRUD Flask App"` in `controller.py` to `return render_template("home.html")` 
```python
from flask import render_template, request
from app import app

@app.route('/')
def index():
    return render_template("home.html")
```

![Sample 2](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-2.PNG)

12. Then modify function `index()` to accept method `POST` request
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
    return render_template("home.html")
```
![Sample 3](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-3.PNG)
![Sample 4](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-4.PNG)

13. Configure the database with SQLAlchemy, you should modify `__init__.py` and it will be created `flaskcrud.db` inside `app` directory
```python
import os
from flask import Flask

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "flaskcrud.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

from app.module.controller import *
```
14. Define model to application, you should create `models.py` file inside `module` directory according the above structure.
```python
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    nim = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)
```

15. The structure of database should like as follows

Mahasiswa  |
------------- |
`id (Integer, PK, Autoincrement, NOT NULL)`  |
`name (String, NOT NULL)`  |
`nim (String, NOT NULL)`  |

16. Stop app if that is still running, press `CTRL+C` key to quit and type `python` to go to python terminal

![Sample 4](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-5.PNG)

17. Type command bellow to create database file `flaskcrud.db`
```
>>> from bookmanager import db
>>> db.create_all()
>>> exit()
```
18. The structure project will be look as follows
```
* flask-project/
  |--- app/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- templates/ (html file)
  |    |--- __init__.py
  |    |--- flaskcrud.db
  |--- venv/
  |--- run.py
```
19. Modify `controller.py` to create function to storing data of `Mahasiswa` then save to the database that is already made and retrieving data with `Mahasiswa.query.all()` it will be retrieving all data from database then made with `try` and `except` to handling an error
```python
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        nim = request.form['nim']
        try:
            mhs = Mahasiswa(nim=nim, name=name)
            db.session.add(mhs)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    listMhs = Mahasiswa.query.all()
    print(listMhs)
    return render_template("home.html", data=enumerate(listMhs,1))
```

20. Then modify `home.html` file to show that data is already inputed on database from input form
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Crud</title>
</head>
<body>
<h3>Form Add Mahasiswa</h3>
<form action="/" method="POST">
    <table>
        <tr>
            <td>Nama Lengkap</td>
            <td>:</td>
            <td><input type="text" name="name"></td>
        </tr>
        <tr>
            <td>Nomor Induk Mahasiswa</td>
            <td>:</td>
            <td><input type="text" name="nim"></td>
        </tr>
        <tr>
            <td><button type="submit">Save</button></td>
        </tr>
    </table>
</form>

<h3>Data Mahasiswa</h3>
<table border="1">
    <tr>
        <th>No</th>
        <th>Nomor Induk Mahasiswa</th>
        <th>Nama</th>
    </tr>
    {% for no, x in data %}
        <tr>
            <td>{{ no }}</td>
            <td>{{ x.nim }}</td>
            <td>{{ x.name }}</td>
        </tr>
    {% endfor %}
</table>
</body>
</html>
```
21. 









### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
