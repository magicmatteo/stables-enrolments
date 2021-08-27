from configparser import ConfigParser
from mainapp import app
filepath = app.root_path + '/config/database.ini'

def config(filename=filepath, section='database'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db2 = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db2[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db2

def db_uri(filename=filepath, section='database'):
    
    # This is only really for Postgres at the moment.. Edit depending on db
    
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    if parser.has_section(section):
        db2 = {}
        params = parser.items(section)
        for param in params:
            db2[param[0]] = param[1]
        return f"postgresql://{db2['user']}:{db2['password']}@{db2['host']}:5432/{db2['database']}"
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))