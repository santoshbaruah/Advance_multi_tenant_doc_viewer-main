
## Prerequisites
- Amazon EC2 instance running Amazon Linux 2024.
- Access to AWS IAM credentials for S3 access.

---

## 1. EC2 Instance Setup

1. **Launch an Amazon Linux 2024 EC2 instance** and connect to it via SSH.
2. **Install Required Packages**:

    ```
    sudo yum update -y
    sudo yum install -y python3 python3-pip mysql-devel python3-devel gcc
    ```

3. **Clone Your Repository**:
   ```
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

## 2. Python Environment Setup

1. **Create and Activate a Virtual Environment**:

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install Python Packages**:

    ```
    pip install -r requirements.txt
    ```

## 3. Environment Variable Configuration

1. **Create a `.env` File**:
   
   In the root directory, create a `.env` file with the following configuration:

    ```dotenv
    SECRET_KEY=your-secret-key
    DATABASE_URL=mysql+pymysql://username:password@your-aurora-endpoint:3306/multi_tenant_db
    S3_BUCKET=your-tenant-assets
    AWS_ACCESS_KEY_ID=your-access-key-id
    AWS_SECRET_ACCESS_KEY=your-secret-access-key
    ```

2. **Generate a Secure SECRET_KEY**:
   
   Use this Python code to generate a random secret key:

    ```python
    import os
    print(os.urandom(24).hex())
    ```

   Replace `your-secret-key` in the `.env` file with the generated key.

3. **Database Connection URL**:
   
   Update the `DATABASE_URL` with your MySQL credentials and endpoint details.

## 4. Database Initialization

1. **Create the Initialization SQL Script**:

   Ensure the `sql/init_db.sql` file exists in the `sql` directory, with SQL commands to create tables, indexes, and any required sample data.

2. **Modify `run.py` for Database Initialization**:

   In `run.py`, add code to initialize the database with `init_db.sql`:

    ```python
    from app import create_app, db
    import os

    app = create_app()

    if __name__ == '__main__':
        with app.app_context():
            db.create_all()
            # Execute SQL initialization script
            with open('sql/init_db.sql', 'r') as f:
                sql_script = f.read()
            db.engine.execute(sql_script)
        app.run(debug=True)
    ```

---

## 5. AWS S3 and Flask Configuration

1. **Ensure AWS Credentials Are Correctly Configured**:

   - The `.env` file should include `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
   - Ensure your IAM user has the appropriate permissions to access the specified S3 bucket.

2. **Flask Configuration (`config.py`)**:

   Add the following code in `config.py` to load environment variables and set up Flask configuration:

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()

    class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        S3_BUCKET = os.environ.get('S3_BUCKET')
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    ```

---

## 6. Application Deployment

1. **Run the Flask Application**:

    ```bash
    python run.py
    ```

   This will start the Flask application on `http://127.0.0.1:5000` (adjust settings as needed for production).

---

## 7. Project Directory Structure

Your project structure should look like this:

```
.
├── .env
├── config.py
├── requirements.txt
├── run.py
├── sql/
│   └── init_db.sql
```

---

## 8. Detailed Steps

### SQL Initialization Script (sql/init_db.sql)
The `init_db.sql` script should contain SQL commands for setting up the necessary tables and inserting any default data.

### Frontend Interface
- **Login & Registration**: User authentication.
- **Document Upload**: Allows users to upload documents to the S3 bucket.
- **Dashboard**: Lists uploaded documents with previews.
- **Search**: Enables searching through documents in the database.

---

## Troubleshooting

- **Missing Environment Variables**: Verify the `.env` file for accurate configuration.
- **Database Errors**: Ensure the database server is accessible and credentials in `DATABASE_URL` are correct.
- **S3 Access Issues**: Confirm AWS IAM permissions and S3 bucket policies allow the required operations.

---
