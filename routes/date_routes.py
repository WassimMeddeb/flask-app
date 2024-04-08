from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Example database URL
db = SQLAlchemy(app)

class DateRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    current_date = datetime.now().date()  # Get current date
    record = DateRecord.query.first()  # Assuming you have a single record for date in your database
    if record:
        current_date = record.date.strftime('%Y-%m-%d')
    return render_template('index.html', current_date=current_date)

@app.route('/save_date', methods=['POST'])
def save_date():
    date = request.form['date']  # Assuming the date is sent via a form submission
    record = DateRecord.query.first()  # Assuming you have a single record for date in your database
    if record:
        record.date = date
    else:
        new_record = DateRecord(date=date)
        db.session.add(new_record)
    db.session.commit()
    return 'Date saved successfully'

if __name__ == '__main__':
    app.run(debug=True)