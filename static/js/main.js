// === FUNGSI UTAMA (UTILITIES) ===
function showToast(message, type) {
    type = type || 'success';
    var toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(function() { toast.classList.add('show'); }, 10);
    setTimeout(function() {
        toast.classList.remove('show');
        setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Tutup modal jika klik di area gelap luar modal
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// Toggle Sidebar untuk HP
var menuToggle = document.querySelector('.menu-toggle');
var sidebar = document.querySelector('.sidebar');
if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });
}

// === DATA SISWA ===
async function tambahSiswa() {
    var nama = document.getElementById('siswa_nama').value.trim();
    var kelas = document.getElementById('siswa_kelas').value;
    var jk = document.getElementById('siswa_jk').value;
    if (!nama || !kelas || !jk) { showToast('Semua field harus diisi!', 'error'); return; }
    
    try {
        var res = await fetch('/api/siswa', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({nama: nama, kelas: kelas, jenis_kelamin: jk}) 
        });
        var data = await res.json();
        if (data.success) { 
            showToast('Siswa berhasil ditambahkan!'); 
            closeModal('modalTambahSiswa'); 
            setTimeout(function() { location.reload(); }, 1000); 
        }
    } catch(e) { showToast('Terjadi kesalahan!', 'error'); }
}

async function editSiswa(id) {
    var row = document.querySelector('tr[data-id="' + id + '"]');
    var cells = row.querySelectorAll('td');
    document.getElementById('edit_siswa_id').value = id;
    document.getElementById('edit_siswa_nama').value = cells[1].textContent;
    document.getElementById('edit_siswa_kelas').value = cells[2].textContent;
    document.getElementById('edit_siswa_jk').value = cells[3].textContent;
    openModal('modalEditSiswa');
}

async function simpanEditSiswa() {
    var id = document.getElementById('edit_siswa_id').value;
    var nama = document.getElementById('edit_siswa_nama').value.trim();
    var kelas = document.getElementById('edit_siswa_kelas').value;
    var jk = document.getElementById('edit_siswa_jk').value;
    
    try {
        var res = await fetch('/api/siswa/' + id, { 
            method: 'PUT', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({nama: nama, kelas: kelas, jenis_kelamin: jk}) 
        });
        var data = await res.json();
        if (data.success) { 
            showToast('Data berhasil diupdate!'); 
            closeModal('modalEditSiswa'); 
            setTimeout(function() { location.reload(); }, 1000); 
        }
    } catch(e) { showToast('Terjadi kesalahan!', 'error'); }
}

async function hapusSiswa(id) {
    if (!confirm('Yakin ingin menghapus data siswa ini?')) return;
    try {
        var res = await fetch('/api/siswa/' + id, { method: 'DELETE' });
        var data = await res.json();
        if (data.success) { 
            showToast('Siswa berhasil dihapus!'); 
            setTimeout(function() { location.reload(); }, 1000); 
        }
    } catch(e) { showToast('Terjadi kesalahan!', 'error'); }
}

function filterKelas(kelas) { window.location.href = '/data-siswa?kelas=' + kelas; }

function searchSiswa(query) {
    var rows = document.querySelectorAll('.data-table tbody tr');
    query = query.toLowerCase();
    rows.forEach(function(row) {
        var nama = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        row.style.display = nama.includes(query) ? '' : 'none';
    });
}

// === RPL BK ===
async function tambahRPL() {
    var judul = document.getElementById('rpl_judul').value.trim();
    var kelas = document.getElementById('rpl_kelas').value;
    var jenis = document.getElementById('rpl_jenis').value;
    var tahun = document.getElementById('rpl_tahun').value;
    var semester = document.getElementById('rpl_semester').value;
    if (!judul || !kelas) { showToast('Judul dan Kelas harus diisi!', 'error'); return; }
    
    try {
        var res = await fetch('/api/rpl', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({judul: judul, kelas: kelas, jenis: jenis, tahun_ajaran: tahun, semester: semester}) 
        });
        var data = await res.json();
        if (data.success) { 
            showToast('RPL BK berhasil ditambahkan!'); 
            closeModal('modalTambahRPL'); 
            setTimeout(function() { location.reload(); }, 1000); 
        }
    } catch(e) { showToast('Terjadi kesalahan!', 'error'); }
}

// === KONSELING ===
async function simpanKonseling() {
    var siswaEl = document.getElementById('konseling_siswa');
    var siswa_id = siswaEl.value;
    var nama_siswa = siswaEl.options[siswaEl.selectedIndex] ? siswaEl.options[siswaEl.selectedIndex].text : '';
    var tanggal = document.getElementById('konseling_tanggal').value;
    var jenis = document.getElementById('konseling_jenis').value;
    var masalah = document.getElementById('konseling_masalah').value.trim();
    var hasil = document.getElementById('konseling_hasil').value.trim();
    var tindak = document.getElementById('konseling_tindak').value.trim();
    
    if (!tanggal || !masalah) { showToast('Tanggal dan Masalah harus diisi!', 'error'); return; }
    
    try {
        var res = await fetch('/api/konseling', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({
                siswa_id: parseInt(siswa_id) || null, 
                nama_siswa: nama_siswa, 
                tanggal: tanggal, 
                jenis_konseling: jenis, 
                masalah: masalah, 
                hasil: hasil, 
                tindak_lanjut: tindak
            }) 
        });
        var data = await res.json();
        if (data.success) { 
            showToast('Catatan konseling berhasil disimpan!'); 
            document.getElementById('konseling_tanggal').value=''; 
            document.getElementById('konseling_masalah').value=''; 
            document.getElementById('konseling_hasil').value=''; 
            document.getElementById('konseling_tindak').value=''; 
        }
    } catch(e) { showToast('Terjadi kesalahan!', 'error'); }
}

// === JADWAL BK ===
async function tambahJadwal() {
    var judul = document.getElementById('jadwal_judul').value.trim();
    var jenis = document.getElementById('jadwal_jenis').value;
    var kelas = document.getElementById('jadwal_kelas').value;
    var tanggal = document.getElementById('jadwal_tanggal').value;
    var wm = document.getElementById('jadwal_waktu_mulai').value;
    var ws = document.getElementById('jadwal_waktu_selesai').value;
    var ruang = document.getElementById('jadwal_ruang').value.trim();
    var desk = document.getElementById('jadwal_deskripsi').value.trim();
    
    if (!judul || !tanggal || !wm || !ws) { showToast('Field wajib harus diisi!', 'error'); return; }
    
    try {
        var res = await fetch('/api/jadwal', { 
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify({
                judul: judul, jenis: jenis, kelas: kelas, tanggal: tanggal, 
                waktu_mulai: wm, waktu_selesai: ws, ruang: ruang, deskripsi: desk
            }) 
        });
        var data = await res.json();
        if (data.success) { 
            showToast('Jadwal berhasil ditambahkan!'); 
            closeModal('modalTambahJadwal'); 
            setTimeout(function() { location.reload(); }, 1000); 
        }
    } catch(e) { showToast('Terjadi kesalahan!', 'error'); }
}

function filterJadwal(jenis) { window.location.href = '/jadwal-bk?jenis=' + jenis; }

// === CHART SEDERHANA ===
function renderBarChart(containerId, data) {
    var container = document.getElementById(containerId);
    if (!container) return;
    var values = [];
    for (var k in data) { values.push(data[k]); }
    var maxVal = Math.max.apply(null, values.concat([1]));
    container.innerHTML = '';
    for (var label in data) {
        var group = document.createElement('div');
        group.className = 'chart-bar-group';
        var bar = document.createElement('div');
        bar.className = 'chart-bar ' + label.toLowerCase();
        bar.style.height = ((data[label] / maxVal) * 150) + 'px';
        bar.title = label + ': ' + data[label];
        var lbl = document.createElement('span');
        lbl.className = 'chart-label';
        lbl.textContent = label;
        group.appendChild(bar);
        group.appendChild(lbl);
        container.appendChild(group);
    }
}

// Jalankan chart saat halaman dashboard dimuat
document.addEventListener('DOMContentLoaded', function() {
    var chartData = document.getElementById('chartData');
    if (chartData) {
        var data = JSON.parse(chartData.textContent);
        renderBarChart('activityChart', data);
    }
});