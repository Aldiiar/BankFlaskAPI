import os
from app import create_app
from flask_migrate import upgrade, migrate, init

# Инициализация приложения
app = create_app()

migrations_dir = 'migrations'

if not os.path.exists(migrations_dir):
    with app.app_context():
        init()
        migrate()
        upgrade()
        print("Миграции завершены!")
else:
    with app.app_context():
        migrate()
        upgrade()
        print("Миграции завершены!")