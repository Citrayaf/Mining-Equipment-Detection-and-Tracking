#from flask import Flask, render_template

#app = Flask(__name__)

#@app.route('/')
#def index():
    # Call your API function or use your API logic here
 #   return render_template('index.html')

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5001,debug=True)
 
from flask import Flask, render_template
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

@app.route('/')
def index():
    # Call your API function or use your API logic here
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True, ssl_context=('cert.pem', 'key.pem'))

