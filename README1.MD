Multi-Tenant Document Management System
This README provides instructions for setting up, configuring, and deploying the Multi-Tenant Document Management System.
Configuration and Deployment

1. Set up an EC2 instance with Amazon Linux 2023
Sign in to the AWS Management Console.
Navigate to EC2 and launch a new instance.
Choose Amazon Linux 2023 as the AMI.
Configure instance details, add storage, and configure security group.
Create or select an existing key pair for SSH access.

2. Connect to your EC2 instance
Use SSH to connect to your EC2 instance:

ssh -i /path/to/your-key-pair.pem ec2-user@your-instance-public-dns

3. Install required packages
Update the system and install necessary packages:

sudo yum update -y
sudo yum install -y python3 python3-pip mysql-devel python3-devel gcc

4. Clone the repository
Clone your project repository to the EC2 instance:

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

5. Set up a virtual environment
Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

6. Install Python packages
Install the required Python packages:

pip install -r requirements.txt

7. Set up environment variables
Create a .env file in the project root directory:
text
touch .env

Add the following content to the .env file, replacing placeholders with your actual values:

SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@your-aurora-endpoint:3306/multi_tenant_db
S3_BUCKET=your-tenant-assets
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key

8. Initialize the database
Ensure you have the sql/init_db.sql file in your project directory. The run.py script will automatically execute this SQL script to initialize the database.

9. Configure the application
Update config.py to use the environment variables:
python
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

10. Run the application
Start the Flask application:

python run.py

The application will be accessible at http://your-ec2-public-dns:5000.

Additional Configuration

Database Initialization
The run.py script includes code to automatically initialize the database using the sql/init_db.sql script:
python
with app.app_context():
    db.create_all()
    with open('sql/init_db.sql', 'r') as f:
        sql_script = f.read()
    db.engine.execute(sql_script)

AWS Credentials
Ensure your AWS credentials are correctly configured in the .env file for S3 access.

Flask Configuration
The Flask application is configured to use the environment variables set in the .env file through the config.py file.

Deployment Notes
Ensure all necessary ports are open in your EC2 instance's security group.

For production deployment, consider using a WSGI server like Gunicorn and a reverse proxy like Nginx.
Set up SSL/TLS for secure HTTPS connections in a production environment.

Troubleshooting

If you encounter database connection issues, verify your RDS endpoint and credentials.
For S3 access problems, check your AWS credentials and bucket permissions.
If the application fails to start, check the Flask logs for error messages.
