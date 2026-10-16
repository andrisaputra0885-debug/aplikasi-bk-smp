from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'bk-smp-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/bk_smp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# === MODELS (Struktur Database) ===
class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    jenis_kelamin = db.Column(db.String(1), nullable=False)

class KegiatanBK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    jenis = db.Column(db.String(20), nullable=False)
    kelas = db.Column(db.String(10))
    tanggal = db.Column(db.Date, nullable=False)
    waktu_mulai = db.Column(db.String(5))
    waktu_selesai = db.Column(db.String(5))
    ruang = db.Column(db.String(50))
    deskripsi = db.Column(db.Text)

class KonselingSiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    siswa_id = db.Column(db.Integer, db.ForeignKey('siswa.id'))
    nama_siswa = db.Column(db.String(100))
    tanggal = db.Column(db.Date, nullable=False)
    jenis_konseling = db.Column(db.String(20))
    masalah = db.Column(db.Text)
    hasil = db.Column(db.Text)
    tindak_lanjut = db.Column(db.Text)

class RPLBK(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    kelas = db.Column(db.String(10), nullable=False)
    jenis = db.Column(db.String(20))
    tahun_ajaran = db.Column(db.String(20))
    semester = db.Column(db.String(10))

# === ROUTES (Halaman Website) ===
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    total_siswa = Siswa.query.count()
    kegiatan_hari_ini = KegiatanBK.query.filter_by(tanggal=date.today()).count()
    jadwal_konseling = KegiatanBK.query.filter(KegiatanBK.tanggal >= date.today()).count()
    rpl_count = RPLBK.query.count()
    jadwal_hari_ini = KegiatanBK.query.filter_by(tanggal=date.today()).order_by(KegiatanBK.waktu_mulai).all()
    
    bulan_ini = datetime.now().month
    tahun_ini = datetime.now().year
    kegiatan_bulan = {
        'Klasikal': KegiatanBK.query.filter(db.extract('month', KegiatanBK.tanggal)==bulan_ini, db.extract('year', KegiatanBK.tanggal)==tahun_ini, KegiatanBK.jenis=='Klasikal').count(),
        'Individu': KegiatanBK.query.filter(db.extract('month', KegiatanBK.tanggal)==bulan_ini, db.extract('year', KegiatanBK.tanggal)==tahun_ini, KegiatanBK.jenis=='Individu').count(),
        'Kelompok': KegiatanBK.query.filter(db.extract('month', KegiatanBK.tanggal)==bulan_ini, db.extract('year', KegiatanBK.tanggal)==tahun_ini, KegiatanBK.jenis=='Kelompok').count(),
        'RPL': KegiatanBK.query.filter(db.extract('month', KegiatanBK.tanggal)==bulan_ini, db.extract('year', KegiatanBK.tanggal)==tahun_ini, KegiatanBK.jenis=='RPL').count()
    }
    
    siswa_per_kelas = {}
    for k in ['7A','7B','8A','8B','9A','9B']:
        siswa_per_kelas[k] = Siswa.query.filter_by(kelas=k).count()
        
    return render_template('dashboard.html', total_siswa=total_siswa, kegiatan_hari_ini=kegiatan_hari_ini, 
                         jadwal_konseling=jadwal_konseling, rpl_count=rpl_count, jadwal_hari_ini=jadwal_hari_ini, 
                         kegiatan_bulan=kegiatan_bulan, siswa_per_kelas=siswa_per_kelas)

@app.route('/data-siswa')
def data_siswa():
    kelas_filter = request.args.get('kelas', '')
    if kelas_filter:
        siswa_list = Siswa.query.filter_by(kelas=kelas_filter).order_by(Siswa.nama).all()
    else:
        siswa_list = Siswa.query.order_by(Siswa.kelas, Siswa.nama).all()
    kelas_list = sorted(set(s.kelas for s in Siswa.query.all()))
    return render_template('data_siswa.html', siswa_list=siswa_list, kelas_list=kelas_list, selected_kelas=kelas_filter)

@app.route('/api/siswa', methods=['POST'])
def tambah_siswa():
    data = request.json
    new_siswa = Siswa(nama=data['nama'], kelas=data['kelas'], jenis_kelamin=data['jenis_kelamin'])
    db.session.add(new_siswa)
    db.session.commit()
    return jsonify({'success': True, 'id': new_siswa.id})

@app.route('/api/siswa/<int:id>', methods=['PUT'])
def update_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    data = request.json
    siswa.nama = data['nama']
    siswa.kelas = data['kelas']
    siswa.jenis_kelamin = data['jenis_kelamin']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/siswa/<int:id>', methods=['DELETE'])
def hapus_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    db.session.delete(siswa)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/rpl-bk')
def rpl_bk():
    tahun_ajaran = request.args.get('tahun_ajaran', '2025/2026')
    semester = request.args.get('semester', 'Ganjil')
    rpl_list = RPLBK.query.filter_by(tahun_ajaran=tahun_ajaran, semester=semester).order_by(RPLBK.kelas).all()
    return render_template('rpl_bk.html', rpl_list=rpl_list, tahun_ajaran=tahun_ajaran, semester=semester)

@app.route('/api/rpl', methods=['POST'])
def tambah_rpl():
    data = request.json
    new_rpl = RPLBK(judul=data['judul'], kelas=data['kelas'], jenis=data.get('jenis','Klasikal'), tahun_ajaran=data['tahun_ajaran'], semester=data['semester'])
    db.session.add(new_rpl)
    db.session.commit()
    return jsonify({'success': True, 'id': new_rpl.id})

@app.route('/konseling')
def konseling():
    siswa_list = Siswa.query.order_by(Siswa.nama).all()
    riwayat = KonselingSiswa.query.order_by(KonselingSiswa.tanggal.desc()).limit(20).all()
    return render_template('konseling.html', siswa_list=siswa_list, riwayat=riwayat)

@app.route('/api/konseling', methods=['POST'])
def simpan_konseling():
    data = request.json
    new_k = KonselingSiswa(siswa_id=data.get('siswa_id'), nama_siswa=data['nama_siswa'], 
                          tanggal=datetime.strptime(data['tanggal'],'%Y-%m-%d').date(), 
                          jenis_konseling=data['jenis_konseling'], masalah=data['masalah'], 
                          hasil=data.get('hasil',''), tindak_lanjut=data.get('tindak_lanjut',''))
    db.session.add(new_k)
    db.session.commit()
    return jsonify({'success': True, 'id': new_k.id})

@app.route('/jadwal-bk')
def jadwal_bk():
    filter_jenis = request.args.get('jenis', '')
    if filter_jenis:
        jadwal_list = KegiatanBK.query.filter_by(jenis=filter_jenis).order_by(KegiatanBK.tanggal, KegiatanBK.waktu_mulai).all()
    else:
        jadwal_list = KegiatanBK.query.order_by(KegiatanBK.tanggal, KegiatanBK.waktu_mulai).all()
    return render_template('jadwal_bk.html', jadwal_list=jadwal_list, selected_jenis=filter_jenis)

@app.route('/api/jadwal', methods=['POST'])
def tambah_jadwal():
    data = request.json
    new_j = KegiatanBK(judul=data['judul'], jenis=data['jenis'], kelas=data.get('kelas',''), 
                      tanggal=datetime.strptime(data['tanggal'],'%Y-%m-%d').date(), 
                      waktu_mulai=data['waktu_mulai'], waktu_selesai=data['waktu_selesai'], 
                      ruang=data.get('ruang',''), deskripsi=data.get('deskripsi',''))
    db.session.add(new_j)
    db.session.commit()
    return jsonify({'success': True, 'id': new_j.id})

@app.route('/laporan')
def laporan():
    tahun_ajaran = request.args.get('tahun_ajaran', '2025/2026')
    bulan = request.args.get('bulan', str(datetime.now().month))
    kegiatan_per_jenis = {
        'Klasikal': KegiatanBK.query.filter(db.extract('month',KegiatanBK.tanggal)==int(bulan)).filter(KegiatanBK.jenis=='Klasikal').count(),
        'Individu': KegiatanBK.query.filter(db.extract('month',KegiatanBK.tanggal)==int(bulan)).filter(KegiatanBK.jenis=='Individu').count(),
        'Kelompok': KegiatanBK.query.filter(db.extract('month',KegiatanBK.tanggal)==int(bulan)).filter(KegiatanBK.jenis=='Kelompok').count(),
        'RPL': KegiatanBK.query.filter(db.extract('month',KegiatanBK.tanggal)==int(bulan)).filter(KegiatanBK.jenis=='RPL').count()
    }
    rekap_siswa = {}
    total = 0
    for k in ['7','8','9']:
        count = Siswa.query.filter(Siswa.kelas.like(k+'%')).count()
        rekap_siswa['Kelas '+k] = count
        total += count
    rekap_siswa['Total'] = total
    return render_template('laporan.html', kegiatan_per_jenis=kegiatan_per_jenis, rekap_siswa=rekap_siswa, tahun_ajaran=tahun_ajaran, bulan=bulan)

@app.route('/cetak-dokumen')
def cetak_dokumen():
    return render_template('cetak_dokumen.html')

@app.route('/administrasi-bk')
def administrasi_bk():
    return render_template('administrasi_bk.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)