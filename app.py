from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Doctor, Patient, MedicalRecord
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tan_tung_trung_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/hospital_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- TRANG CHỦ: Hàng đợi hôm nay ---
@app.route('/')
def index():
    if 'doctor_id' not in session: return redirect(url_for('login'))
    today = datetime.now().date()
    
    # Lấy bệnh nhân hẹn khám "hôm nay" VÀ trạng thái là "Chờ khám"
    records = db.session.query(MedicalRecord, Patient).\
              join(Patient, MedicalRecord.Patient_id == Patient.Patient_id).\
              filter(MedicalRecord.Visit_date == today, MedicalRecord.Status == 'Chờ khám').all()
    return render_template('index.html', records=records)

# --- ĐĂNG NHẬP ---
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

# --- QUẢN LÝ BỆNH NHÂN (Thêm mới, Đặt lịch hẹn, Tìm kiếm) ---
@app.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    if 'doctor_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 1. Tạo thông tin Bệnh nhân trước
        new_p = Patient(
            Full_name=request.form.get('fullname'),
            Dob=request.form.get('dob') or None,
            Gender=request.form.get('gender'),
            Phone=request.form.get('phone'),
            Address=request.form.get('address')
        )
        db.session.add(new_p)
        db.session.flush() 
        
        # 2. Xử lý logic ĐẶT LỊCH
        visit_date_str = request.form.get('visit_date')
        if visit_date_str:
            visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        else:
            visit_date = datetime.now().date()
            
        symptoms = request.form.get('symptoms', 'Chưa ghi nhận')
        
        # 3. Đẩy vào bảng MedicalRecords với trạng thái Chờ khám
        new_record = MedicalRecord(
            Patient_id=new_p.Patient_id,
            Doctor_id=session['doctor_id'],
            Visit_date=visit_date,
            Symptoms=symptoms,
            Status='Chờ khám'
        )
        db.session.add(new_record)
        db.session.commit()
        
        flash(f'Đã đặt lịch thành công vào ngày {visit_date.strftime("%d/%m/%Y")}!', 'success')
        return redirect(url_for('manage_patients'))
    
    # Code tìm kiếm
    search_query = request.args.get('q', '')
    if search_query:
        all_patients = Patient.query.filter(
            (Patient.Full_name.contains(search_query)) | 
            (Patient.Phone.contains(search_query))
        ).all()
    else:
        all_patients = Patient.query.all()
        
    return render_template('patients.html', patients=all_patients, search_query=search_query)

# --- CHỨC NĂNG TỪ APP1: Đưa bệnh nhân cũ vào hàng đợi hôm nay ---
@app.route('/add_to_queue/<int:patient_id>')
def add_to_queue(patient_id):
    if 'doctor_id' not in session: return redirect(url_for('login'))
    
    today = datetime.now().date()
    # Thêm điều kiện Status='Chờ khám' để tránh báo lỗi nếu họ đã khám xong trong cùng ngày
    existing_record = MedicalRecord.query.filter_by(Patient_id=patient_id, Visit_date=today, Status='Chờ khám').first()
    
    if existing_record:
        flash('Bệnh nhân này đang có mặt trong hàng đợi hôm nay rồi!', 'warning')
    else:
        new_record = MedicalRecord(
            Patient_id=patient_id,
            Doctor_id=session['doctor_id'],
            Visit_date=today,
            Symptoms='Chưa ghi nhận',
            Status='Chờ khám' # Bắt buộc phải có để hiện lên trang chủ
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Đã thêm bệnh nhân cũ vào hàng đợi khám thành công!', 'success')
        
    return redirect(url_for('index'))

# --- CHỨC NĂNG TỪ APP1: Sửa thông tin bệnh nhân ---
@app.route('/edit_patient/<int:patient_id>', methods=['POST'])
def edit_patient(patient_id):
    if 'doctor_id' not in session: return redirect(url_for('login'))
    
    patient = Patient.query.get_or_404(patient_id)
    patient.Full_name = request.form.get('fullname')
    
    dob = request.form.get('dob')
    if dob: patient.Dob = dob
        
    patient.Gender = request.form.get('gender')
    patient.Phone = request.form.get('phone')
    patient.Address = request.form.get('address')
    
    db.session.commit()
    flash('Đã cập nhật thông tin bệnh nhân thành công!', 'success')
    return redirect(url_for('manage_patients'))

# --- THỰC HIỆN KHÁM ---
@app.route('/examine/<int:record_id>', methods=['POST'])
def examine(record_id):
    if 'doctor_id' not in session: return redirect(url_for('login'))
    
    record = MedicalRecord.query.get_or_404(record_id)
    record.Symptoms = request.form.get('symptoms')
    record.Diagnosis = request.form.get('diagnosis')
    record.Treatment = request.form.get('treatment')
    record.Status = 'Đã khám'  # Cập nhật thành Đã khám để ẩn khỏi hàng chờ
    
    db.session.commit()
    flash('Đã lưu kết quả! Bệnh nhân đã rời hàng chờ.', 'success')
    return redirect(url_for('index'))

# --- LỊCH SỬ KHÁM ---
@app.route('/history/<int:patient_id>')
def view_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    history = MedicalRecord.query.filter_by(Patient_id=patient_id).order_by(MedicalRecord.Visit_date.desc()).all()
    return render_template('history.html', patient=patient, history=history)

# --- THOÁT ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)