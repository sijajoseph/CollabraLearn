
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "5244716f129015789646146459b3edfebd2605e849aeca80385936e06a227600")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/sijaj/Documents/MyStudyCircleInstance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
