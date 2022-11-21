import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def get_db():
    # SI DB NO ESTÁ EN G, CREAMOS LA BBDD
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
            
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
    
def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    
    db.commit()

# creamos ahora la funcion que nos construye la bbdd desde la línea de comandos
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Base de datos inicializada")

def init_app(app):
    # preparamos la bbdd para que se cierre tras cada uso y añadimos comando ejecutable en línea de comandos
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)






