import pyodbc
from faker import Faker
import random
from datetime import date, timedelta

# Inicializar Faker para generar datos ficticios
fake = Faker('es_ES')

# Conexión a la base de datos SQL Server
def conectar_bd():
    try:
        connection = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=JOSE_TUN\SQLEXPRESS;"       # Reemplaza con tu nombre de servidor
            "DATABASE=BD3FINAL;"                # Nombre de la base de datos
            "Trusted_Connection=yes;"           # Autenticación Windows
        )
        print("Conexión exitosa a la base de datos.")
        return connection
    except pyodbc.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Generar fechas aleatorias
def generar_fecha_aleatoria(start_year=1990, end_year=2005):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

# Insertar estudiantes
def insertar_estudiantes(connection, num_registros):
    cursor = connection.cursor()
    for _ in range(num_registros):
        nombre = fake.first_name()
        apellido = fake.last_name()
        email = fake.unique.email()
        fecha_nacimiento = generar_fecha_aleatoria()
        
        # Asegurarse de que la fecha sea compatible con SQL Server
        fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')
        
        query = """
        INSERT INTO Estudiantes (Nombre, Apellido, Email, FechaNacimiento)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, apellido, email, fecha_nacimiento_str))
    connection.commit()
    cursor.close()
    print("Estudiantes insertados.")

# Insertar profesores
def insertar_profesores(connection, num_registros):
    especialidades = ["Matemáticas", "Física", "Química", "Biología", "Historia", "Literatura", "Informática"]
    cursor = connection.cursor()
    for _ in range(num_registros):
        nombre = fake.first_name()
        apellido = fake.last_name()
        especialidad = random.choice(especialidades)
        
        query = """
        INSERT INTO Profesores (Nombre, Apellido, Especialidad)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (nombre, apellido, especialidad))
    connection.commit()
    cursor.close()
    print("Profesores insertados.")

# Insertar cursos
def insertar_cursos(connection, num_registros):
    nombres_cursos = ["Álgebra I", "Cálculo", "Física I", "Química Orgánica", "Historia Antigua", "Literatura Clásica"]
    cursor = connection.cursor()
    for _ in range(num_registros):
        nombre_curso = random.choice(nombres_cursos)
        creditos = random.randint(3, 6)
        profesor_id = random.randint(1, 100)  # Asumiendo que hay 100 profesores
        
        query = """
        INSERT INTO Cursos (NombreCurso, Creditos, ProfesorID)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (nombre_curso, creditos, profesor_id))
    connection.commit()
    cursor.close()
    print("Cursos insertados.")

# Insertar matrículas
def insertar_matriculas(connection, num_registros):
    cursor = connection.cursor()
    for _ in range(num_registros):
        estudiante_id = random.randint(1, 1000)  # Asumiendo que hay 1000 estudiantes
        curso_id = random.randint(1, 200)       # Asumiendo que hay 200 cursos
        fecha_matricula = fake.date_between(start_date='-2y', end_date='today')
        
        # Asegurarse de que la fecha sea compatible con SQL Server
        fecha_matricula_str = fecha_matricula.strftime('%Y-%m-%d')
        
        query = """
        INSERT INTO Matriculas (EstudianteID, CursoID, FechaMatricula)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (estudiante_id, curso_id, fecha_matricula_str))
    connection.commit()
    cursor.close()
    print("Matrículas insertadas.")

# Insertar calificaciones
def insertar_calificaciones(connection, num_registros):
    cursor = connection.cursor()
    for _ in range(num_registros):
        matricula_id = random.randint(1, 2000)  # Asumiendo que hay 2000 matrículas
        tarea = round(random.uniform(0, 100), 2)
        examen1 = round(random.uniform(0, 100), 2)
        examen2 = round(random.uniform(0, 100), 2)
        proyecto = round(random.uniform(0, 100), 2)
        
        query = """
        INSERT INTO Calificaciones (MatriculaID, Tarea, Examen1, Examen2, Proyecto)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (matricula_id, tarea, examen1, examen2, proyecto))
    connection.commit()
    cursor.close()
    print("Calificaciones insertadas.")

# Función principal
def main():
    connection = conectar_bd()
    if connection:
        # Insertar datos en las tablas
        insertar_estudiantes(connection, 1000)  # 1000 estudiantes
        insertar_profesores(connection, 100)   # 100 profesores
        insertar_cursos(connection, 200)       # 200 cursos
        insertar_matriculas(connection, 2000)  # 2000 matrículas
        insertar_calificaciones(connection, 3000)  # 3000 calificaciones
        connection.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()