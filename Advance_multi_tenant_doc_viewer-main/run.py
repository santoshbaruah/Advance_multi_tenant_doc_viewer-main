from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Optionally, you can execute the SQL script to initialize the database
        with open('sql/init_db.sql', 'r') as f:
            sql_script = f.read()
        db.engine.execute(sql_script)
    app.run(debug=True)
