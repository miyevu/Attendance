from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db = SQLAlchemy(app)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance', methods=['GET'])
def get_attendance():
    attendance_list = Attendance.query.all()
    return jsonify([entry.name for entry in attendance_list])

@app.route('/attendance', methods=['POST'])
def post_attendance():
    name = request.form.get('name')
    if name:
        new_attendance = Attendance(name=name)
        db.session.add(new_attendance)
        db.session.commit()
        return '', 200
    else:
        return 'Bad Request', 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
