import csv
import sys
import MySQLdb

# Conecion con la base de datos
try:
    db = MySQLdb.Connect(host='localhost', user='root', password='', db='localprovdb')
except MySQLdb.Error as e:
    print("No se pudo conectar a la base de datos:", e)
    sys.exit(1)
print("Conexión correcta.")

# se lee el archivo CSV y se le  da formato de diccionario
with open('localidades.csv') as archivo_csv:
    lector_csv = csv.reader(archivo_csv, delimiter=',', quotechar='"')
    cabecera = next(lector_csv)
    localidades = []
    for fila in lector_csv:
        loc = {}
        for i in range(len(cabecera)):
            loc[cabecera[i]] = fila[i]
        localidades.append(loc)
    print("El CSV  ha sido leido correctamente.")
cursor = db.cursor()

# Todas las consultas para la base de datos
create_table_localidades = "CREATE TABLE localidades (provincia VARCHAR(255), id INT, localidad VARCHAR(255), cp VARCHAR(10), id_prov_mstr INT)"
select_all_provinces = "SELECT provincia AS 'Provincia', COUNT(*) AS 'Localidades' FROM `localidades` GROUP BY provincia"
drop_if_exists = "DROP TABLE IF EXISTS localidades"
insert_localidades = 'INSERT INTO localidades (provincia, id, localidad, cp, id_prov_mstr) VALUES (%s, %s, %s, %s, %s)'
select_localidades = 'SELECT * FROM localidades WHERE provincia = %s'
try:
    # si la tabla ya exite se borra y se vuelve a crear
    cursor.execute(drop_if_exists)
    cursor.execute(create_table_localidades)
    print("Tabla creada con exito.")
    # Insertamos todos los registros de localidades
    for loc in localidades:
        valores = [loc["provincia"], loc["id"], loc["localidad"], loc["cp"], loc["id_prov_mstr"]]
        cursor.execute(insert_localidades, valores)
    db.commit()
    print("Registros  fueron insertadoscon exito")

    #7provincias junto a  la cantidad de localidades de cada una
    cursor.execute(select_all_provinces)
    provinces_localities = dict(cursor.fetchall())
    all_provinces = list(provinces_localities.keys())
    # Traemos todas las localidades de cada una de las provincias
    for prov in all_provinces:
        cursor.execute(select_localidades, [prov])
        locs = list(cursor.fetchall())
        # escribimos los resultados en un archivo CSV para cada una de las provincias, 
        # primero la cabecera, todas las localidades y por ultimo el total de localidades
        with open(f'localidad_provincia/{prov}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)   
            writer.writerow(cabecera)
            writer.writerows(locs)
            writer.writerow(["la totalidad de localidades: " + str(provinces_localities[prov])])

    print("Los CSVs han sido  creados con exito.")

except Exception as e:
    print("Error: ", e)
    db.rollback()

db.close()