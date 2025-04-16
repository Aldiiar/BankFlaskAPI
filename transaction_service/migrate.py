import os
from app import create_app
from flask_migrate import upgrade, migrate, init

app = create_app()

migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')

if not os.path.exists(migrations_dir):
    with app.app_context():
        init(directory=migrations_dir)
        migrate(directory=migrations_dir)
        upgrade(directory=migrations_dir)
        print("Миграции завершены!")
else:
    with app.app_context():
        migrate(directory=migrations_dir)
        upgrade(directory=migrations_dir)
        print("Миграции завершены!")
