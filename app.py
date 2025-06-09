from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy user storage (you can replace this with a database later)
users = {}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
def home():
    return '<h2>Welcome to QuickGST! <a href="/login">Login</a> or <a href="/register">Register</a></h2>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash("User already exists!")
        else:
            users[email] = password
            flash("User registered successfully!")
            return redirect(url_for('login'))
    return render_template_string('''
        <h2>Register</h2>
        <form method="post">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
        <a href="/">Back</a>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if users.get(email) == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")
    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        <a href="/">Back</a>
    ''')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"<h2>Welcome, {current_user.id}!</h2><a href='/logout'>Logout</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
