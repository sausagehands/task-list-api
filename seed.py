from app import create_app
from app.models.task import Task
from app.models.goal import Goal
from app.db import db
from datetime import datetime
from dotenv import load_dotenv

app = create_app()

with app.app_context():
    print("Clearing existing data...")
    # Delete all existing data
    Task.query.delete()
    Goal.query.delete()
    db.session.commit()
    
    print("Creating goals...")
    # Create goals
    goal1 = Goal(title="Get Fit")
    goal2 = Goal(title="Learn Python")
    goal3 = Goal(title="Travel More")
    
    db.session.add_all([goal1, goal2, goal3])
    db.session.commit()
    
    print("Creating tasks...")
    # Tasks for "Get Fit" goal
    task1 = Task(
        title="Run 5k 🏃",
        description="Morning run in the park",
        goal_id=goal1.id
    )
    task2 = Task(
        title="Do 50 pushups 💪",
        description="Daily strength training",
        goal_id=goal1.id,
        completed_at=datetime.now()  # This one is complete
    )
    task3 = Task(
        title="Eat healthy meals 🥗",
        description="Meal prep on Sundays",
        goal_id=goal1.id
    )
    
    # Tasks for "Learn Python" goal
    task4 = Task(
        title="Build a Flask API 💻",
        description="Complete task list project",
        goal_id=goal2.id
    )
    task5 = Task(
        title="Read Python docs 📚",
        description="Study advanced topics",
        goal_id=goal2.id
    )
    task6 = Task(
        title="Practice algorithms 🧠",
        description="Solve coding challenges",
        goal_id=goal2.id,
        completed_at=datetime.now()  # This one is complete
    )
    
    # Tasks for "Travel More" goal
    task7 = Task(
        title="Book flight to Japan ✈️",
        description="Research dates and prices",
        goal_id=goal3.id
    )
    task8 = Task(
        title="Learn basic Japanese 🇯🇵",
        description="Common phrases and etiquette",
        goal_id=goal3.id
    )
    
    # Tasks without a goal
    task9 = Task(
        title="Call dentist 🦷",
        description="Schedule cleaning appointment"
    )
    task10 = Task(
        title="Pay utility bills 💸",
        description="Due by end of month"
    )
    task11 = Task(
        title="Water plants 🌱",
        description="Check soil moisture first",
        completed_at=datetime.now()  # This one is complete
    )
    
    db.session.add_all([
        task1, task2, task3, task4, task5, task6,
        task7, task8, task9, task10, task11
    ])
    db.session.commit()
    
    print("✅ Database seeded successfully!")
    print(f"   Created {Goal.query.count()} goals")
    print(f"   Created {Task.query.count()} tasks")
    print(f"   - {Task.query.filter(Task.completed_at.isnot(None)).count()} completed")
    print(f"   - {Task.query.filter(Task.goal_id.isnot(None)).count()} assigned to goals")