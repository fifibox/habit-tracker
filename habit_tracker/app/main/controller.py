from habit_tracker.app.models import Habit, HabitRecord, User
from datetime import datetime, timedelta
import itsdangerous
from flask_mail import Message
from flask import current_app
from habit_tracker.app import db

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def create_default_habits(user_id):
    """Create default habits for new users"""
    # Default habit names
    default_habits = [
        "Wake up early",
        "Drink water",
        "No takeout",
        "Meditate"
    ]
    
    # Check if user already has habits
    existing_count = Habit.query.filter_by(user_id=user_id).count()
    if existing_count > 0:
        return  # User already has habits
    
    # Create default habits
    for habit_name in default_habits:
        habit = Habit(
            habit_name=habit_name,
            user_id=user_id
        )
        db.session.add(habit)
    
    db.session.commit()

def get_habit_color(habit_name):
    _last_color_index = -1
    """Return the CSS color class based on habit name"""
    colors = ["green", "red", "blue", "purple"]
    _last_color_index = (_last_color_index + 1) % 4
    return colors[_last_color_index]

def calculate_streak(user_id):
    """Calculate current streak for a user based on all habits being completed.

    Returns the number of consecutive days all habits were completed, starting from yesterday.
    """
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
   
    # Check if all habits for the user are completed today
    habits = Habit.query.filter_by(user_id=user_id).all()
    all_completed_today = all(
        HabitRecord.query.filter_by(
            habit_id=habit.id,
            date=today,
            completed=True
        ).first()
        for habit in habits
    )
    
    streak = 1 if all_completed_today else 0

    # Start streak calculation from yesterday
    current_date = yesterday

    while True:
        # Check if all habits for the user were completed on the current date
        habits = Habit.query.filter_by(user_id=user_id).all()
        all_completed = all(
            HabitRecord.query.filter_by(
                habit_id=habit.id,
                date=current_date,
                completed=True
            ).first()
            for habit in habits
        )
        
        if not all_completed:
            break  # Streak ends if any habit is not completed on the current date
        
        streak += 1
        current_date -= timedelta(days=1)  # Move to the previous day

    return streak

def get_weekly_completion(habit_id):
    """Get weekly completion data for a habit
    
    Returns tuple: (completed_days, total_days)
    """
    today = datetime.now().date()
    start_date = today - timedelta(days=6)  # Last 7 days including today
    
    # Get all habit records in date range
    records = HabitRecord.query.filter(
        HabitRecord.habit_id == habit_id,
        HabitRecord.date >= start_date,
        HabitRecord.date <= today,
        HabitRecord.completed == True
    ).all()
    
    completed_days = len(records)
    total_days = 7  # Last 7 days
    
    return (completed_days, total_days)

# generate reset token for forgot password
def generate_reset_token(user, expires_sec=1800):
    s = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(user.email, salt='password-reset-salt')

# verify reset token for forgot password
def verify_reset_token(token, expires_sec=1800):
    s = itsdangerous.URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expires_sec)
    except Exception:
        return None
    return User.query.filter_by(email=email).first()
