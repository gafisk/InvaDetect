from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/prediksi', methods=['GET', 'POST'])
def prediksi():
    # Pemetaan nama input ke nama fitur asli
    mapping = {
        'p1': 'Usia (tahun)',
        'p2': 'Jenis kelamin',
        'p3': 'Penggunaan antibiotik',
        'p4': 'Jumlah alat medis invasif',
        'p5': 'Perpaduan jenis alat medis invasif',
        'p6': 'Penggunaan CVC',
        'p7': 'Lama penggunaan CVC (hari)',
        'p8': 'Sepsis',
        'p9': 'Total parenteral nutrition',
        'p10': 'Multifokal kolonisasi Candida',
        'p11': 'Riwayat pembedahan gastrointestinal',
        'p12': 'Lama rawat (hari)',
        'p13': 'Riwayat perawatan di RS sebelumnya',
        'p14': 'Riwayat penyakit penyerta',
        'p15': 'Konsentrasi beta-D-glukan (pg/ml)'
    }

    input_names = [f'p{i}' for i in range(1, 16)]

    if request.method == 'POST':
        input_values = {}

        # Ambil data dari form
        for name in input_names:
            if name == 'p5':
                raw_p5_list = request.form.getlist('p5[]')
                input_values[name] = raw_p5_list
            else:
                value = request.form.get(name)
                try:
                    input_values[name] = float(value)
                except (ValueError, TypeError):
                    input_values[name] = 0.0

        # Proses encoding fitur p5
        try:
            converted_p5 = [x.replace('_', ' ') for x in input_values['p5']]
            sorted_p5 = ', '.join(sorted(converted_p5)).lower()
            le = joblib.load('models/Encoder_Fitur_5.pkl')
            input_values['p5'] = int(le.transform([sorted_p5])[0])
        except Exception as e:
            print("Encoding p5 gagal:", e)
            input_values['p5'] = 0

        print("Data untuk prediksi:", input_values)

        # Prediksi menggunakan model
        try:
            model = joblib.load('models/dt_model.pkl')
            input_renamed = {mapping[k]: v for k, v in input_values.items()}
            X = pd.DataFrame([input_renamed])
            y_pred = model.predict(X)[0]

            label_mapping = {
                0: 'Tidak Kandidiasis invasif',
                1: 'Kandidiasis invasif'
            }

            hasil_prediksi = label_mapping.get(int(y_pred), 'Tidak diketahui')

        except Exception as e:
            print("Prediksi gagal:", e)
            hasil_prediksi = 'Error dalam prediksi'
        print(hasil_prediksi)
        return render_template("prediksi.html", hasil_prediksi=hasil_prediksi)

    return render_template("prediksi.html")


if __name__ == "__main__":
    app.run(debug=True)
