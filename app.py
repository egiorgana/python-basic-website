from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# INITIALIZE DB
db = SQLAlchemy(app)
# CREATE DB MODEL
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # CREATE A FUNCTION TO RETURN A STRING WHEN WE ADD SOMETHING
    def __repr__(self):
        return '<Name %r>' % self.id


names = ['Eliher', 'Hugo', 'Alejandro', 'Maria', 'Raffles']
subscribers = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', names=names)

@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    message = 'Subscribe To My Email Newsletter'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('CORREO', 'PASSWORD')
    server.sendmail('CORREO', email, message)

    if not first_name or not last_name or not email:
        error_statement = 'All Form Fields Required...'
        return render_template('subscribe.html', 
            error_statement=error_statement, 
            first_name=first_name, 
            last_name=last_name, 
            email=email
        )
    subscribers.append(f'{first_name} {last_name} | {email}')
    return render_template('form.html', subscribers=subscribers)

@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == 'POST':
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        # PUSH TO DB
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return 'There was an error adding your friend...'
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', friends=friends)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return 'There was a problem updating that friend...'
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

if __name__ == '__main__':
    app.run(debug=True)