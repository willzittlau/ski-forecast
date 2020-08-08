from flask_script import Manager
from app import app
from scripts import daily_weather

manager = Manager(app)

@manager.command
def save_to_db():
    daily_weather()

if __name__ == "__main__":
    manager.run()