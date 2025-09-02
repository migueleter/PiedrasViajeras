from flask import Flask, render_template, request, jsonify, redirect, url_for
import csv
import datetime
import os

app = Flask(__name__)
CSV_FILE = 'piedrasviajeras.csv'

# Inicializa el archivo CSV si no existe
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['IdPiedra', 'Fecha', 'Latitud', 'Longitud', 'Foto'])
init_csv()

def leer_localizaciones(id_piedra):
    localizaciones = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['IdPiedra'] == id_piedra:
                localizaciones.append(row)
    # Ordenar por Fecha
    localizaciones.sort(key=lambda x: x['Fecha'])
    return localizaciones

def añadir_localizacion(id_piedra, lat, lon, fecha, foto=None):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([id_piedra, fecha, lat, lon, foto if foto else ''])

def actualizar_foto(id_piedra, fecha, foto_url):
    # Leer todas las filas
    filas = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['IdPiedra'] == id_piedra and row['Fecha'] == fecha:
                row['Foto'] = foto_url
            filas.append(row)
    # Escribir de nuevo el archivo
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['IdPiedra', 'Fecha', 'Latitud', 'Longitud', 'Foto'], delimiter=';')
        writer.writeheader()
        writer.writerows(filas)

@app.route('/')
def home():
    return "Usa /piedra?IdPiedra=XXX"

@app.route('/piedra')
def piedra():
    id_piedra = request.args.get('IdPiedra', '1') # Valor por defecto '1'
    # if not id_piedra:
    #     return "Falta el parámetro IdPiedra"
    localizaciones = leer_localizaciones(id_piedra)
    return render_template('index.html', id_piedra=id_piedra, localizaciones=localizaciones)

@app.route('/add_location', methods=['POST'])
def add_location():
    data = request.json
    id_piedra = data['IdPiedra']
    lat = data['Latitud']
    lon = data['Longitud']
    fecha = datetime.datetime.now().isoformat()
    añadir_localizacion(id_piedra, lat, lon, fecha)
    return jsonify({'success': True, 'fecha': fecha})

@app.route('/add_photo', methods=['POST'])
def add_photo():
    id_piedra = request.form['IdPiedra']
    fecha = request.form['Fecha']
    photo = request.files['Foto']
    os.makedirs('static/uploads', exist_ok=True)
    filename = f"{id_piedra}_{fecha.replace(':','-')}.jpg"
    filepath = os.path.join('static/uploads', filename)
    photo.save(filepath)
    photo_url = url_for('static', filename=f'uploads/{filename}')
    actualizar_foto(id_piedra, fecha, photo_url)
    return jsonify({'success': True, 'photo_url': photo_url})

@app.route('/get_locations')
def get_locations():
    id_piedra = request.args.get('IdPiedra')
    localizaciones = leer_localizaciones(id_piedra)
    return jsonify(localizaciones)

if __name__ == '__main__':
    app.run(debug=True)
