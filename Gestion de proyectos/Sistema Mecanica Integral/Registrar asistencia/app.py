from flask import Flask, request, redirect, render_template, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'asistencias'
}

# Función general para registrar asistencia
def registrar_asistencia(tabla, id_column, codigo):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute(f"SELECT id FROM {tabla} WHERE codigo = %s", (codigo,))
    trabajador = cursor.fetchone()

    if trabajador:
        ahora = datetime.now()
        if ahora.hour == 13 and ahora.minute <= 30:
            estado = 'Entrada'
        elif ahora.hour == 19:  # Hora de salida fijada a las 7 PM
            estado = 'Salida'
        else:
            estado = 'Hora no válida'
        
        if estado != 'Hora no válida':
            cursor.execute(f"INSERT INTO {id_column} ({tabla[:-1]}_id, estado, fecha_hora) VALUES (%s, %s, %s)", (trabajador['id'], estado, ahora))
            db.commit()
            mensaje = f'Asistencia registrada correctamente: {estado}.'
        else:
            mensaje = 'No es momento de registrar entrada o salida.'
        
        cursor.close()
        db.close()
        return mensaje
    else:
        cursor.close()
        db.close()
        return 'El código proporcionado no corresponde a ningún trabajador registrado.'

# Rutas modificadas para cada tipo de trabajador
@app.route('/registrarmecanico', methods=['GET', 'POST'])
def registrarmecanico():
    if request.method == 'POST':
        codigo = request.form['codigo']
        resultado = registrar_asistencia('mecanicos', 'asistenciasmecanico', codigo)
        return render_template('mecanicos.html', resultado=resultado)
    return render_template('mecanicos.html')

@app.route('/registrarsoldador', methods=['GET', 'POST'])
def registrarsoldador():
    if request.method == 'POST':
        codigo = request.form['codigo']
        resultado = registrar_asistencia('soldadores', 'asistenciassoldador', codigo)
        return render_template('soldadores.html', resultado=resultado)
    return render_template('soldadores.html')

@app.route('/registrarlavador', methods=['GET', 'POST'])
def registrarlavador():
    if request.method == 'POST':
        codigo = request.form['codigo']
        resultado = registrar_asistencia('lavadores', 'asistenciaslavador', codigo)
        return render_template('lavadores.html', resultado=resultado)
    return render_template('lavadores.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

