from urllib import request
import simplejson as json
from flask import Flask, redirect, url_for, session, render_template, Response
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import mysql.connector

from authlib.integrations.flask_client import OAuth

app = Flask(__name__, template_folder='templates')
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)
app.secret_key = 'ying wu college 2021 secret key'

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'stockData'
mysql.init_app(app)

# Authentication -------------------- #
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='290202919562-2qd67u9ko2016ijo95f2no2ssa3a4bs6.apps.googleusercontent.com',
    client_secret='poHIJ00YY61YC8g4yh1QGjfV',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)


# ----------------------------------- #

@app.route('/', methods=['GET'])
def index():
    email = dict(session).get('email', None)
    user = {'username': 'Stock Portfolio'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM stockPortfolioImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, stocks=result)


@app.route('/view/<int:stock_id>', methods=['GET'])
def record_view(stock_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM stockPortfolioImport WHERE id=%s', stock_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', stock=result[0])


@app.route('/edit/<int:stock_id>', methods=['GET'])
def form_edit_get(stock_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM stockPortfolioImport WHERE id=%s', stock_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', stock=result[0])


@app.route('/edit/<int:stock_id>', methods=['POST'])
def form_update_post(stock_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Symbol'), request.form.get('Company_Name'), request.form.get('Rating'),
                 request.form.get('Weight'), request.form.get('Gain_Loss'),
                 request.form.get('Gain_Loss_1'), request.form.get('Price'), request.form.get('Price_Target'), stock_id)
    sql_update_query = """UPDATE stockPortfolioImport t SET t.Symbol = %s, t.Company_Name = %s, t.Rating = %s, t.Weight = 
    %s, t.Gain_Loss = %s, t.Gain_Loss_1 = %s, t.Price = %s, t.Price_Target = %s, WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/stocks/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New stock Form')


@app.route('/stocks/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Symbol'), request.form.get('Company_Name'), request.form.get('Rating'),
                 request.form.get('Weight'), request.form.get('Gain_Loss'),
                 request.form.get('Gain_Loss_1'), request.form.get('Price'), request.form.get('Price_Target'))
    sql_insert_query = """INSERT INTO stockPortfolioImport (Symbol,Company_Name,Rating,Weight,Gain_Loss,Gain_Loss_1,Price, Price_Target) VALUES (%s, %s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:stock_id>', methods=['POST'])
def form_delete_post(stock_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM stockPortfolioImport WHERE id = %s """
    cursor.execute(sql_delete_query, stock_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/stocks', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM stockPortfolioImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/stocks/<int:stock_id>', methods=['GET'])
def api_retrieve(stock_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM stockPortfolioImport WHERE id=%s', stock_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/stocks/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/stocks/<int:stock_id>', methods=['PUT'])
def api_edit(stock_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/stocks/<int:stock_id>', methods=['DELETE'])
def api_delete(stock_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


# Authentication Section Start
@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


# Authentication Section End

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
