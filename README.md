# AI Cyber Awareness Platform

## Overview

AI Cyber Awareness Platform is a cybersecurity web application that helps organizations detect phishing attacks and improve employee security awareness. The system monitors when employees interact with suspicious links and warns the organization about potential security risks.

## How the Project Works

In an organization, employees may accidentally enter company credentials into phishing websites. This platform detects such activity and analyzes the link to determine whether it is safe or risky.

If an employee enters company details in a phishing link, the system:

1. Detects the suspicious link.
2. Generates a risk score based on the threat level.
3. Displays a warning that the link is risky.
4. Sends an alert to the manager dashboard indicating that an employee attempted to log in through a suspicious link.

This helps organizations identify phishing attacks early and prevent data breaches.

## Features

* Phishing link detection
* Risk score calculation
* Manager dashboard alerts
* Employee security monitoring
* Cybersecurity awareness system

## Project Structure

instance/ – Application instance folder
templates/ – HTML pages for the web interface
.env – Environment configuration file
app.py – Main Flask application
database.db – Database for storing user and alert data
requirements.txt – Python dependencies

## Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* SQLite Database

## Goal

The goal of this project is to help organizations detect phishing attacks quickly and improve employee cybersecurity awareness.

## Future Improvements

* Email phishing detection
* Real-time security alerts
* Advanced AI-based threat detection
