import sys
import MySQLdb
import csv
try:
    db = MySQLdb.Connect(host='localhost', user='root', password='', db='localidadesdb')
except MySQLdb.Error as err:
    print("No se pudo conectar a la base de datos:", err)
    sys.exit(1)
print("ConexiÃ³n correcta.")

with open('localidades.csv') as archivo_csv:
    lector_csv = csv.reader(archivo_csv, delimiter=',', quotechar='"')
    cabecera = next(lector_csv)
    localidades = []

    for fila in lector_csv:
        loc = {}
        for i in range(len(cabecera)):
            loc[cabecera[i]] = fila[i]
        localidades.append(loc)

    localidades_por_provincia = {}

    for loc in localidades:
        if loc['provincia'] not in localidades_por_provincia:
            localidades_por_provincia[loc['provincia']] = []
        localidades_por_provincia[loc['provincia']].append(loc)
    
    for pro in localidades_por_provincia:

        columnas = localidades_por_provincia[pro][0].keys()
        with open(f'localidad_provincia/{pro}.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columnas)
            writer.writeheader()
            
            writer.writerows(localidades_por_provincia[pro])

cursor = db.cursor()
nombres_provincias = list(localidades_por_provincia.keys())
create_table = "CREATE TABLE provincias (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))"
create_table_localidades = "CREATE TABLE localidades (provincia INT, id INT, localidad VARCHAR(255), cp VARCHAR(10), id_prov_mstr INT)"

try:
    cursor.execute("DROP TABLE IF EXISTS localidades")
    cursor.execute("DROP TABLE IF EXISTS provincias")
    cursor.execute(create_table)
    cursor.execute(create_table_localidades)

    for i, prov in enumerate(nombres_provincias, start=1):
        cursor.execute(f'INSERT INTO provincias (id, nombre) VALUES ("{i}", "{prov}")')
    db.commit()

    cursor.execute("SELECT * FROM provincias")
    id_provinces = dict(cursor.fetchall())
    db.commit()

    provinces_id = {v: k for k, v in id_provinces.items()}
    localidades_con_id = []

    for loca in localidades:
        localidades_con_id.append({
            **loca,
            "provincia": provinces_id[loca["provincia"]]
        })
    
    for loc in localidades_con_id:
        cursor.execute(f'INSERT INTO localidades (provincia, id, localidad, cp, id_prov_mstr) VALUES ({loc["provincia"]}, {loc["id"]}, "{loc["localidad"]}", "{loc["cp"]}", {loc["id_prov_mstr"]})')
    db.commit()

except Exception as e:
    print("Error: ", e)
    db.rollback()

db.close()