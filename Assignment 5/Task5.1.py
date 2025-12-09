import os, time
from flask import Flask, request, session, redirect, url_for, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_fallback_key")  # set SECRET_KEY in env for real use
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# Simple in-memory "user store" with hashed passwords (for demo)
USERS = {
    "admin": generate_password_hash("password123"),
    "user": generate_password_hash("userpass")
}

# Very small rate-limit per username (demo only)
ATTEMPTS = {}  # username -> (count, first_attempt_time)
MAX_ATTEMPTS = 5
WINDOW = 60

HOME_HTML = """
<h2>Secure Login Demo</h2>
{% if user %}
  <p>Welcome {{ user }}! <a href="{{ url_for('logout') }}">Logout</a></p>
{% else %}
  <form method="POST" action="{{ url_for('login') }}">
    Username: <input name="username"><br>
    Password: <input type="password" name="password"><br>
    <input type="submit" value="Login">
  </form>
{% endif %}
"""

def rate_limited(u):
    now = time.time()
    cnt, first = ATTEMPTS.get(u, (0, now))
    if now - first > WINDOW:
        ATTEMPTS[u] = (0, now); return False
    return cnt >= MAX_ATTEMPTS

def record_attempt(u):
    cnt, first = ATTEMPTS.get(u, (0, time.time()))
    ATTEMPTS[u] = (cnt + 1, first)

@app.route('/')
def home():
    return render_template_string(HOME_HTML, user=session.get("user"))

@app.route('/login', methods=['POST'])
def login():
    u = request.form.get("username", "").strip()
    p = request.form.get("password", "")
    if rate_limited(u):
        return "Too many attempts. Try later.", 429
    if u in USERS and check_password_hash(USERS[u], p):
        session.clear(); session["user"] = u
        ATTEMPTS.pop(u, None)
        return redirect(url_for("home"))
    record_attempt(u)
    return "Invalid credentials. <a href='/'>Try again</a>", 401

@app.route('/logout')
def logout():
    session.pop("user", None); return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=False)
