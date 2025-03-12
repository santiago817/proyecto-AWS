El primer paso era instalar Python 3.x, AWS CLI, Boto3 y Git
como ya tengo las herramientas a usar solo instale el Boto3 en Visual Code


Segundo paso crear un csv llamado Cliente.csv
y agregando esta informacion
 id_cliente, nombre_cliente, plan, fecha_inicio, fecha_fin, monto 
• 1, Cliente A, Plan Básico,2024-01-01,2024-12-31,25 
• 2, Cliente B, Plan Premium,2024-02-01,2024-12-31,50 


Tercer paso era cargar el csv a s3 bucket
voy al Servicio de s3 crear bucket me creo un nombre(los nombres son unicos asi q s3 te avisa si alguien esta usando ese nombre) al crearlo entras al bucket q creamos y cargamos nuestro csv guardamos y salimos


Cuarto paso tenia q usar AWS Glue donde tenia q crear un Crawler, lo primero q hice fue 
ir a AWS Glue ir a DataBase crear una database y despues a Crawlers crear crawlers , crear un nombre ,elegir la ruta de almacenamiento de s3 donde esta el Clientes.csv seleccionarlo,creamos un rol(ese rol lo tenemos q crear cuado nos pide hacerlo en el crawler porq si hacemos otro rol en IAM no lo va a reconocer)al crear un rol tenemos a ir a IAM, Roles buscamos el rol q creamos en crawlers y lo seleccionamos y vamos a agregar permisos y a asociar politicas, buscamos los persisos q nesesitamos q serian AdministratorAccess / AmazonS3FullAccess / AWSGlueConsoleFullAccess, una ves seleccionados los permisos q nesesitamos vamos a guardar. volvemos a aws glue
refrescamos para seleccionar el rol q creamos y lo seleccionamos despues le damos a Update chosen IAM role para q agregue todos los cambias q hicimos recientemente. ahora seleccionamos la base de datos q creamos despues lo seleccionamos y creamos el crawler. al crearlo vamos a darle Run Crawler esto proceso tarda , una ves q se haya iniciado aparecera en verde Ready! eso significa q ya se podria usar 

quinto Estando en el mismo servicio de Glue vamos a ETL jobs creamos un job visual para las conecciones de s3 a catalogo de datos en AWS Glue  en Sources(Fuentes) elegimos Amazon s3 y en Targets(objetivo) AWS Glue Data catalog se crearan unos cuadros conectaran automaticamente despues seleccionamos el cuadro de AWS Glue Data catalog  y rellenamos los requisitos para q funcione tanto el uso de la base de datos q creamos y la tabla q se creo al sacar la info de s3 despues de terminar con esos ajustes vamos al cuadro de s3 , nos pedira q busquemos nuestra tabla q esta en s3 elegir el tipo de formato si esta en JSON /CSV etc y nos pedira q usemos el rol de IAM q creamos al crear el CRAWLER en AWS Glue nos pedira q cambiemos el nombre de jobs guardamos y le damos a run , al cargar todo los datos nos aparecera la tabla q con la informacionq de nuestro s3 guardado en forma de tabla sql.

Sexto paso ir a AWS Athena para hacer una consulta, escribimos select * from Clientes_csv y le damos a ejecutar nos mostrara la tabla q se hizo en la grafica de jobs(si solo salta la tabla sola sin la informacion o no te sale la tabla es porq no le diste run a la grafica de jobs )


Septimo paso entrar a Amazon Redshift y vamos a crear cluster nos pedira q creemos un nombre en el 
tipo de nodo: usar el dc2.large por te cobra menos
Numeros de nodos : usar 1
Configuraciones de la base de datos: ahi nos estara dando un nombre para adm lo podemos cambiar o no
Roles de IAM asociados: aca creamos un rol y hacemos lo mismo ir a IAM ir a roles elegir el rol q recien creamos y ingresarle mas permisos de AdministratorAccess / AmazonS3FullAccess / AWSGlueConsoleFullAccess/RedShiftFullAccess lo guardamos y vamos al cluster de nuevoy le damos guardar
despues de q cargue el cluster q creamos (tarda mucho) entramos a nuestro cluster y vamos a hacer una coneccion despues de eso asociar algunos parametros q ya habiamos hecho y vamos a las 3 rayitas q estan ala ezquierda nos aparecera q estamamos usando el motor de consultas v2 tenemos q elegir la Version 1 (la version2 ocaciona problemas) una ves en el motor de consultas ejecutamos esto:

CREATE TABLE telecom_transformed (
    id_cliente INT, 
    nombre_cliente VARCHAR(256), 
    plan VARCHAR(255), 
    fecha_inicio DATE, 
    fecha_fin DATE, 
    monto DECIMAL(19, 2), 
    monto_total DECIMAL(10, 2)
);
al ejecutarlo nos aparecera q se a ejecutado de manera exitosa

Octavo paso ir a Amazon DynamoDB con el nombre de "pipeline-config" y contraseña "id_pipeline"
lo creamos y se ejecutara despues de eso vamos a Visual Studios y ejecutamos:

import boto3
from datetime import datetime

# Crear recurso DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pipeline-config')

# Insertar un ítem en la tabla
table.put_item(
    Item={
        'id_pipeline': 'pipeline_001',
        'status': 'Success',
        'timestamp': datetime.utcnow().isoformat()
    }
)

con esto nos respondera q esta conectado
con esto se finaliza rl proyecto.



------------------------------------------------------ O ---------------------------------------------------
Problemas: para hacer este proyecto tuve varios problemas ,al crearme una cuenta de AWS no me dejaba usar los servicios de pago, me habia creado max 3 cuentas y con el mismo problema , me prestaron una cuenta temporal y tuve problemas con athena no me salia la informacion solo la tabla al llegar a redshift tenia problemas de acceso la cuenta tempora no tenia permisos suficientes para usar ese servicio , problemas con redshift cuando pude resolver ese problema me salto otro y es q me tiraba error de IAM al querer crear una tabla nueva decia q le faltaban mas permisos ,problemas con Visual Studios al tener cuenta prestada no se me ejecutava la parte de boto3, lo q no pude resolver fue CloudWatch ademas de no saber como usarlo no lo hice por el costo que se me genero.

---------------------------------------------------------O--------------------------------------------------
Soluciones: un compañero me presto la cuenta para terminar mi proyecto.
athena : me habia salteado una parte tenia q entrar a jobs y unir las tablas y ejecutarlas asi cuando hacia la consulta de la tabla me saltaba el grafico

RedShift: con el problema de q ala cuenta temporal le faltaban mas permisos fue pedir la cuenta de un compañero
Redshift: al no querer ejecutar con un compañero reunidos solucionamos el problema y era q teniamos q ir al motor de consultas V1 y no ala V2(ese te da problemas)
Boto3:al querer ejecutar ese Script en Visual Studios me tiraba error y con el tutor resolvimos q era por problemas de q le faltaba hacer la conexion de AWS a Visual Code era entrar ala terminar poner AWS configure
poner la clave de acceso y demas cosas y ejecutar el Script de nuevo al hacer esto ya me saltaba q habia una conexion
