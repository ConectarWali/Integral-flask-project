from os import getcwd, path
from flask import Flask
from flask_migrate import Migrate, migrate, upgrade, init
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

from src.config.config import Config

class Database_config(Config):

    MIGRATIONS_PATH ='database/migrations'

    def __init__(self, app:Flask)->None:
        super().__init__()
        self.__app:Flask = app
        self.__app_db:SQLAlchemy = SQLAlchemy(app)
        self.__migration = Migrate(app, self.__app_db, directory=self.MIGRATIONS_PATH)

    @property
    def app_db(self) -> SQLAlchemy: return self.__app_db

    @property
    def migration(self)->Migrate: return self.__migration

    def setup(self):
        uri:str = self.__app.config['SQLALCHEMY_DATABASE_URI']

        if not isinstance(uri, str): raise ValueError('Database URI must be string')
        
        if Config.FLASK_ENV == 'production':
            if not database_exists(uri):
                print("La base de datos no existe. Creándola...")
                create_database(uri)
                print("Base de datos creada con éxito.")
            else:
                print("La base de datos ya existe. Verificando estado de migraciones...")

            with self.__app.app_context():
                # Verifica si las migraciones están inicializadas
                migrations_dir = path.join(getcwd(), self.__migration.directory)
                if not path.exists(migrations_dir):
                    print("Migraciones no inicializadas. Ejecutando `init`...")
                    init()  # Inicializa la carpeta de migraciones
                    migrate()
                    print("Migraciones inicializadas.")
                else:
                    print("Migraciones ya están inicializadas.")

                # Verifica si hay migraciones pendientes
                try:
                    print("Aplicando migraciones pendientes...")
                    upgrade()  # Aplica las migraciones pendientes
                    print("Migraciones aplicadas con éxito.")
                except Exception as e:
                    print(f"No hay migraciones pendientes o ocurrió un error: {e}")
    

    