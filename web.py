import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
import streamlit as st
from io import StringIO
from imblearn.over_sampling import SMOTE


st.set_page_config(page_title='Smart Hidroponik', layout='wide',initial_sidebar_state="collapsed", page_icon="https://raw.githubusercontent.com/Yeahthu/tes-streamlit/main/logo%20fixx1.png",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
                  )
# Fungsi untuk mengambil nilai sensor terbaru dari MongoDB
def get_latest_sensor_data():
    client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
    db = client['Smart_Hidroponik']
    collection = db['Sensor']

    latest_data_cursor = collection.find({}, {'_id': 0, 'pH': 1, 'tds': 1, 'suhu': 1}).sort('waktu', -1).limit(1)
    latest_data = list(latest_data_cursor)
    return latest_data[0] if latest_data else None

# Fungsi utama Streamlit
def streamlit_app():

    
    

    # Konten CSS dari tes2.css
    desain_css = """
    <style>
<style>
body {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
    background-color: #fff;
}

#Tampilan {
    position: relative;
    width: 100%;
    margin: 10px auto;
    border-radius: 10px;
}

.bagian-header {
    background-image: url("https://raw.githubusercontent.com/Yeahthu/tes-streamlit/main/bgHidroponik.jpg");
    border-radius: 10px 10px 0 0;
    border-bottom: 2px solid #eb0e0e;
    margin: 0;
    padding: 20px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover; 
    text-align: center;
    height: 18.75em;
}

#logo {
    width: 20%;
    border-radius: 30px;
}

.bagian-utama {
    margin: 8px;
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
}

.bagian-utama > .sensor {
    flex: 1 1 30%; /* Atur lebar sensor dengan proporsi */
    text-align: center;
    box-sizing: border-box;
}


.judul-overview {
    font-size: 24px;
    font-weight: bold;
    width: 100%;
    text-align: center;
    margin: 20px;
    color: red;
}

.sensor h2 {
    margin: 0px;
    font-size: 24px;
    font-weight: bold;
    color: red;
    text-align: center;
}

.sensor {
    padding: 0px;
    margin: 1px;
}

#icon_pH, #icon_suhu, #icon_nutrisi {
    width: 25%;
}

.bagian_ph, .bagian_suhu, .bagian_nutrisi {
    font-size: 24px;
    font-weight: bold;
    margin: 10px;
}

.unit {
    font-size: 12px;
    color: #eb0e0e;
    vertical-align: middle;
}

.value {
    color: rgb(0, 255, 30);
}

.bagian-akhir {
    margin: 50em;
    padding: 15px;
    height: 20%;
}

.status-hidroponik {
    font-size: 24px;
    font-weight: bold;
    width: 100%;
    text-align: center;
    margin: 20px;
    margin-top: 200px;
    color: #2E8B57;
}

.batas-text {
    font-family: 'Courier New', Courier, monospace;
    font-size: 20px;
    text-align: center;
    margin: 0px;
    color: orange;
}

.ukuran {
    width: 100%;
    border-radius: 20px;
    border-top: 4px solid RGB(169, 169, 169);
    border-bottom: 4px solid RGB(169, 169, 169);
    margin-bottom:3em;
    margin-left: 0em;
    margin-right: 14em;
    padding: 15px;
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

.slide-ph, .slide-suhu, .slide-nutrisi {
    -webkit-appearance: none;
    width: 100%;
    margin: 30px 0;
}

.slide-ph:focus, .slide-suhu:focus, .slide-nutrisi:focus {
    outline: none;
}

.slide-ph::-webkit-slider-runnable-track, .slide-suhu::-webkit-slider-runnable-track, .slide-nutrisi::-webkit-slider-runnable-track {
    width: 100%;
    height: 8.4px;
    cursor: pointer;
    border-radius: 10px;
    border: 0.2px solid #010101;
}

.slide-ph::-webkit-slider-runnable-track {
    background: linear-gradient(to right, 
                red 0%, rgb(255, 149, 0) 20%, 
                rgb(36, 249, 3) 30%, rgb(2, 82, 2) 50%, 
                rgb(45, 1, 76) 80%, purple 100%);
}

.slide-suhu::-webkit-slider-runnable-track {
    background: linear-gradient(to right, 
                rgb(0, 42, 255) 0%, rgb(52, 63, 217) 20%, 
                rgb(145, 184, 219) 30%, rgb(0, 246, 45) 50%, 
                rgb(255, 149, 0) 80%, red 100%);
}

.slide-nutrisi::-webkit-slider-runnable-track {
    background: linear-gradient(to right, 
                blue 0%, green 50%, red 100%);
}

.slide-ph::-webkit-slider-thumb, .slide-suhu::-webkit-slider-thumb, .slide-nutrisi::-webkit-slider-thumb {
    -webkit-appearance: none;
    height: 23px;
    width: 23px;
    border-radius: 50%;
    background-color: transparent;
    background-image: url("https://github.com/Yeahthu/tes-streamlit/blob/main/kursor_fixx.png?raw=true");
    background-size: cover;
    cursor: pointer;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
    margin-top: -21px;
}

.label {
    display: flex;
    justify-content: space-between;
    margin: 10px;
    padding: 10px;
    font-size: 14px;
}

.info {
    width: 33.33%;
    text-align: center;
}

@media (max-width: 768px) {
    .bagian-header {
        height: 200px;
    }
    .judul-overview {
        font-size: 18px;
    }
    .sensor h2 {
        font-size: 20px;
    }
    .bagian_ph, .bagian_suhu, .bagian_nutrisi {
        font-size: 18px;
    }
    .status-hidroponik {
        font-size: 18px;
    }
    .batas-text {
        font-size: 16px;
    }
}
</style>

    """
    sensor_data = get_latest_sensor_data()
    if sensor_data is not None:
        ph_value = sensor_data['pH']
        suhu_value = sensor_data['suhu']
        tds_value = sensor_data['tds']

    else:
        st.write('Tidak ada data sensor yang tersedia saat ini.')
    # Konten HTML dari tes2.html
    html_content = f"""
  <div id = "Tampilan">
    <div class = "bagian-header">
      <img src="https://raw.githubusercontent.com/Yeahthu/tes-streamlit/main/logo%20fixx1.png" alt="logo" id="logo">
    </div>
    <h1 class="judul-overview">Ringkasan Hidroponik</h1>
    <div class="bagian-utama">
      <div class="sensor">
        <img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_pH_new.png?raw=true" alt="icon_pH" id="icon_pH" />
        <h2>pH Air</h2>
        <div class="bagian_ph">
          <span class="value">{ph_value}</span>
          <span class="unit">pH</span>
        </div>
      </div>
      <div class="sensor">
        <img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_suhu_air.png?raw=true" alt="icon_suhu" id="icon_suhu" /> 
        <h2>Suhu Air</h2>
        <div class="bagian_suhu">
          <span class="value">{suhu_value}</span>
          <span class="unit">°C</span>
        </div>
      </div>
      <div class="sensor">
        <img src="https://github.com/Yeahthu/tes-streamlit/blob/main/icon_tds.png?raw=true" alt="icon_nutrisi" id="icon_nutrisi" />
        <h2>Nutrisi</h2>
        <div class="bagian_nutrisi">
          <span class="value">{tds_value}</span>
          <span class="unit">ppm</span>
        </div>
      </div>
    </div>
    <h1 class="status-hidroponik">Status hidroponik</h1>
    </div>
<div class="ukuran">
        <h1 class="batas-text">Ukuran pH</h1>
        <input type="range" min="1" max="14" value="{ph_value}" class="slide-ph" id="myRange">
        <div class="label">
          <div class="info">Kadar rendah</div>
          <div class="info">Kadar sesuai</div>
          <div class="info">Kadar tinggi</div>
        </div>
        <div class="label">
          <div class="info">[1-4]</div>
          <div class="info">[5-7]</div>
          <div class="info">[9-14]</div>
        </div>
        <p>pH tanamanmu: <span id="demo">{ph_value}</span></p>
    </div>
    <div class="ukuran">
        <h1 class="batas-text">Ukuran Suhu</h1>
        <input type="range" min="1" max="45" value="{suhu_value}" class="slide-suhu" id="myRange">
        <div class="label">
          <div class="info">Kadar rendah</div>
          <div class="info">Kadar sesuai</div>
          <div class="info">Kadar tinggi</div>
        </div>
        <div class="label">
          <div class="info">[Kurang dari 18 C]</div>
          <div class="info">[18 - 25 C]</div>
          <div class="info">[Lebih dar 25 C]</div>
        </div>
        <p>Suhu tanamanmu: <span id="demo">{suhu_value}</span></p>
    </div>
        <div class="ukuran">
        <h1 class="batas-text">Ukuran Nutrisi</h1>
        <input type="range" min="1" max="5000" value="{tds_value}" class="slide-nutrisi" id="myRange">
        <div class="label">
          <div class="info">Kadar rendah</div>
          <div class="info">Kadar sesuai</div>
          <div class="info">Kadar tinggi</div>
        </div>
        <div class="label">
          <div class="info">[Kurang dari 1050 ppm]</div>
          <div class="info">[1050 - 1400 ppm]</div>
          <div class="info">[Lebih dari 1400 ppm]</div>
        </div>
        <p>NUtrisi di tanamanmu: <span id="demo">{tds_value}</span></p>
    </div>
    <script>
        var slider = document.getElementById("myRange");
        var output = document.getElementById("demo");
        output.innerHTML = slider.value;
        slider.oninput = function() {{
            output.innerHTML = this.value;
            var cursorImage = "url(https://github.com/Yeahthu/tes-streamlit/blob/main/kursor_fixx.png?raw=true)";
            slider.style.cursor = cursorImage;
        }}

    </script>
    """

    # Mengambil nilai sensor awal dari MongoDB


    # Menampilkan CSS dan HTML di Streamlit
    st.markdown(desain_css, unsafe_allow_html=True)
    st.markdown(html_content, unsafe_allow_html=True)


def ml():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://SmartHidroponik:MERA_X@smarthidroponik.hdetbis.mongodb.net/?retryWrites=true&w=majority&appName=SmartHidroponik')
    db = client['Smart_Hidroponik']
    collection = db['Sensor']

    # Load data from MongoDB
    data = list(collection.find())
    data_rapi = pd.DataFrame(data)

    st.title("Smart Hidroponik - Prediksi Kesehatan Tanaman")

    # Display the data
    st.subheader("Data Sensor")
    st.write(data_rapi)

    # Clean the data
    st.subheader("Pengecekan Data")
    st.write("Deskripsi Data:")
    st.write(data_rapi.describe())

    if data_rapi.isnull().sum().sum() == 0:
        st.write("- Tidak Ada Data Kosong")
    else:
        st.write("- Ada Data Kosong")
        st.write(data_rapi[data_rapi.isnull().any(axis=1)])

    if data_rapi.duplicated().sum() == 0:
        st.write("- Tidak Ada Penduplikatan data")
    else:
        st.write("- Ada Penduplikatan data")
        st.write(data_rapi[data_rapi.duplicated()])

    # Drop unnecessary columns
    data_rapi = data_rapi.drop(columns=['_id', 'waktu'])

    # Data Correlation
    st.subheader("Korelasi Data")
    korelasi_data = data_rapi.corr()
    fig, ax = plt.subplots()
    sns.heatmap(korelasi_data, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    plt.title('Heatmap Korelasi')
    st.pyplot(fig)

    # Categorize target variables
    def categorize_ph(value):
        if value < 5:
            return 'Rendah'
        elif 5 <= value <= 7:
            return 'Sedang'
        else:
            return 'Tinggi'

    def categorize_tds(value):
        if value < 1050:
            return 'Rendah'
        elif 1050 <= value <= 1400:
            return 'Sedang'
        else:
            return 'Tinggi'

    data_rapi['pH kategori'] = data_rapi['pH'].apply(categorize_ph)
    data_rapi['TDS kategori'] = data_rapi['tds'].apply(categorize_tds)

    # Encode categorical data
    label_encoder = LabelEncoder()
    data_rapi['TDS kategori'] = label_encoder.fit_transform(data_rapi['TDS kategori'])
    data_rapi['pH kategori'] = label_encoder.fit_transform(data_rapi['pH kategori'])

    # Prepare data for modeling
    independen_ph = data_rapi[['suhu', 'tds']]
    dependen_ph = data_rapi['pH kategori']
    independen_nutrisi = data_rapi[['suhu', 'pH']]
    dependen_nutrisi = data_rapi['TDS kategori']

    # Split data
    independen_train_ph, independen_test_ph, dependen_train_ph, dependen_test_ph = train_test_split(independen_ph, dependen_ph, test_size=0.25, stratify=dependen_ph)
    independen_train_nutrisi, independen_test_nutrisi, dependen_train_nutrisi, dependen_test_nutrisi = train_test_split(independen_nutrisi, dependen_nutrisi, test_size=0.25, stratify=dependen_nutrisi)

    # Apply SMOTE to handle class imbalance
    smote = SMOTE()
    independen_train_ph, dependen_train_ph = smote.fit_resample(independen_train_ph, dependen_train_ph)
    independen_train_nutrisi, dependen_train_nutrisi = smote.fit_resample(independen_train_nutrisi, dependen_train_nutrisi)

    # Modeling pH
    model_LR_ph = LogisticRegression(class_weight='balanced')
    model_LR_ph.fit(independen_train_ph, dependen_train_ph)
    hasil_prediksi_LR_ph = model_LR_ph.predict(independen_test_ph)

    model_RF_ph = RandomForestClassifier(class_weight='balanced')
    model_RF_ph.fit(independen_train_ph, dependen_train_ph)
    hasil_prediksi_RF_ph = model_RF_ph.predict(independen_test_ph)

    # Modeling Nutrisi
    model_LR_nutrisi = LogisticRegression(class_weight='balanced')
    model_LR_nutrisi.fit(independen_train_nutrisi, dependen_train_nutrisi)
    hasil_prediksi_LR_nutrisi = model_LR_nutrisi.predict(independen_test_nutrisi)

    model_RF_nutrisi = RandomForestClassifier(class_weight='balanced')
    model_RF_nutrisi.fit(independen_train_nutrisi, dependen_train_nutrisi)
    hasil_prediksi_RF_nutrisi = model_RF_nutrisi.predict(independen_test_nutrisi)

    # Evaluation
    accuracy_LR_ph = accuracy_score(dependen_test_ph, hasil_prediksi_LR_ph)
    precision_LR_ph = precision_score(dependen_test_ph, hasil_prediksi_LR_ph, average='macro')
    recall_LR_ph = recall_score(dependen_test_ph, hasil_prediksi_LR_ph, average='macro')
    f1_LR_ph = f1_score(dependen_test_ph, hasil_prediksi_LR_ph, average='macro')

    accuracy_RF_ph = accuracy_score(dependen_test_ph, hasil_prediksi_RF_ph)
    precision_RF_ph = precision_score(dependen_test_ph, hasil_prediksi_RF_ph, average='macro')
    recall_RF_ph = recall_score(dependen_test_ph, hasil_prediksi_RF_ph, average='macro')
    f1_RF_ph = f1_score(dependen_test_ph, hasil_prediksi_RF_ph, average='macro')

    accuracy_LR_nutrisi = accuracy_score(dependen_test_nutrisi, hasil_prediksi_LR_nutrisi)
    precision_LR_nutrisi = precision_score(dependen_test_nutrisi, hasil_prediksi_LR_nutrisi, average='macro')
    recall_LR_nutrisi = recall_score(dependen_test_nutrisi, hasil_prediksi_LR_nutrisi, average='macro')
    f1_LR_nutrisi = f1_score(dependen_test_nutrisi, hasil_prediksi_LR_nutrisi, average='macro')

    accuracy_RF_nutrisi = accuracy_score(dependen_test_nutrisi, hasil_prediksi_RF_nutrisi)
    precision_RF_nutrisi = precision_score(dependen_test_nutrisi, hasil_prediksi_RF_nutrisi, average='macro')
    recall_RF_nutrisi = recall_score(dependen_test_nutrisi, hasil_prediksi_RF_nutrisi, average='macro')
    f1_RF_nutrisi = f1_score(dependen_test_nutrisi, hasil_prediksi_RF_nutrisi, average='macro')

    # Display metrics
    st.write("Logistik Regression pH")
    st.write(f"Accuracy Logistic Regression: {accuracy_LR_ph}")
    st.write(f"Precision Logistic Regression: {precision_LR_ph}")
    st.write(f"Recall Logistic Regression: {recall_LR_ph}")
    st.write(f"F1-score Logistic Regression: {f1_LR_ph}")

    st.write("Random Forest pH")
    st.write(f"Accuracy Random Forest: {accuracy_RF_ph}")
    st.write(f"Precision Random Forest: {precision_RF_ph}")
    st.write(f"Recall Random Forest: {recall_RF_ph}")
    st.write(f"F1-score Random Forest: {f1_RF_ph}")

    st.write("Logistik Regression Nutrisi")
    st.write(f"Accuracy Logistic Regression: {accuracy_LR_nutrisi}")
    st.write(f"Precision Logistic Regression: {precision_LR_nutrisi}")
    st.write(f"Recall Logistic Regression: {recall_LR_nutrisi}")
    st.write(f"F1-score Logistic Regression: {f1_LR_nutrisi}")

    st.write("Random Forest Nutrisi")
    st.write(f"Accuracy Random Forest: {accuracy_RF_nutrisi}")
    st.write(f"Precision Random Forest: {precision_RF_nutrisi}")
    st.write(f"Recall Random Forest: {recall_RF_nutrisi}")
    st.write(f"F1-score Random Forest: {f1_RF_nutrisi}")

    # Plot sensor data
    st.subheader("Grafik Sensor")
    st.write("pH Sensor:")
    st.line_chart(data_rapi.set_index('waktu')['pH'])

    st.write("Suhu Air:")
    st.line_chart(data_rapi.set_index('waktu')['suhu'])

    st.write("Nutrisi (TDS):")
    st.line_chart(data_rapi.set_index('waktu')['tds'])
    
if 'page' not in st.session_state:
    st.session_state.page = "Home"
    
# Menampilkan konten berdasarkan halaman yang dipilih
if st.session_state.page == "Home":
    st.title("Home")
    streamlit_app()
    st.write("Ini adalah halaman Home.")
    if st.button("Lanjutkan ke Page 2"):
        st.session_state.page = "Page 2"

elif st.session_state.page == "Page 2":
    st.title("Page 2")
    ml()  # Panggil fungsi ml() di sini
    st.write("Ini adalah halaman kedua.")
    if st.button("Kembali ke Home"):
        st.session_state.page

