from flask import Flask, render_template, request
import numpy as np
import os
import matplotlib.pyplot as plt

# Konfigurasi Flask
app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def run_simulation(berat_badan, jumlah_sesi, probabilitas):
    # Perhitungan kebutuhan cairan
    kebutuhan_cairan = berat_badan * 35
    cairan_per_sesi = kebutuhan_cairan / jumlah_sesi

    # Simulasi menggunakan distribusi binomial
    simulasi = np.random.binomial(n=jumlah_sesi, p=probabilitas, size=1000)
    total_cairan = simulasi * cairan_per_sesi

    # Statistik dasar
    rata_rata_cairan = np.mean(total_cairan)
    standar_deviasi_cairan = np.std(total_cairan)

    # Langkah-langkah perhitungan dengan rumus
    penjelasan = {
        "kebutuhan_cairan": r"Kebutuhan cairan dihitung dengan rumus: \( \text{Kebutuhan Cairan} = \text{Berat Badan} \times 35 \)."
                             f"<br>Dengan berat badan {berat_badan} kg: \( {berat_badan} \times 35 = {kebutuhan_cairan} \, \text{{ml}} \).",
        "cairan_per_sesi": r"Cairan per sesi dihitung dengan rumus: \( \text{Cairan per Sesi} = \frac{\text{Kebutuhan Cairan}}{\text{Jumlah Sesi}} \)."
                            f"<br>Dengan kebutuhan cairan {kebutuhan_cairan} ml dan jumlah sesi {jumlah_sesi}: "
                            f"\( \frac{{{kebutuhan_cairan}}}{{{jumlah_sesi}}} = {cairan_per_sesi:.2f} \, \text{{ml/sesi}} \).",
        "probabilitas": f"Probabilitas minum cukup adalah {probabilitas * 100:.1f}% di setiap sesi minum.",
        "contoh_iterasi": r"Contoh hasil iterasi simulasi: "
                           f"{simulasi[0]} sesi sukses dari {jumlah_sesi} sesi.<br>"
                           r"Total cairan diminum dihitung dengan rumus: \( \text{Total Cairan} = \text{Sesi Sukses} \times \text{Cairan per Sesi} \)."
                           f"<br>Dengan {simulasi[0]} sesi sukses dan cairan per sesi {cairan_per_sesi:.2f} ml:"
                           f" \( {simulasi[0]} \times {cairan_per_sesi:.2f} = {simulasi[0] * cairan_per_sesi:.2f} \, \text{{ml}} \).",
        "statistik": r"Dari 1000 iterasi simulasi, dihitung statistik:<br>"
                      r"- Rata-rata cairan diminum: \( \mu = \frac{1}{N} \sum_{i=1}^{N} x_i \)."
                      f"<br>Hasil: \( \mu = {rata_rata_cairan:.2f} \, \text{{ml}} \).<br>"
                      r"- Standar deviasi: \( \sigma = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2} \)."
                      f"<br>Hasil: \( \sigma = {standar_deviasi_cairan:.2f} \, \text{{ml}} \)."
    }

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(total_cairan, bins=20, color='lightblue', alpha=0.8, edgecolor='black')
    plt.axvline(kebutuhan_cairan, color='red', linestyle='--', label='Kebutuhan Cairan')
    plt.title("Simulasi Kebutuhan Cairan (Distribusi Binomial)")
    plt.xlabel("Total Cairan Diminum (ml)")
    plt.ylabel("Frekuensi")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save plot to static folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'histogram.png')
    plt.savefig(file_path)
    plt.close()

    return kebutuhan_cairan, rata_rata_cairan, standar_deviasi_cairan, file_path, penjelasan

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            berat_badan = float(request.form['berat_badan'])
            jumlah_sesi = int(request.form['jumlah_sesi'])
            probabilitas = float(request.form['probabilitas'])

            # Run simulation
            kebutuhan_cairan, rata_rata_cairan, standar_deviasi_cairan, plot_path, penjelasan = run_simulation(
                berat_badan, jumlah_sesi, probabilitas
            )

            return render_template(
                'index.html',
                hasil=True,
                kebutuhan_cairan=kebutuhan_cairan,
                rata_rata_cairan=rata_rata_cairan,
                standar_deviasi_cairan=standar_deviasi_cairan,
                plot_path=plot_path,
                penjelasan=penjelasan,
                berat_badan=berat_badan,
                jumlah_sesi=jumlah_sesi,
                probabilitas=probabilitas,
            )
        except ValueError:
            return render_template('index.html', error="Input tidak valid. Silakan coba lagi.")

    return render_template('index.html', hasil=False)

if __name__ == '__main__':
    app.run(debug=True)
