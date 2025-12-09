from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    html_file_path = os.path.join(os.path.dirname(__file__), 'Task3.html')
    return send_file(html_file_path)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if username and password:
        print(f"Successful login! Username: {username}")
        return f"<h1>Login Successful!</h1><p>Welcome, {username}!</p><a href='/'>Back to Login</a>"
    else:
        return "<h1>Login Failed!</h1><p>Username and password are required.</p><a href='/'>Back to Login</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

