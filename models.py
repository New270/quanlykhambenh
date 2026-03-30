from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 1. Lớp bác sĩ
class Doctor(db.Model):
    __tablename__ = 'Doctors'
    Doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Full_name = db.Column(db.String(255), nullable=False)
    Specialization = db.Column(db.String(255), nullable=False)
    Account = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

# 2. Lớp bệnh nhân
class Patient(db.Model):
    __tablename__ = 'Patients'
    Patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Full_name = db.Column(db.String(255), nullable=False)
    Dob = db.Column(db.Date)
    Gender = db.Column(db.String(10), nullable=False)
    Phone = db.Column(db.String(20))
    Address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

# 3. Lớp hồ sơ khám bệnh
class MedicalRecord(db.Model):
    __tablename__ = 'MedicalRecords'
    Record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Patient_id = db.Column(db.Integer, db.ForeignKey('Patients.Patient_id'), nullable=False)
    Doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.Doctor_id'), nullable=False)
    Visit_date = db.Column(db.Date, default=datetime.now)
    Symptoms = db.Column(db.Text)
    Diagnosis = db.Column(db.Text)
    Treatment = db.Column(db.Text)
    Notes = db.Column(db.Text)
    Status = db.Column(db.String(50), default='Chờ khám')
    created_at = db.Column(db.DateTime, default=datetime.now)