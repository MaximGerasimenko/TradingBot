from flask import Flask, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TestSignal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<TestSignal %r>' % self.id

"""
Main Page 
"""
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


"""
Main Page 
"""
@app.route('/signals/all', methods=['GET'])
@app.route('/signals/all/', methods=['GET'])
def index_signals_all():
    return render_template('signals_list.html', signals=TestSignal.query.order_by(TestSignal.date).all(), all=True)


"""
Main API page 
"""
@app.route('/api', methods=['GET'])
@app.route('/api/', methods=['GET'])
def index_api():
    return render_template('api_page.html')


"""
Binance API page 
"""
@app.route('/api/binance', methods=['GET'])
@app.route('/api/binance/', methods=['GET'])
def index_api_binance():
    return render_template('api_binance.html')


"""
WebHook API page 
"""
@app.route('/api/webhook', methods=['GET'])
@app.route('/api/webhook/', methods=['GET'])
def index_api_webhook():
    return 'WebhookAPI'


"""
Webhook
"""
@app.route('/webhook', methods=['POST'])
@app.route('/webhook/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            db.session.add(TestSignal(title='Testing', text=json.dumps(request.json)))
            db.session.commit()
            return 'success', 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return abort(400)
    else:
        abort(400)


"""
Starting Application
Change debug=False before deploy
"""
if __name__ == '__main__':
    app.run(debug=True)
