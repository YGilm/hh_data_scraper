import configparser


def config(filename='database.ini', section='postgresql'):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db_config = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'Секция {section} не найдена в файле {filename}')

    return db_config
