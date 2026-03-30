from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Doctor, Patient, MedicalRecord
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tan_tung_trung_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/hospital_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- 1. TRANG CHỦ: Hàng đợi của bác sĩ ---
@app.route('/')
def index():
    if 'doctor_id' not in session: return redirect(url_for('login'))
    
    date_str = request.args.get('date')
    display_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date()

    records = db.session.query(MedicalRecord, Patient).\
              join(Patient, MedicalRecord.Patient_id == Patient.Patient_id).\
              filter(
                  MedicalRecord.Visit_date == display_date, 
                  MedicalRecord.Status == 'Chờ khám',
                  MedicalRecord.Doctor_id == session['doctor_id']
              ).all()
    return render_template('index.html', records=records, display_date=display_date)

# --- 2. ĐĂNG NHẬP ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        acc = request.form.get('account')
        pw = request.form.get('password')
        doctor = Doctor.query.filter_by(Account=acc).first()
        if doctor and doctor.Password == pw:
            session['doctor_id'] = doctor.Doctor_id
            session['doctor_name'] = doctor.Full_name
            return redirect(url_for('index'))
        flash('Sai tài khoản hoặc mật khẩu!', 'danger')
    return render_template('login.html')

# --- 3. QUẢN LÝ BỆNH NHÂN (Thêm mới & Tìm kiếm) ---
@app.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    if 'doctor_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        selected_doc_id = request.form.get('doctor_id')
        if not selected_doc_id:
            flash('Vui lòng chọn bác sĩ khám!', 'danger')
            return redirect(url_for('manage_patients'))

        new_p = Patient(
            Full_name=request.form.get('fullname'),
            Dob=request.form.get('dob') or None,
            Gender=request.form.get('gender'),
            Phone=request.form.get('phone'),
            Address=request.form.get('address')
        )
        db.session.add(new_p)
        db.session.flush() 
        
        visit_date_str = request.form.get('visit_date')
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date() if visit_date_str else datetime.now().date()
        
        new_record = MedicalRecord(
            Patient_id=new_p.Patient_id,
            Doctor_id=selected_doc_id, 
            Visit_date=visit_date,
            Symptoms=request.form.get('symptoms', 'Chưa ghi nhận'),
            Status='Chờ khám'
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Đã thêm bệnh nhân và đặt lịch thành công!', 'success')
        return redirect(url_for('manage_patients'))
    
    all_doctors = Doctor.query.all()
    search_query = request.args.get('q', '')
    if search_query:
        all_patients = Patient.query.filter(Patient.Full_name.contains(search_query)).all()
    else:
        all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients, doctors=all_doctors, search_query=search_query)

# --- 4. NÚT KHÁM NAY: Đưa bệnh nhân cũ vào hàng đợi ---
@app.route('/add_to_queue/<int:patient_id>')
def add_to_queue(patient_id):
    if 'doctor_id' not in session: return redirect(url_for('login'))
    today = datetime.now().date()
    
    # Kiểm tra xem hôm nay bác sĩ này đã đăng ký cho bệnh nhân này chưa
    existing = MedicalRecord.query.filter_by(Patient_id=patient_id, Doctor_id=session['doctor_id'], Visit_date=today, Status='Chờ khám').first()
    if existing:
        flash('Bệnh nhân này đã có trong hàng đợi của bạn hôm nay!', 'warning')
    else:
        new_record = MedicalRecord(
            Patient_id=patient_id,
            Doctor_id=session['doctor_id'],
            Visit_date=today,
            Symptoms='Tái khám/Khám trực tiếp',
            Status='Chờ khám'
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Đã đưa bệnh nhân vào hàng đợi khám!', 'success')
    return redirect(url_for('index'))

# --- 5. NÚT LỊCH SỬ: Xem lại các lần khám ---
@app.route('/history/<int:patient_id>')
def view_history(patient_id):
    if 'doctor_id' not in session: return redirect(url_for('login'))
    patient = Patient.query.get_or_404(patient_id)
    # Lấy tất cả hồ sơ, ưu tiên ngày mới nhất lên đầu
    history = MedicalRecord.query.filter_by(Patient_id=patient_id).order_by(MedicalRecord.Visit_date.desc()).all()
    return render_template('history.html', patient=patient, history=history)

# --- 6. KHÁM BỆNH: Lưu kết quả ---
@app.route('/examine/<int:record_id>', methods=['POST'])
def examine(record_id):
    if 'doctor_id' not in session: return redirect(url_for('login'))
    record = MedicalRecord.query.get_or_404(record_id)
    record.Symptoms = request.form.get('symptoms')
    record.Diagnosis = request.form.get('diagnosis')
    record.Treatment = request.form.get('treatment')
    record.Status = 'Đã khám' 
    db.session.commit()
    flash('Đã hoàn thành ca khám!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)