# TFG-Blockchaindatabase-Exploration
![GitHub](https://img.shields.io/github/license/franciscomirasg/TFG-Blockchaindatabase-Exploration-Release)

Este repositorio ha sido creado para publicar el codigo source del proyecto. En el repositorio privado se encuentra los commits realizados durante el desarrollo de la prueba de concepto.

El projecto hace uso de TAPLE: [TAPLE](https://www.taple.es/)

## Contenido

- La carpeta `doc` contiene el archivo PDF con la documentación del trabajo.
- La carpeta `src` contiene el código fuente del proyecto.

## Requisitos

- Python 3.11
- Docker
- LevelDb

## Uso

Para utilizar el código, se debe ejecutar desde la carpeta `src`.
Se recomienda el uso de Linux para este proyecto. 

### Instalación de requisitos

Para instalar los requisitos, se debe ejecutar el siguiente comando:

```bash
pip install -r requirements.txt
```

### Despliegue

Para el despliegue, ejecutar el script `deploy.sh`:

```bash
cd ..
chmod +x deploy.sh
./deploy.sh
```

### Ejecución Cliente

Para ejecutar uno de los clientes:
Los clientes se encuentran en la raiz de la carpeta `src`.

```bash
python3 client_<client_name>.py
```

#### Uso cliente
Una vez inicializado un cliente, se puede utilizar el siguiente comando para ver las opciones disponibles:

```bash
help
```

Para ver información adicional de un comando, se puede utilizar el siguiente comando:

```bash
<command> help
```

Se recomienda ejecutar primero el comando `init` para inicializar el cliente.

# Tareas a futuro
 - [ ] Convertir REST Adapter `utils/taple_connector.py` en libreria.
 - [ ] Reordenar interfaces de la API REST. Y Mover a la libreria.
 - [ ] Actualizar a TAPLE 0.2 cuando se publique.

<br>

# TFG-Blockchaindatabase-Exploration - English

This repository has been created to publish the source code of the project. The private repository contains the commits made during the development of the proof of concept.

The project makes use of TAPLE: [TAPLE](https://www.taple.es/)

## Contents

- The `doc` folder contains the PDF file with the documentation of the project.
- The `src` folder contains the source code of the project.

## Requirements

- Python 3.11
- Docker
- LevelDb

## Usage

To use the code, it must be executed from the `src` folder.
Linux is recommended for this project.

### Installation of Requirements

To install the requirements, run the following command:

```bash
pip install -r requirements.txt
```

### Deployment

For deployment, execute the `deploy.sh` script:

```bash
cd ..
chmod +x deploy.sh
./deploy.sh
```

### Client Execution

To execute one of the clients:
The clients can be found in the root of the `src` folder.

```bash
python3 client_<client_name>.py
```

#### Client Usage
Once a client is initialized, the following command can be used to see the available options:

```bash
help
```

To see additional information about a command, the following command can be used:

```bash
<command> help
```

It is recommended to first execute the `init` command to initialize the client.