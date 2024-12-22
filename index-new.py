import streamlit as st
import cloudinary
import cloudinary.uploader
import mysql.connector
import pandas as pd

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name='dopcryjje',
    api_key='517418157241333',
    api_secret='-D8pHN6k55f8rAfmgjnESATQcAs'
)

# Fungsi untuk menghubungkan ke database
def create_db_connection():
    return mysql.connector.connect(
        host="154.26.133.67",
        user="remotex",
        password="84pUcAHV",
        database="DUDI"
    )

# Fungsi untuk meng-upload gambar ke Cloudinary
def upload_to_cloudinary(image_file):
    try:
        upload_result = cloudinary.uploader.upload(image_file)
        return upload_result['url']
    except Exception as e:
        st.error(f"Terjadi kesalahan saat meng-upload gambar: {e}")
        return None

# Fungsi untuk menyimpan data ke database
def save_data_to_db(new_data):
    conn = create_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO data_peserta 
        (NIK, Nama, Alamat, Kabupaten, Jenis_Kelamin, Pendidikan_Terakhir, Nomor_Tlp,
        Pertanyaan11, Pertanyaan12, Pertanyaan13, Pertanyaan21, Pertanyaan22,
        Pertanyaan31, Pertanyaan32, Pertanyaan33, Pertanyaan34, Pertanyaan35, Pertanyaan36,
        Pertanyaan41, Pertanyaan42, Pertanyaan43, Pertanyaan44, Pertanyaan51, Pertanyaan52,
        Pertanyaan53, Pertanyaan54, Pertanyaan55, Foto_Dokumentasi_Geotag, Foto_Dokumentasi_Non_Geotag)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, tuple(new_data.values()))
    conn.commit()
    cursor.close()
    conn.close()

# Load data dari Excel dan cache
@st.cache_data
def load_data():
    file_path = 'Data Dukung DUDI 2024 Baru.xlsx'
    df = pd.read_excel(file_path, sheet_name=1)
    df['Kab/Kota'] = df['Kab/Kota'].str.upper()
    return df

# Load data
df = load_data()
kabupaten_list = df['Kab/Kota'].unique()

# HEADER
st.header("BPPP TEGAL")

# Fungsi untuk mereset form dan gambar
def reset_form():
    for key in ["form_data", "uploaded_file", "uploaded_file2"]:
        if key in st.session_state:
            del st.session_state[key]

# Menampilkan dropdown untuk Kabupaten
kabupaten_choice = st.selectbox("Pilih Kabupaten", kabupaten_list, key="kabupaten_choice")

# Reset form jika kabupaten diubah
if "kabupaten_choice" in st.session_state and st.session_state.kabupaten_choice != kabupaten_choice:
    reset_form()

# Filter data berdasarkan Kabupaten yang dipilih
filtered_df = df[df['Kab/Kota'] == kabupaten_choice]

# Jika terdapat lebih dari satu data dengan nama yang sama, tambahkan dropdown NIK untuk memperjelas
nama_list = filtered_df['Nama Purnawidya'].unique()
nama_choice = st.selectbox("Pilih Nama", nama_list, key="nama_choice")

# Filter lebih lanjut jika nama terpilih memiliki lebih dari satu NIK
selected_data_by_name = filtered_df[filtered_df['Nama Purnawidya'] == nama_choice]
if len(selected_data_by_name) > 1:
    st.warning("Terdapat nama yang sama di kabupaten ini. Silakan pilih berdasarkan NIK.")
    nik_list = selected_data_by_name['NIK'].unique()
    nik_choice = st.selectbox("Pilih NIK", nik_list, key="nik_choice")
    selected_data = selected_data_by_name[selected_data_by_name['NIK'] == nik_choice].iloc[0]
else:
    selected_data = selected_data_by_name.iloc[0]

# Menampilkan data peserta
st.write("### Data Peserta:")
st.write(f"**NIK**: {selected_data['NIK']}")
st.write(f"**Alamat**: {selected_data['Alamat']}")
st.write(f"**Jenis Kelamin**: {selected_data['Jenis Kelamin  (L/P)']}")
st.write(f"**Pendidikan Terakhir**: {selected_data['Pendidikan Terakhir']}")
st.write(f"**Nomor Telepon**: {selected_data['Nomor Tlp.']}")
st.write(f"**Nama Pelatihan**: {selected_data['Nama Pelatihan']}")

# --- Menambahkan Form Input Kosong untuk Data Tambahan ---
st.write("### KUISIONER EVALUASI PASCA PELATIHAN MASYARAKAT")

# Form data untuk 16 pertanyaan dengan 4 pilihan (Likert Scale)
likert_options = ['Sangat Tidak Setuju', 'Tidak Setuju', 'Setuju', 'Sangat Setuju']
form_data = {}

# Group 1: Pertanyaan 1 - 3
st.subheader("1. Relevansi Isi Pelatihan")
form_data["Pertanyaan11"] = st.selectbox("Pelatihan yang dilakukan sudah relevan/bersangkut paut dengan pekerjaan Anda sekarang dan tujuan Anda", likert_options)
form_data["Pertanyaan12"] = st.selectbox("Isi Pelatihan (materi, presentasi, dll) mudah dipahami", likert_options)
form_data["Pertanyaan13"] = st.selectbox("Isi Pelatihan (materi, presentasi, dll) sudah menjelaskan topik yang Anda harapkan", likert_options)

# Group 2: Pertanyaan 4 - 6
st.subheader("2. Penerapan/Pengaplikasian Keterampilan, Pengetahuan, dan Sikap")
form_data["Pertanyaan21"] = st.selectbox("Anda mampu menerapkan/mempraktikan Pengetahuan/Keterampilan/Sikap yang anda dapatkan dari pelatihan di tempat kerja anda", likert_options)
form_data["Pertanyaan22"] = st.selectbox("Anda mampu menjelaskan Pengetahuan/Keterampilan/Sikap yang anda peroleh dari orang lain", likert_options)

# Group 3: Pertanyaan 7 - 9
st.subheader("3. Dampak Pelatihan Terhadap Kinerja")
form_data["Pertanyaan31"] = st.selectbox("Pelatihan yang dilakukan sudah bermanfaat terhadap pekerjaan anda", likert_options)
form_data["Pertanyaan32"] = st.text_input("Jika Setuju, Apa bentuk manfaatnya? (Optional)")
form_data["Pertanyaan33"] = st.selectbox("Anda memperoleh kesempatan atau peluang baru yang disebabkan oleh pelatihan yang telah anda lakukan", likert_options)
form_data["Pertanyaan34"] = st.text_input("Jika setuju, seperti apa kesempatan dan peluang barunya? (Optional)")
form_data["Pertanyaan35"] = st.selectbox("Anda merasa lebih mampu dan lebih percaya diri dalam pekerjaan anda setelah ikut pelatihan", likert_options)
form_data["Pertanyaan36"] = st.text_input("Jika setuju, Apa yang membuat anda lebih percaya diri? (Optional)")

# Group 4: Pertanyaan 10 - 12
st.subheader("4. Dampak Pelatihan Terhadap Pendapatan dan Produksi")
form_data["Pertanyaan41"] = st.selectbox("Anda memperoleh peningkatan pendapatan setelah mengikuti pelatihan", likert_options)
form_data["Pertanyaan42"] = st.text_input("Jika Setuju, Berapa peningkatannya? (dalam presentase atau rupiah) - (Optional)")
form_data["Pertanyaan43"] = st.selectbox("Anda memperoleh peningkatan produksi setelah mengikuti pelatihan", likert_options)
form_data["Pertanyaan44"] = st.text_input("Jika Setuju, Berapa peningkatannya? (Optional)")

# Group 5: Pertanyaan 13 - 15
st.subheader("5. Peningkatan Kualitas (Optional)")
form_data["Pertanyaan51"] = st.text_input("Yang menurut anda paling berguna dalam pelatihan ini")
form_data["Pertanyaan52"] = st.text_input("Yang menurut anda paling tidak berguna dalam pelatihan ini", value="tidak ada", disabled=True)
form_data["Pertanyaan53"] = st.text_input("Saran Anda untuk pelaksanaan pelatihan ke depannya")
form_data["Pertanyaan54"] = st.text_input("Saran Anda untuk materi pelatihan ke depannya")
form_data["Pertanyaan55"] = st.text_input("Tambahan*")

# Menambahkan input foto dokumentasi
st.write("### Dokumentasi Foto Geotag (Optional)")
uploaded_file = st.file_uploader("Upload Foto Dokumentasi", type=["jpg", "jpeg", "png"], key="uploaded_file")

# Menambahkan input foto dokumentasi non-geotag
st.write("### Dokumentasi Foto Non Geotag (Optional)")
uploaded_file2 = st.file_uploader("Upload Foto Dokumentasi", type=["jpg", "jpeg", "png"], key="uploaded_file2")

# Tombol untuk submit data ke database MySQL
submit_button = st.button("Submit Jawaban")

if submit_button:
    try:
        # Koneksi ke database MySQL untuk pengecekan nama
        conn_check = create_db_connection()
        cursor_check = conn_check.cursor()

        # Query untuk mengecek apakah NIK atau Nama sudah ada di database
        check_query = """
            SELECT COUNT(*) FROM data_peserta 
            WHERE NIK = %s
        """
        cursor_check.execute(check_query, (selected_data['NIK'],))
        result = cursor_check.fetchone()

        # Jika sudah ada, tampilkan pesan error dan hentikan submit
        if result[0] > 0:
            st.error("Nama atau NIK sudah terdaftar di database. Data tidak bisa disubmit.")
        else:
            # Proses upload gambar ke Cloudinary
            imgur_url_geotag = upload_to_cloudinary(uploaded_file) if uploaded_file is not None else None
            imgur_url_non_geotag = upload_to_cloudinary(uploaded_file2) if uploaded_file2 is not None else None

            # Jika nama atau NIK belum terdaftar, lanjutkan proses submit
            new_data = {
                'NIK': selected_data['NIK'],
                'Nama': selected_data['Nama Purnawidya'],
                'Alamat': selected_data['Alamat'],
                'Kabupaten': kabupaten_choice,
                'Jenis_Kelamin': selected_data['Jenis Kelamin  (L/P)'],
                'Pendidikan_Terakhir': selected_data['Pendidikan Terakhir'],
                'Nomor_Tlp': selected_data['Nomor Tlp.'],
                'Pertanyaan11': form_data["Pertanyaan11"],
                'Pertanyaan12': form_data["Pertanyaan12"],
                'Pertanyaan13': form_data["Pertanyaan13"],
                'Pertanyaan21': form_data["Pertanyaan21"],
                'Pertanyaan22': form_data["Pertanyaan22"],
                'Pertanyaan31': form_data["Pertanyaan31"],
                'Pertanyaan32': form_data["Pertanyaan32"] if form_data["Pertanyaan32"] else None, 
                'Pertanyaan33': form_data["Pertanyaan33"],
                'Pertanyaan34': form_data["Pertanyaan34"] if form_data["Pertanyaan34"] else None, 
                'Pertanyaan35': form_data["Pertanyaan35"],
                'Pertanyaan36': form_data["Pertanyaan36"] if form_data["Pertanyaan36"] else None, 
                'Pertanyaan41': form_data["Pertanyaan41"],
                'Pertanyaan42': form_data["Pertanyaan42"] if form_data["Pertanyaan42"] else None, 
                'Pertanyaan43': form_data["Pertanyaan43"],
                'Pertanyaan44': form_data["Pertanyaan44"] if form_data["Pertanyaan44"] else None, 
                'Pertanyaan51': form_data["Pertanyaan51"] if form_data["Pertanyaan51"] else None, 
                'Pertanyaan52': form_data["Pertanyaan52"] if form_data["Pertanyaan52"] else None, 
                'Pertanyaan53': form_data["Pertanyaan53"] if form_data["Pertanyaan53"] else None, 
                'Pertanyaan54': form_data["Pertanyaan54"] if form_data["Pertanyaan54"] else None, 
                'Pertanyaan55': form_data["Pertanyaan55"] if form_data["Pertanyaan55"] else None,
                'Foto_Dokumentasi_Geotag': imgur_url_geotag,
                'Foto_Dokumentasi_Non_Geotag': imgur_url_non_geotag
            }

            # Simpan data ke database
            save_data_to_db(new_data)

            # Menampilkan konfirmasi
            st.success("Data berhasil disimpan!")

    except mysql.connector.Error as e:
        st.error(f"Terjadi kesalahan saat menyimpan data: {e}")
    finally:
        # Pastikan koneksi ditutup hanya jika terbuka
        if 'conn_check' in locals() and conn_check.is_connected():
            cursor_check.close()
            conn_check.close()

# Menambahkan tombol untuk mereset form
if st.button("Reset Form"):
    reset_form()
