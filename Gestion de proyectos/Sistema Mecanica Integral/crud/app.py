import io
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_mysqldb import MySQL
from fpdf import FPDF
from flask import send_file
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import barcode
from barcode.writer import ImageWriter


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'asistencias'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Rutas para manejar los mecánicos
@app.route('/mecanicos', methods=['GET', 'POST'])
def mecanicos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mecanicos (nombre, codigo) VALUES (%s, %s)", (nombre, codigo))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('mecanicos'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM mecanicos")
    mecanicos = cur.fetchall()
    cur.close()
    return render_template('mecanicos.html', mecanicos=mecanicos)

@app.route('/agregar', methods=['POST'])
def agregar_mecanico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mecanicos (nombre, codigo) VALUES (%s, %s)", (nombre, codigo))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('mecanicos'))

@app.route('/mecanicos/<int:id>/eliminar', methods=['GET'])
def eliminar_mecanico(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM mecanicos WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print("Error al eliminar el mecánico:", e)
        return "Ocurrió un error al eliminar al mecánico"
    finally:
        cur.close()
    return redirect(url_for('mecanicos'))


@app.route('/mecanicos/<int:id>/editar', methods=['GET', 'POST'])
def editar_mecanico(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE mecanicos SET nombre = %s, codigo = %s WHERE id = %s", (nuevo_nombre, nuevo_codigo, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('mecanicos'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM mecanicos WHERE id = %s", (id,))
        mecanico = cur.fetchone()
        cur.close()
        return render_template('editar.html', mecanico=mecanico)
    
    # Rutas para manejar los soldadores
@app.route('/soldadores', methods=['GET', 'POST'])
def soldadores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO soldadores (nombre, codigo) VALUES (%s, %s)", (nombre, codigo))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('soldadores'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM soldadores")
    soldadores = cur.fetchall()
    cur.close()
    return render_template('soldadores.html', soldadores=soldadores)

# Agregar soldadores
@app.route('/agregarsoldador', methods=['POST'])
def agregar_soldadores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO soldadores (nombre, codigo) VALUES (%s, %s)", (nombre, codigo))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('soldadores'))

@app.route('/soldadores/<int:id>/eliminar', methods=['GET'])
def eliminar_soldadores(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM soldadores WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print("Error al eliminar el soldador:", e)
        return "Ocurrió un error al eliminar al soldador"
    finally:
        cur.close()
    return redirect(url_for('soldadores'))



@app.route('/soldadores/<int:id>/editarsoldador', methods=['GET', 'POST'])
def editar_soldador(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE soldadores SET nombre = %s,  codigo = %s WHERE id = %s", (nuevo_nombre, nuevo_codigo, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('soldadores'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM soldadores WHERE id = %s", (id,))
        soldador = cur.fetchone()
        cur.close()
        return render_template('editarsoldador.html', soldador=soldador)
    
    # Rutas para manejar los lavadores
@app.route('/lavadores', methods=['GET', 'POST'])
def lavadores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO lavadores (nombre, codigo) VALUES (%s, %s)", (nombre, codigo))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('lavadores'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM lavadores")
    lavadores = cur.fetchall()
    cur.close()
    return render_template('lavadores.html', lavadores=lavadores)

# Agregar lavadores
@app.route('/agregarlavador', methods=['POST'])
def agregar_lavadores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO lavadores (nombre, codigo) VALUES (%s, %s)", (nombre, codigo))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('lavadores'))

@app.route('/lavadores/<int:id>/eliminar', methods=['GET'])
def eliminar_lavadores(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM lavadores WHERE id = %s", (id,))
        mysql.connection.commit()
    except Exception as e:
        print("Error al eliminar el lavador:", e)
        return "Ocurrió un error al eliminar al lavador"
    finally:
        cur.close()
    return redirect(url_for('lavadores'))



@app.route('/lavadores/<int:id>/editarlavador', methods=['GET', 'POST'])
def editar_lavador(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_codigo = request.form['codigo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE lavadores SET nombre = %s, codigo = %s WHERE id = %s", (nuevo_nombre, nuevo_codigo, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('lavadores'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM lavadores WHERE id = %s", (id,))
        lavador = cur.fetchone()
        cur.close()
        return render_template('editarlavador.html', lavador=lavador)
    
# Generar PDF Mecanico
@app.route('/generar_pdfmecanico')
def generar_pdfmecanico():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.image('static/logo.png', x=10, y=8, w=25)
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=24)
    pdf.cell(200, 10, txt="MECANICA INTEGRAL", ln=True, align='C')
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Registro de Asistencias para Mecánicos", ln=True, align='C')
    pdf.set_font("Arial", size=12)

    # Obtener registros de asistencias desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT mecanicos.nombre, asistenciasmecanico.estado, asistenciasmecanico.fecha_hora FROM asistenciasmecanico JOIN mecanicos ON asistenciasmecanico.mecanico_id = mecanicos.id")
    asistenciasmecanico = cur.fetchall()
    cur.close()

    # Agregar los registros al PDF
    for asistenciasmecanicos in asistenciasmecanico:
        nombre = asistenciasmecanicos['nombre']
        estado = asistenciasmecanicos['estado']
        fecha_hora = asistenciasmecanicos['fecha_hora'].strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, txt=f"Nombre: {nombre}, Estado: {estado}, Fecha y Hora: {fecha_hora}", ln=True, align='L')

        # Generar y agregar el código de barras
        codigo_barras = barcode.get_barcode_class('code128')
        codigo = codigo_barras(f'Nombre: {nombre}, Estado: {estado}, Fecha y Hora: {fecha_hora}', writer=ImageWriter())
        codigo_file = codigo.save('codigo_barras')

        # Insertar la imagen del código de barras centrada y en la parte inferior de la página
        pdf.image('codigo_barras.png', x=pdf.w/2-50, y=pdf.h - 50, w=100)

   
    # Guardar el PDF en el servidor
    pdf_output = "registro_asistencias_mecanico.pdf"
    pdf.output(pdf_output)

    # Devolver el archivo para descarga
    return send_file(pdf_output, as_attachment=True)

# Generar PDF Soldadores
@app.route('/generar_pdfsoldador')
def generar_pdfsoldador():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.image('static/logo.png', x=10, y=8, w=25)
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=24)
    pdf.cell(200, 10, txt="MECANICA INTEGRAL", ln=True, align='C')
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Registro de Asistencias para Soldadores", ln=True, align='C')
    pdf.set_font("Arial", size=12)

    # Obtener registros de asistencias de soldadores desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT soldadores.nombre, asistenciassoldador.estado, asistenciassoldador.fecha_hora FROM asistenciassoldador JOIN soldadores ON asistenciassoldador.soldador_id = soldadores.id")
    asistenciassoldador = cur.fetchall()
    cur.close()

    # Agregar los registros al PDF
    for asistenciassoldadors in asistenciassoldador:
        nombre = asistenciassoldadors['nombre']
        estado = asistenciassoldadors['estado']
        fecha_hora = asistenciassoldadors['fecha_hora'].strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, txt=f"Nombre: {nombre}, Estado: {estado}, Fecha y Hora: {fecha_hora}", ln=True, align='L')

         # Generar y agregar el código de barras
        codigo_barras = barcode.get_barcode_class('code128')
        codigo = codigo_barras(f'Nombre: {nombre}, Estado: {estado}, Fecha y Hora: {fecha_hora}', writer=ImageWriter())
        codigo_file = codigo.save('codigo_barras')

        # Insertar la imagen del código de barras centrada y en la parte inferior de la página
        pdf.image('codigo_barras.png', x=pdf.w/2-50, y=pdf.h - 50, w=100)

    # Guardar el PDF en el servidor
    pdf_output = "registro_asistencias_soldador.pdf"
    pdf.output(pdf_output)

    # Devolver el archivo para descarga
    return send_file(pdf_output, as_attachment=True)

# Generar PDF Lavador
@app.route('/generar_pdflavador')
def generar_pdflavador():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.image('static/logo.png', x=10, y=8, w=25)
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=24)
    pdf.cell(200, 10, txt="MECANICA INTEGRAL", ln=True, align='C')
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Registro de Asistencias para Lavadores", ln=True, align='C')
    pdf.set_font("Arial", size=12)

    # Obtener registros de asistencias de lavadores desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT lavadores.nombre, asistenciaslavador.estado, asistenciaslavador.fecha_hora FROM asistenciaslavador JOIN lavadores ON asistenciaslavador.lavador_id = lavadores.id")
    asistenciaslavador = cur.fetchall()
    cur.close()

    # Agregar los registros al PDF
    for asistenciaslavadors in asistenciaslavador:
        nombre = asistenciaslavadors['nombre']
        estado = asistenciaslavadors['estado']
        fecha_hora = asistenciaslavadors['fecha_hora'].strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(200, 10, txt=f"Nombre: {nombre}, Estado: {estado}, Fecha y Hora: {fecha_hora}", ln=True, align='L')

         # Generar y agregar el código de barras
        codigo_barras = barcode.get_barcode_class('code128')
        codigo = codigo_barras(f'Nombre: {nombre}, Estado: {estado}, Fecha y Hora: {fecha_hora}', writer=ImageWriter())
        codigo_file = codigo.save('codigo_barras')

        # Insertar la imagen del código de barras centrada y en la parte inferior de la página
        pdf.image('codigo_barras.png', x=pdf.w/2-50, y=pdf.h - 50, w=100)

    # Guardar el PDF en el servidor
    pdf_output = "registro_asistencias_lavador.pdf"
    pdf.output(pdf_output)

    # Devolver el archivo para descarga
    return send_file(pdf_output, as_attachment=True)

# Agregar Grafica
@app.route('/grafico_asistencias_mecanico')
def grafico_asistencias_mecanico():
    # Conectarse a la base de datos y obtener los datos
    cur = mysql.connection.cursor()
    query = """
    SELECT nombre, estado, DATE_FORMAT(fecha_hora, '%Y-%m-%d') as fecha, 
           DATE_FORMAT(fecha_hora, '%H:%i') as hora_salida
    FROM asistenciasmecanico
    JOIN mecanicos ON asistenciasmecanico.mecanico_id = mecanicos.id
    ORDER BY fecha_hora;
    """
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    # Preparar datos para el gráfico
    nombres = [x['nombre'] for x in result]
    estados = [x['estado'] for x in result]
    horas_salida = [x['hora_salida'] for x in result]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(nombres, horas_salida, color='blue')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Hora de Salida')
    ax.set_title('Hora de salida de los mecánicos')

    # Agregar etiquetas de datos
    for i in range(len(nombres)):
        ax.text(i, horas_salida[i], nombres[i], ha='center', va='bottom', rotation=90)

    # Convertir gráfico en una imagen PNG
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/grafico_asistencias_soldador')
def grafico_asistencias_soldador():
    # Conectarse a la base de datos y obtener los datos
    cur = mysql.connection.cursor()
    query = """
    SELECT nombre, estado, DATE_FORMAT(fecha_hora, '%Y-%m-%d') as fecha, 
           DATE_FORMAT(fecha_hora, '%H:%i') as hora_salida
    FROM asistenciassoldador
    JOIN soldadores ON asistenciassoldador.soldador_id = soldadores.id
    ORDER BY fecha_hora;
    """
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    # Preparar datos para el gráfico
    nombres = [x['nombre'] for x in result]
    estados = [x['estado'] for x in result]
    horas_salida = [x['hora_salida'] for x in result]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(nombres, horas_salida, color='green')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Hora de Salida')
    ax.set_title('Hora de salida de los soldadores')

    # Agregar etiquetas de datos
    for i in range(len(nombres)):
        ax.text(i, horas_salida[i], nombres[i], ha='center', va='bottom', rotation=90)

    # Convertir gráfico en una imagen PNG
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/grafico_asistencias_lavador')
def grafico_asistencias_lavador():
    # Conectarse a la base de datos y obtener los datos
    cur = mysql.connection.cursor()
    query = """
    SELECT nombre, estado, DATE_FORMAT(fecha_hora, '%Y-%m-%d') as fecha, 
           DATE_FORMAT(fecha_hora, '%H:%i') as hora_salida
    FROM asistenciaslavador
    JOIN lavadores ON asistenciaslavador.lavador_id = lavadores.id
    ORDER BY fecha_hora;
    """
    cur.execute(query)
    result = cur.fetchall()
    cur.close()

    # Preparar datos para el gráfico
    nombres = [x['nombre'] for x in result]
    estados = [x['estado'] for x in result]
    horas_salida = [x['hora_salida'] for x in result]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.bar(nombres, horas_salida, color='orange')
    ax.set_xlabel('Empleado')
    ax.set_ylabel('Hora de Salida')
    ax.set_title('Hora de salida de los lavadores')

    # Agregar etiquetas de datos
    for i in range(len(nombres)):
        ax.text(i, horas_salida[i], nombres[i], ha='center', va='bottom', rotation=90)

    # Convertir gráfico en una imagen PNG
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

#Generar archivos xml para mecanicos 
@app.route('/generar_xmlmecanico')
def generar_xmlmecanico():
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<asistencias>\n'

    # Obtener registros de asistencias desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT mecanicos.nombre, asistenciasmecanico.estado, asistenciasmecanico.fecha_hora FROM asistenciasmecanico JOIN mecanicos ON asistenciasmecanico.mecanico_id = mecanicos.id")
    asistenciasmecanico = cur.fetchall()
    cur.close()

    # Agregar los registros al XML
    for asistencia in asistenciasmecanico:
        nombre = asistencia['nombre']
        estado = asistencia['estado']
        fecha_hora = asistencia['fecha_hora'].strftime("%Y-%m-%d %H:%M:%S")
        xml_content += f'\t<asistencia>\n\t\t<nombre>{nombre}</nombre>\n\t\t<estado>{estado}</estado>\n\t\t<fecha_hora>{fecha_hora}</fecha_hora>\n\t</asistencia>\n'

    xml_content += '</asistencias>'

    # Guardar el XML en el servidor
    xml_output = "registro_asistencias_mecanico.xml"
    with open(xml_output, 'w') as xml_file:
        xml_file.write(xml_content)

    # Devolver el archivo para descarga
    return send_file(xml_output, as_attachment=True, mimetype='application/xml')


#Generar archivos xml para soldadores 
@app.route('/generar_xmlsoldador')
def generar_xmlsoldador():
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<asistencias>\n'

    # Obtener registros de asistencias desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT soldadores.nombre, asistenciassoldador.estado, asistenciassoldador.fecha_hora FROM asistenciassoldador JOIN soldadores ON asistenciassoldador.soldador_id = soldadores.id")
    asistenciassoldador = cur.fetchall()
    cur.close()

    # Agregar los registros al XML
    for asistencia in asistenciassoldador:
        nombre = asistencia['nombre']
        estado = asistencia['estado']
        fecha_hora = asistencia['fecha_hora'].strftime("%Y-%m-%d %H:%M:%S")
        xml_content += f'\t<asistencia>\n\t\t<nombre>{nombre}</nombre>\n\t\t<estado>{estado}</estado>\n\t\t<fecha_hora>{fecha_hora}</fecha_hora>\n\t</asistencia>\n'

    xml_content += '</asistencias>'

    # Guardar el XML en el servidor
    xml_output = "registro_asistencias_soldador.xml"
    with open(xml_output, 'w') as xml_file:
        xml_file.write(xml_content)

    # Devolver el archivo para descarga
    return send_file(xml_output, as_attachment=True, mimetype='application/xml')

#Generar archivos xml para lavadores 
@app.route('/generar_xmllavador')
def generar_xmllavador():
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<asistencias>\n'

    # Obtener registros de asistencias desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT lavadores.nombre, asistenciaslavador.estado, asistenciaslavador.fecha_hora FROM asistenciaslavador JOIN lavadores ON asistenciaslavador.lavador_id = lavadores.id")
    asistenciaslavador = cur.fetchall()
    cur.close()

    # Agregar los registros al XML
    for asistencia in asistenciaslavador:
        nombre = asistencia['nombre']
        estado = asistencia['estado']
        fecha_hora = asistencia['fecha_hora'].strftime("%Y-%m-%d %H:%M:%S")
        xml_content += f'\t<asistencia>\n\t\t<nombre>{nombre}</nombre>\n\t\t<estado>{estado}</estado>\n\t\t<fecha_hora>{fecha_hora}</fecha_hora>\n\t</asistencia>\n'

    xml_content += '</asistencias>'

    # Guardar el XML en el servidor
    xml_output = "registro_asistencias_lavador.xml"
    with open(xml_output, 'w') as xml_file:
        xml_file.write(xml_content)

    # Devolver el archivo para descarga
    return send_file(xml_output, as_attachment=True, mimetype='application/xml')



if __name__ == '__main__':
    app.run(debug=True)

