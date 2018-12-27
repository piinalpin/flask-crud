from flask import render_template, request, redirect
from app import app
from .models import db, Mahasiswa

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

@app.route('/form-update/<int:id>')
def updateForm(id):
    mhs = Mahasiswa.query.filter_by(id=id).first()
    return render_template("form-update.html", data=mhs)

@app.route('/form-update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        nim = request.form['nim']
        try:
            mhs = Mahasiswa.query.filter_by(id=id).first()
            mhs.name = name
            mhs.nim = nim
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    try:
        mhs = Mahasiswa.query.filter_by(id=id).first()
        db.session.delete(mhs)
        db.session.commit()
    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/")