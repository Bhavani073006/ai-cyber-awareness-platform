from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'

DB = "database.db"

# Email configuration - Set these directly or use environment variables
SMTP_SERVER = 'smtp.gmail.com'  # or your SMTP server
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@gmail.com'  # Replace with your email
SMTP_PASSWORD = 'your-app-password'  # Replace with your app password
ALERT_EMAIL = 'manager@company.com'  # Default manager email

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    """Initialize database with tables and sample data"""
    with conn() as c:
        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT,
                department TEXT,
                manager_email TEXT,
                risk_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_activity table
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Create alerts table
        c.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                alert_type TEXT,
                message TEXT,
                severity TEXT,
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Check if users table is empty
        cursor = c.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            sample_users = [
                ('Bhavani', 'bhavanibhanu@gmail.com', 'Software Engineer', 'Engineering', 'tech.manager@company.com', 25),
                ('Tulasi', 'Tulasi@gmail.com', 'HR Specialist', 'Human Resources', 'hr.manager@company.com', 15),
                ('Bavitha', 'Bavitha0210@gmail.com', 'Sales Executive', 'Sales', 'sales.manager@company.com', 30),
                ('Lasya', 'Lasya0730@gmail.com', 'Financial Analyst', 'Finance', 'finance.manager@company.com', 10),
                ('Abhigna', 'Abhigna@gmail.com', 'Marketing Lead', 'Marketing', 'marketing.manager@company.com', 20)
            ]
            c.executemany('''
                INSERT INTO users (name, email, role, department, manager_email, risk_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_users)
            print("Sample users added to database!")

def send_alert_email(user_data, action_details):
    """Send email alert to manager about suspicious activity"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚨 Security Alert: Suspicious Activity Detected - {user_data['name']}"
        msg['From'] = SMTP_USERNAME
        msg['To'] = user_data['manager_email']
        
        # Create HTML email body
        html = f'''
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .alert {{ background-color: #ff4444; color: white; padding: 20px; border-radius: 5px; }}
                .details {{ background-color: #f5f5f5; padding: 15px; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="alert">
                <h2>⚠️ Security Alert: Phishing Simulation</h2>
                <p>An employee has clicked a suspicious link and entered credentials.</p>
            </div>
            
            <div class="details">
                <h3>Employee Details:</h3>
                <table>
                    <tr><td><strong>Name:</strong></td><td>{user_data['name']}</td></tr>
                    <tr><td><strong>Email:</strong></td><td>{user_data['email']}</td></tr>
                    <tr><td><strong>Department:</strong></td><td>{user_data['department']}</td></tr>
                    <tr><td><strong>Role:</strong></td><td>{user_data['role']}</td></tr>
                    <tr><td><strong>Current Risk Score:</strong></td><td>{user_data['risk_score']}</td></tr>
                </table>
                
                <h3>Incident Details:</h3>
                <table>
                    <tr><td><strong>Action:</strong></td><td>{action_details['action']}</td></tr>
                    <tr><td><strong>Timestamp:</strong></td><td>{action_details['timestamp']}</td></tr>
                    <tr><td><strong>IP Address:</strong></td><td>{action_details['ip_address']}</td></tr>
                    <tr><td><strong>User Agent:</strong></td><td>{action_details['user_agent']}</td></tr>
                </table>
            </div>
            
            <p><strong>Action Required:</strong> Please review this incident and schedule security awareness training if necessary.</p>
            <p><a href="http://localhost:5000/dashboard" style="background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Dashboard</a></p>
        </body>
        </html>
        '''
        
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    c = conn()
    
    # Get all users with their activity counts
    users = c.execute('''
        SELECT u.*, 
               COUNT(a.activity_id) as total_activities,
               MAX(a.timestamp) as last_activity
        FROM users u
        LEFT JOIN user_activity a ON u.user_id = a.user_id
        GROUP BY u.user_id
        ORDER BY u.risk_score DESC
    ''').fetchall()
    
    # Get recent alerts
    alerts = c.execute('''
        SELECT a.*, u.name, u.email 
        FROM alerts a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.is_read = 0
        ORDER BY a.created_at DESC
        LIMIT 10
    ''').fetchall()
    
    c.close()
    return render_template("dashboard.html", users=users, alerts=alerts)

@app.route("/activity")
def activity():
    c = conn()
    logs = c.execute("""
        SELECT users.name, users.email, users.department, 
               user_activity.action, user_activity.timestamp,
               user_activity.ip_address, user_activity.user_agent
        FROM user_activity
        JOIN users ON users.user_id = user_activity.user_id
        ORDER BY user_activity.timestamp DESC
    """).fetchall()
    c.close()
    return render_template("activity.html", logs=logs)

@app.route("/alerts")
def view_alerts():
    c = conn()
    alerts = c.execute('''
        SELECT a.*, u.name, u.email, u.department
        FROM alerts a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.created_at DESC
    ''').fetchall()
    c.close()
    return render_template("alerts.html", alerts=alerts)

@app.route("/alert/<int:alert_id>/read", methods=["POST"])
def mark_alert_read(alert_id):
    c = conn()
    c.execute("UPDATE alerts SET is_read = 1 WHERE alert_id = ?", (alert_id,))
    c.commit()
    c.close()
    return {"success": True}

@app.route("/suspicious/<int:link_id>")
def suspicious_link(link_id):
    """Suspicious phishing link page"""
    return render_template("suspicious_login.html", link_id=link_id)

@app.route("/trusted/<int:link_id>")
def trusted_link(link_id):
    """Trusted safe link page"""
    return render_template("trusted.html", link_id=link_id)

@app.route("/capture", methods=["POST"])
def capture():
    email = request.form.get("email")
    password = request.form.get("password")  # In real scenario, don't store actual passwords
    link_id = request.form.get("link_id", "1")
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    c = conn()
    
    # Find user by email
    user = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    
    if user:
        # Log the activity
        action = "Clicked Phishing Link & Entered Credentials"
        c.execute("""
            INSERT INTO user_activity (user_id, action, ip_address, user_agent) 
            VALUES (?, ?, ?, ?)
        """, (user['user_id'], action, ip_address, user_agent))
        
        # Update risk score (increase by 40 for clicking phishing link)
        new_risk_score = user['risk_score'] + 40
        c.execute("UPDATE users SET risk_score = ? WHERE user_id = ?", 
                  (new_risk_score, user['user_id']))
        
        # Create alert
        alert_message = f"Employee clicked suspicious link and entered credentials. Risk score increased from {user['risk_score']} to {new_risk_score}."
        c.execute("""
            INSERT INTO alerts (user_id, alert_type, message, severity) 
            VALUES (?, ?, ?, ?)
        """, (user['user_id'], 'PHISHING_CLICK', alert_message, 'HIGH'))
        
        c.commit()
        
        # Prepare data for email alert
        user_data = {
            'name': user['name'],
            'email': user['email'],
            'department': user['department'],
            'role': user['role'],
            'manager_email': user['manager_email'],
            'risk_score': new_risk_score
        }
        
        action_details = {
            'action': action,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': ip_address,
            'user_agent': user_agent
        }
        
        # Send email alert to manager
        send_alert_email(user_data, action_details)
        
        c.close()
        
        return render_template("capture_result.html", 
                             success=False, 
                             user=user,
                             risk_increase=40,
                             new_score=new_risk_score)
    else:
        # Log unknown user attempt
        c.execute("""
            INSERT INTO user_activity (user_id, action, ip_address, user_agent) 
            VALUES (?, ?, ?, ?)
        """, (None, f"Unknown user attempted login with email: {email}", ip_address, user_agent))
        c.commit()
        c.close()
        
        return render_template("capture_result.html", 
                             success=False, 
                             unknown_email=email)

@app.route("/campaign")
def campaign():
    return render_template("campaign.html")

@app.route("/user/<int:user_id>")
def user_details(user_id):
    c = conn()
    user = c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    activities = c.execute("""
        SELECT * FROM user_activity 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    """, (user_id,)).fetchall()
    c.close()
    
    if user:
        return render_template("user_details.html", user=user, activities=activities)
    return "User not found", 404

@app.route("/reset_risk/<int:user_id>", methods=["POST"])
def reset_risk(user_id):
    c = conn()
    c.execute("UPDATE users SET risk_score = 0 WHERE user_id = ?", (user_id,))
    c.execute("""
        INSERT INTO alerts (user_id, alert_type, message, severity) 
        VALUES (?, 'RISK_RESET', 'Risk score reset to 0 after training', 'INFO')
    """, (user_id,))
    c.commit()
    c.close()
    return redirect(url_for('dashboard'))
@app.route("/trusted_capture", methods=["POST"])
def trusted_capture():
    email = request.form.get("email")
    password = request.form.get("password")
    link_id = request.form.get("link_id", "1")
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    print(f"Trusted link clicked - Email: {email}")
    
    c = conn()
    
    # Find user by email
    user = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    
    if user:
        # Log the activity
        action = f"Clicked Trusted Link & Completed Security Training (Link ID: {link_id})"
        c.execute("""
            INSERT INTO user_activity (user_id, action, ip_address, user_agent) 
            VALUES (?, ?, ?, ?)
        """, (user['user_id'], action, ip_address, user_agent))
        
        # DECREASE risk score by 20 for good security behavior
        old_risk_score = user['risk_score']
        new_risk_score = max(0, old_risk_score - 20)  # Don't go below 0
        c.execute("UPDATE users SET risk_score = ? WHERE user_id = ?", 
                  (new_risk_score, user['user_id']))
        
        # Create positive alert
        alert_message = f"✅ {user['name']} demonstrated good security awareness! Risk score decreased from {old_risk_score} to {new_risk_score}."
        c.execute("""
            INSERT INTO alerts (user_id, alert_type, message, severity) 
            VALUES (?, ?, ?, ?)
        """, (user['user_id'], 'GOOD_SECURITY', alert_message, 'INFO'))
        
        c.commit()
        c.close()
        
        return render_template("trusted_result.html", 
                             user=user,
                             risk_decrease=20,
                             new_score=new_risk_score,
                             email_provided=email)
    else:
        # Log unknown user
        c.execute("""
            INSERT INTO user_activity (user_id, action, ip_address, user_agent) 
            VALUES (?, ?, ?, ?)
        """, (None, f"Unknown user clicked trusted link with email: {email}", ip_address, user_agent))
        c.commit()
        c.close()
        
        return render_template("trusted_result.html", 
                             unknown_email=email)
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)True)
