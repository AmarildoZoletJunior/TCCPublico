from configparser import ConfigParser
import os

# Caminho absoluto para o arquivo de configuração
config_file = r'C:\Users\amjun\Desktop\Catolica\TCC\TCCPublico\BackEnd\src\config\conf.ini'

# Inicializa o ConfigParser
conf_obj = ConfigParser()

# Verifica se o arquivo existe
if os.path.exists(config_file):
    conf_obj.read(config_file)
else:
    raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_file}")

try:
    # Acessando a seção 'DataBase'
    if 'DataBase' in conf_obj:
        config = conf_obj['DataBase']
        DRIVER = config.get('DRIVER', None)
        SERVER = config.get('SERVER', None)
        DATABASE = config.get('DATABASE', None)

        # Verifica se as chaves foram corretamente obtidas
        if DRIVER is None or SERVER is None or DATABASE is None:
            raise ValueError("Alguma chave está faltando na seção [DataBase].")

    # Acessando a seção 'Parametros'
    if 'Parametros' in conf_obj:
        config = conf_obj['Parametros']
        CHAVE = config.get('ChaveJWT', None)

        # Verifica se a chave foi obtida
        if CHAVE is None:
            raise ValueError("Chave 'ChaveJWT' não encontrada na seção [Parametros].")
    else:
        raise ValueError("Seção 'Parametros' não encontrada no arquivo de configuração.")

except Exception as e:
    print(f"Erro ao ler o arquivo de configuração: {e}")
