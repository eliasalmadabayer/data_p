from simple_salesforce import Salesforce
import requests
import numpy as np
import pandas as pd
from io import StringIO
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import tempfile
import os
import zipfile
import requests
import base64
import json

 

# Datos en formato CSV como cadena
datos_csv = '''
Submotivo;SLA dias laborales
Reconocimiento comercial por cobranza;10
Reconocimiento comercial 100% - 3 CP;10
Reconocimiento comercial por cobranza;10
Env�o de documento en PDF;1
Reclamo Env�o Liq. 1116 A/B;1
Publicidad y Patrocinio Institucional;1
Cuenta corriente;2
Facturar pedido de Clientes;2
Solicitud de Contratos;2
Alta o Extensi�n de Cuenta;2
Desconoce comprobante en Cta. Cte.;2
Desconoce NC/ND diferencia de cambio;2
Aspectos corporativos -de Industria;2
Comunidad - Semillero de Futuro;2
Distribuci�n - Consulta de CdeS;2
Comunicaci�n Interna;4
No interpreta resumen Cta. Cte.;5
Desconoce NC/ND por intereses;8
Documentaci�n Impositiva;8
Garant�as;11
Comisi�n �nica por Cobranza Canje;2
Comisi�n �nica por Cobranza Cash;2
Facturaci�n Contra Bono;2
Consulta Proceso de Pagos;3
Comisi�n Adicional;5
Comisi�n especial;5
Comisiones;5
Liquidaciones - Prepago;6
Liquidaciones - POD;9
Baja de pedidos;1
Bloqueo de despacho;1
Cambio de hibrido Grado (CHG);3
Carga Condici�n Comercial (Grower, Hipot, bonus);1
Carga de Fecha Vencimiento: DQ;2
Carga de N015/N030;1
Carga de Fecha Vencimiento: N060/N090;1
Carga de pedido Reintegro;2
Carga de pedidos clientes;2
Customer Acomodation;1
Desbloqueo de despacho;1
Documentos Financieros;3
Emergencia;5
Facturaci�n - Reclama NC IIBB;5
Facturar pedido CdeS y Cta Asociada;1
Facturar pedido de Clientes;1
Financiaci�n en pesos;2
Garant�as;5
Modificaci�n Destino del pedido;1
NC Anulaci�n Parcial;7
NC Anulaci�n Total;7
NC Descuento Reward;7
"NC Devoluci�n ""Virtual""";10
NC Devoluci�n Real;15
NC Diferencia Precio;7
Presiembra;1
Reclamo de Puntos Impulso Bayer x Distribuidor;2,333333333
Grado de conformidad de Performance;1
Carga de pedido CPP;1
Carga de pedidos CdeS;1
ND (CUI);1
Packaging;3
Desbloqueo de despacho;1
NC Anulaci�n Total;7
Reclama aplicaci�n de saldos;1
NC Diferencia Precio;7
Carga de pedidos clientes;1
NC Anulaci�n Parcial;7
Garant�as/Cant. De producto incorrecto- Producto faltante;2,333333333
Solicita Prioridad de Despacho;2,333333333
Env�o de documento en PDF;2,333333333
Facturaci�n - Reclama NC IIBB;5
Consulta Despacho de Pedido;2,333333333
Carga de pedidos CdeS;1
Reclama NC - Anulaci�n intereses;2
Cantidad de producto Incorrecta o Faltante;2,333333333
Modificaci�n de CdeS que Comisiona (ZI);1
Documentos financieros;1
Facturar pedido CdeS y Cta Asociada;1
Baja de pedidos;1
Facturar pedido de Clientes;1
Carga de pedido CPP;1
'''

# Crear un objeto StringIO para simular un archivo
datos_stream = StringIO(datos_csv)

# Cargar el DataFrame desde el objeto StringIO
sla_cs = pd.read_csv(datos_stream, encoding="latin1", sep=";")

# Obtener la fecha y hora actual
fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')

#LOGUEO A SALESFORCE GLOBAL
sf = Salesforce(username='elias.almada.ext@bayer.com.global',password='Isaac21042017#', security_token='')
sf_instance = 'https://bayer-global.my.salesforce.com/' #Your Salesforce Instance URL

print('descargando BASE CALL CENTER E2C')
#DESCARGA BASE CALL CENTER E2C
reportId = '00O3t000008rHozEAE' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
e2c_call_incentivos_chile= pd.read_csv(StringIO(download_report))
print('descarga BASE CALL CENTER E2C OK')



print('descargando BASE E2C MONSANTO BAYER E INVENTARIOS')

#DESCARGA BASE E2C MONSANTO BAYER E INVENTARIOS
reportId = '00O3t000008rK4wEAE' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
e2c_mon_bay_inv = pd.read_csv(StringIO(download_report))
print('descarga BASE E2C MONSANTO BAYER E INVENTARIOS OK')


# Obtener la fecha y hora actual
#fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')

#LOGUEO A SALESFORCE
sf = Salesforce(username='elias.almada.ext@bayer.com',password='Benja123$', security_token='wvEJIhaPu7X6QKjI15IZxPBt')
sf_instance = 'https://las-monsanto.my.salesforce.com/' #Your Salesforce Instance URL
print('descargando BASE CALL CENTER SF LOCAL')
#DESCARGA BASE CALL CENTER SF LOCAL
reportId = '00O6f000007nxSN' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
sf_callcenter = pd.read_csv(StringIO(download_report))
sf_callcenter = sf_callcenter.iloc[:-7]
print('descarga BASE CALL CENTER SF LOCAL OK')


#DESCARGA BASE MONSANTO Y BAYER LEGACY
print('descargando BASE MONSANTO Y BAYER LEGACY SF LOCAL')
sf_instance = 'https://las-monsanto.my.salesforce.com/' #Your Salesforce Instance URL
reportId = '00O6f000007nyBr' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
sf_cs_mon_bay = pd.read_csv(StringIO(download_report))
sf_cs_mon_bay = sf_cs_mon_bay.iloc[:-7]
print('descarga BASE MONSANTO Y BAYER LEGACY SF LOCAL OK')


#DESCARGA BASE INCENTIVOS
print('descargando BASE INCENTIVOS SF LOCAL')
sf_instance = 'https://las-monsanto.my.salesforce.com/' #Your Salesforce Instance URL
reportId = '00O6f000007nxSI' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
sf_incentivos = pd.read_csv(StringIO(download_report))
sf_incentivos = sf_incentivos.iloc[:-7]
print('descarga INCENTIVOS SF LOCAL OK')


#DESCARGA BASE INVENTARIOS
print('descargando BASE INVENTARIOS SF LOCAL')
sf_instance = 'https://las-monsanto.my.salesforce.com/' #Your Salesforce Instance URL
reportId = '00O6f000007nyBh' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
sf_inventarios = pd.read_csv(StringIO(download_report))
sf_inventarios = sf_inventarios.iloc[:-7]
print('descarga INVENTARIOS SF LOCAL OK')


print('Trabajando las bases, aguarde por favor')

#TRANSFORMAR DATOS DE DATAFRAME SALESFORCE MONSANTO LEGACY Y BAYER LEGACY
sf_mon_bay_inv = sf_cs_mon_bay
sf_mon_bay_inv = sf_mon_bay_inv.astype(str)
sf_mon_bay_inv.columns = ["Column1","Column2","Column3","Column4","Column5","Column6","Column7","Column8","Column9","Column10", "Column11","Column12","Column13","Column14","Column15"]
sf_mon_bay_inv = sf_mon_bay_inv.iloc[:-7]
sf_mon_bay_inv['Linea de negocios'] = "Monsanto Legacy"
sf_mon_bay_inv['Linea de negocio'] = sf_mon_bay_inv.apply(lambda row: "Bayer Legacy" if "Bayer" in row['Column8'] else row['Linea de negocios'], axis=1)
sf_mon_bay_inv = sf_mon_bay_inv.drop("Linea de negocios", axis=1)
sf_mon_bay_inv["Origen"] = "Salesforce"

#TRANSFORMAR DATOS DE DATAFRAME SALESFORCE CALLCENTER
sf_callcenter = sf_callcenter.astype(str)
sf_callcenter.columns = ["Column1","Column2","Column3","Column4","Column5","Column6","Column7","Column8","Column9","Column10", "Column11","Column12","Column13","Column14","Column15"]
sf_callcenter = sf_callcenter.iloc[:-7]
sf_callcenter["Linea de negocio"] = "Call Center"
sf_callcenter["Origen"] = "Salesforce"

#TRANSFORMAR DATOS DE DATAFRAME SALESFORCE INCENTIVOS
sf_incentivos = sf_incentivos.astype(str)
sf_incentivos.columns = ["Column1","Column2","Column3","Column4","Column5","Column6","Column7","Column8","Column9","Column10", "Column11","Column12","Column13","Column14","Column15"]
sf_incentivos["Linea de negocio"] = "Incentivos"
sf_incentivos = sf_incentivos.iloc[:-7]
sf_incentivos["Origen"] = "Salesforce"

#TRANSFORMAR DATOS DE DATAFRAME SALESFORCE INVENTARIOS
sf_inventarios = sf_inventarios.astype(str)
sf_inventarios.columns = ["Column1","Column2","Column3","Column4","Column5","Column6","Column7","Column8","Column9","Column10", "Column11","Column12","Column13","Column14","Column15"]
sf_inventarios = sf_inventarios.iloc[:-7]
sf_inventarios["Linea de negocio"] = "Inventarios"
sf_inventarios["Origen"] = "Salesforce"

#TRANSFORMAR DATOS DE DATAFRAME ACS CALL_INCENTIVOS_CHILE
e2c_call_incentivos_chile = e2c_call_incentivos_chile.astype(str)
e2c_call_incentivos_chile= e2c_call_incentivos_chile.iloc[:-7]
e2c_call_incentivos_chile.columns= ["Column1","Column2","Column3","Column4","Column5","Column6","Column7","Column8","Column9","Column10", "Column11","Column12","Column13","Column14","Column15"]
e2c_call_incentivos_chile['Linea de negocio'] = e2c_call_incentivos_chile['Column2'].apply(lambda x: "Chile CS" if "Chile" in x else ("Call Center" if "Call" in x else "Incentivos"))
e2c_call_incentivos_chile["Origen"] = "Correo"

#TRANSFORMAR DATOS DE DATAFRAME ACS MONSANTO LEGACY BAYER LEGACY E INVENTARIOS
e2c_mon_bay_inv = e2c_mon_bay_inv.astype(str)
e2c_mon_bay_inv = e2c_mon_bay_inv.iloc[:-7]
e2c_mon_bay_inv.columns = ["Column1","Column2","Column3","Column4","Column5","Column6","Column7","Column8","Column9","Column10", "Column11","Column12","Column13","Column14","Column15"]
e2c_mon_bay_inv = e2c_mon_bay_inv[~e2c_mon_bay_inv['Column2'].str.contains('AR CUSTOMER OPERATION EXIMIA')]
e2c_mon_bay_inv["Linea de negocios"] = "Monsanto Legacy"
e2c_mon_bay_inv['Column8'] = e2c_mon_bay_inv['Column8'].astype(str)
e2c_mon_bay_inv['Linea de negocio'] = e2c_mon_bay_inv.apply(lambda row: "Bayer Legacy" if "Bayer" in row['Column8'] else row["Linea de negocios"], axis=1)
e2c_mon_bay_inv = e2c_mon_bay_inv.drop("Linea de negocios", axis=1)
e2c_mon_bay_inv["Origen"] = "Correo"
e2c_mon_bay_inv["Nueva_Columna"] = e2c_mon_bay_inv["Column8"] + e2c_mon_bay_inv["Column9"]
e2c_mon_bay_inv["Nueva_Categoria"] = e2c_mon_bay_inv["Nueva_Columna"].apply(lambda x: 
    "Licencias Maíz" if x == "LicenciatarioAR01 - Corn LicenseLicenciatario" else (
    "Licencias Soja" if x == "AR01 - Soybean LicenseLicenciatario" else (
    "Dekalb" if x == "AR01 - DekalbSemillas" else (
    "Monsanto Crop Protection" if x == "AR01 - Roundup/SelectivosProtección de cultivos" else (
    "La Tijereta - Semillas" if x == "AR03 - La TijeretaSemillas" else (
    "La Tijereta - Agroquimicos" if x == "AR03 - La TijeretaProtección de cultivos" else (
    "Intacta" if x in ["AR04 - Intacta RetailerCaptura de Valor", "AR04 - Intacta PODCaptura de Valor"] else (
    "BioAg" if x == "AR05 - BioAgBiologicos" else (
    "Bayer Crop Protection" if x == "Bayer - Crop ProtectionProtección de cultivos" else ""
    )))))))))
# Eliminar las columnas "Column8" y "Column9"
e2c_mon_bay_inv.drop(columns=["Column8", "Column9", "Nueva_Columna"], inplace=True)

# Cambiar el nombre de la columna "Nueva_Columna" a "Column8"
e2c_mon_bay_inv.rename(columns={"Nueva_Categoria": "Column8"}, inplace=True)

# Reordenar las columnas para poner "Column8" en la octava posición
column_order = list(e2c_mon_bay_inv.columns)
column_order.insert(7, column_order.pop(column_order.index("Column8")))
e2c_mon_bay_inv = e2c_mon_bay_inv[column_order]

#CONCATENAR LOS 4 DATAFRAME DE SALESFORCE Y TRANSFORMAR
Base_de_datos = pd.concat ([sf_mon_bay_inv, sf_callcenter, sf_incentivos,sf_inventarios], axis = 0)
Base_de_datos['Column6'] = pd.to_datetime(Base_de_datos['Column6'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
Base_de_datos['Column7'] = pd.to_datetime(Base_de_datos['Column7'], format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
Base_de_datos['Column14'] = pd.to_datetime(Base_de_datos['Column14'], format='%d/%m/%Y %H:%M')
Base_de_datos['Column15'] = pd.to_datetime(Base_de_datos['Column15'], format='%d/%m/%Y %H:%M')
Base_de_datos['Diferencia'] = Base_de_datos['Column15'] - Base_de_datos['Column14']
Base_de_datos['Estado SLA'] = np.where(
Base_de_datos['Diferencia'].isnull(), "Sin SLA establecido", np.where(Base_de_datos['Diferencia'] > pd.Timedelta(0),"Fuera de SLA","Dentro de SLA"))
base_sf = Base_de_datos

#CONCATENAR LOS 2 DATAFRAME DE ACS Y TRANSFORMAR
Base_de_datos = pd.concat ([e2c_call_incentivos_chile, e2c_mon_bay_inv], axis = 0)
Base_de_datos = Base_de_datos.astype(str)
Base_de_datos['Column6'] = pd.to_datetime(Base_de_datos['Column6'], dayfirst=True, format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
Base_de_datos['Column7'] = pd.to_datetime(Base_de_datos['Column7'], dayfirst=True, format='%d/%m/%Y').dt.strftime('%d/%m/%Y')
Base_de_datos['Column14'] = pd.to_datetime(Base_de_datos['Column14'], dayfirst=True, format='%d/%m/%Y %H:%M')
Base_de_datos['Column15'] = pd.to_datetime(Base_de_datos['Column15'], dayfirst=True, format='%d/%m/%Y %H:%M')
Base_de_datos['Diferencia'] = Base_de_datos['Column15'] - Base_de_datos['Column14']
Base_de_datos['Estado SLA'] = "Sin SLA establecido"
base_e2c = Base_de_datos
base_e2c = base_e2c.merge(sla_cs[['Submotivo', 'SLA dias laborales']], 
                          left_on='Column4', 
                          right_on='Submotivo', 
                          how='left')
base_e2c = base_e2c.drop("Submotivo", axis=1)

#CONCATENAR LOS DATAFRAME  FINALES DE SALESFORCE Y ACS

basefiltrada = pd.concat([base_sf, base_e2c])

#ELIMINAR COLUMNAS PARA QUE NOS QUEDEN LAS QUE USAN REPORTING EN POWER BI
basefiltrada.drop(columns=["Column2", "Column7", "Column9", "Column10" , "Column11" , "Column12", "Column14", "Column15", "Diferencia", "SLA dias laborales"], inplace=True)

#REORDENAR COLUMNAS PARA QUE NOS QUEDEN LAS QUE USAN REPORTING EN POWER BI
basefiltrada = basefiltrada[["Column1", "Column3", "Column4", "Origen", "Column6", "Column5", "Column8", "Column13", "Linea de negocio", "Estado SLA"]]

#RENOMBRAR COLUMNAS PARA QUE NOS QUEDEN LAS QUE USAN REPORTING EN POWER BI
basefiltrada.columns = ["Todos los tickets","Razon Secundaria","Razon Terciaria","Origen del caso","Fecha Apertura","Estado Ticket","Organización de Ventas","Tkt conca","Linea de Negocio","Estado SLA"]



# Cargar el DataFrame desde el archivo CSV original
#LOGUEO A SALESFORCE GLOBAL
sf = Salesforce(username='elias.almada.ext@bayer.com.global',password='Isaac21042017#', security_token='')
sf_instance = 'https://bayer-global.my.salesforce.com/' #Your Salesforce Instance URL


print('descargando BASE pybo')
#DESCARGA BASE PYBO POR CASOS HISTORICOS
reportId = '00OUQ0000010wD72AI' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
pybo_historico2= pd.read_csv(StringIO(download_report))
print('descarga BASE PYBO HISTORICO OK')



print('descargando BASE pybo')
#DESCARGA BASE PYBO POR CASOS
reportId = '00OUQ0000010tvB2AQ' # add report id
export = '?isdtp=p1&export=1&enc=UTF-8&xf=csv'
sfUrl = sf_instance + reportId + export
response = requests.get(sfUrl, headers=sf.headers, cookies={'sid': sf.session_id})
download_report = response.content.decode('utf-8')
pybo_casos2= pd.read_csv(StringIO(download_report))
print('descarga BASE PYBO POR CASOS HISTORICO OK')

pybo_casos = pybo_casos2.head(-5)
pybo_historico = pybo_historico2.head(-5)

pybo_historico["Número del caso"] = pybo_historico["Número del caso"].astype(int)
pybo_casos["Número del caso"] = pybo_casos["Número del caso"].astype(int)

pybo_casos = pybo_casos[["Número del caso","Nombre de la cuenta","Antigüedad (Minutos)"]]

tablas_cruzadas = pd.merge(pybo_historico, pybo_casos, how='left', left_on='Número del caso', right_on='Número del caso')

tablas_cruzadas.columns = ['Número del caso', 'Propietario del caso', 'Campo / Evento',
       'Modificado por', 'Valor anterior', 'Valor nuevo',
       'Fecha de modificación', 'Nombre de la Cuenta', 'Asunto',
       'Fecha/Hora de apertura', 'Fecha de apertura', 'Modificado por alias',
       'Alias del propietario del caso', 'Estado', 'Origen del caso',
       'Razón secundaria', 'Razón Terciaria', 'Línea de Negocio', 'Antigüedad',
       'Source System Case ID', 'Canal distribución', 'Nombre de la cuenta',
       'Antigüedad (Minutos)']

tablas_cruzadas = tablas_cruzadas[['Número del caso', 'Propietario del caso', 'Campo / Evento',
       'Modificado por', 'Valor anterior', 'Valor nuevo',
       'Fecha de modificación', 'Nombre de la Cuenta', 'Asunto',
       'Fecha/Hora de apertura', 'Fecha de apertura', 'Modificado por alias',
       'Alias del propietario del caso', 'Estado', 'Origen del caso',
       'Razón secundaria', 'Razón Terciaria', 'Línea de Negocio',
       'Source System Case ID', 'Canal distribución', 'Nombre de la cuenta',
       'Antigüedad (Minutos)']]


# Crear una lista de pares de DataFrame y nombres de archivo correspondientes
dataframes = [
    (basefiltrada, "basefiltrada.csv"),
    (tablas_cruzadas, "basefiltrada_pybo.csv")
]

# Crear un archivo temporal ZIP
with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
    # Crear un objeto ZipFile
    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Iterar sobre los DataFrames y agregar los archivos CSV al ZIP
        for df, filename in dataframes:
            temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            df.to_csv(temp_csv.name, index=False, encoding='utf-16')
            zipf.write(temp_csv.name, arcname=filename)



# Configuración de GitHub
GITHUB_TOKEN = "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"  # Reemplaza con tu token de acceso personal
REPO_OWNER = "eliasalmadabayer"
REPO_NAME = "data_p"
BRANCH_NAME = "main"
zip_filename = "archivo.zip"  # Nombre del archivo ZIP que deseas subir

# Obtener el SHA del archivo existente
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{zip_filename}"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    file_info = response.json()
    sha = file_info['sha']  # Obtén el SHA del archivo
    print(f"SHA del archivo existente: {sha}")
else:
    print(f"Archivo no encontrado, se creará uno nuevo.")
    sha = None  # Si no se puede obtener el SHA, se creará el archivo

# Crear un archivo ZIP temporal
with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
    # Crear un objeto ZipFile
    with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Iterar sobre los DataFrames y agregar los archivos CSV al ZIP
        for df, filename in dataframes:
            temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            df.to_csv(temp_csv.name, index=False, encoding='utf-16')
            zipf.write(temp_csv.name, arcname=filename)

    # Leer el contenido del ZIP
    with open(temp_zip.name, "rb") as zip_file:
        content = zip_file.read()

# Codificar el contenido en base64
encoded_content = base64.b64encode(content).decode()

# Crear el payload para la API de GitHub
payload = {
    "message": "Actualizando archivo ZIP de datos",
    "content": encoded_content,
    "branch": BRANCH_NAME
}

if sha:
    payload["sha"] = sha  # Incluir el SHA si el archivo existe

# Hacer la solicitud a la API de GitHub
response = requests.put(url, headers=headers, data=json.dumps(payload))

if response.status_code in [200, 201]:
    print("Archivo ZIP subido exitosamente a GitHub.")
else:
    print(f"Error al subir el archivo: {response.status_code} - {response.text}")

print("script ejecutado con éxito")
