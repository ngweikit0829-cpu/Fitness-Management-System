# Fitness Management Web System

A Python web application for fitness and health management. It calculates body metrics and daily nutrition targets, recommends meals, provides an exercise library, tracks daily workouts and health logs, shows progress charts, and exports PDF reports.

Project for the Python Programming course, New Era Institute of Vocational & Continuing Education.

<img width="940" height="364" alt="image-3" src="https://github.com/user-attachments/assets/bcc5e878-922e-48bd-b488-a01f6914fc91" />
<img width="940" height="400" alt="image-4" src="https://github.com/user-attachments/assets/af5d1582-f45a-49a5-ac64-3872de014ff5" />

## Features

### User accounts and profile
- Registration and login with **hashed passwords** (no plain-text storage)
- Profile with gender, age, height, weight, activity level and fitness goal (fat loss, maintenance, muscle gain)
- Each user can only see and manage their own logs and reports

### Body metrics and nutrition engine
- **BMI** calculation with a health category
- **BMR** using the Mifflin-St Jeor formula
- **TDEE** using an activity factor between 1.2 and 1.9
- Daily calorie target based on the goal, with protein, carbohydrate and fat targets in grams

| Goal | Daily calorie target |
| --- | --- |
| Fat loss | TDEE - 500 kcal |
| Maintenance | TDEE |
| Muscle gain | TDEE + 300 kcal |

### Smart diet recommendation
- Splits the daily calorie target across breakfast (25%), lunch (40%) and dinner (35%) and matches meals from the food database
- Food search showing calories, protein, carbohydrates and fat

### Exercise library
- Filter by muscle group: chest, back, legs, shoulders, arms, core
- Each exercise has recommended sets and reps, steps and safety notes

### Daily log
- Record workouts (muscle group, exercise, sets, weight, duration)
- Daily health check-in with body weight and water intake

### Analytics dashboard
- Weight and BMI trend charts, hand-drawn with native **SVG and JavaScript** (no charting library)
- Monthly training frequency

### PDF report export
- Generate a report for the last 7 or 30 days, including metrics summary, weight chart, nutrition advice and training completion

### Data validation and security
- Input limits for height, weight and age to prevent invalid or extreme values
- Parameterized queries to prevent SQL injection

## Tech Stack

- **Language:** Python
- **Web framework:** Flask (with Werkzeug)
- **Database:** MySQL, accessed with PyMySQL
- **Frontend:** HTML, CSS, JavaScript, charts drawn with native SVG
- **PDF generation:** ReportLab

## Project Structure

| Path | Purpose |
| --- | --- |
| `app.py` | Flask application: routes, calculations, database access and PDF export |
| `templates/` | HTML templates |
| `static/` | CSS, JavaScript and images |
| `database/` | MySQL setup script |
| `requirements.txt` | Python dependencies |

## Getting Started

### Requirements

- Python 3.8 or later
- A running MySQL server

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ngweikit0829-cpu/Fitness-Management-System.git
   cd Fitness-Management-System
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a MySQL database and import the `.sql` file in the `database/` folder.
4. Open `app.py` and set the MySQL host, database name, username and password to match your setup.
5. Run the app:
   ```bash
   python app.py
   ```
6. Open the address shown in the terminal in your browser (Flask usually uses `http://127.0.0.1:5000`).

## Author

**Ng Wei Kit**
