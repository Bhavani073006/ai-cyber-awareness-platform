# An AI-Driven Social Engineering Attack Simulation and Employee Cybersecurity Awareness Enhancement Framework for Modern Organizations

## Overview

This project is a cybersecurity web application designed to simulate social engineering attacks and improve employee cybersecurity awareness within organizations. The system helps detect when employees interact with suspicious or phishing links and provides alerts to administrators or managers.

The platform analyzes user activity and generates a **risk score** when employees enter sensitive company information into potentially harmful links. This helps organizations identify vulnerabilities and prevent data breaches caused by social engineering attacks.

## Features

* Phishing link detection
* Employee interaction monitoring
* Risk score generation for suspicious activities
* Alerts for risky login attempts
* Cybersecurity awareness improvement
* Simple dashboard for monitoring activity

## How the System Works

1. Employees access links during their work activities.
2. If a user enters company credentials into a suspicious or phishing link, the system analyzes the link.
3. The system evaluates the threat level and calculates a **risk score**.
4. If the link is considered dangerous, the system flags it as a **risk link**.
5. Alerts are generated so managers can monitor and take action.

## Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* SQLite Database

## Project Structure

```
project-folder/
│
├── app.py            # Main Flask application
├── database.db       # SQLite database storing user and risk data
├── requirements.txt  # Project dependencies
├── .env              # Environment variables
│
├── instance/         # Flask instance configuration
│
└── templates/        # HTML templates for web pages
```

## Installation & Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

## Run the Application

Open the application in your browser:

🔗 [**[Open Application](http://localhost:5000)**](https://ai-cyber-awareness-platform-9hxx.onrender.com)

## Future Improvements

* AI-based phishing detection model
* Real-time attack monitoring dashboard
* Email phishing detection
* Employee cybersecurity training modules
* Advanced threat analytics

## Goal

The goal of this project is to help organizations detect social engineering attacks early and improve employee cybersecurity awareness using AI-driven monitoring and risk analysis.
