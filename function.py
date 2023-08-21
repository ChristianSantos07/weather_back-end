import requests
from collections import defaultdict
from datetime import datetime
import locale

#configração de localização para uso do datetime
locale.setlocale(locale.LC_TIME, 'pt_BR')

#Função anônima que retorna o icone do clima da api da open weather  - icon = codigo do icon recebido
#documentação = https://openweathermap.org/weather-conditions#How-to-get-icon-URL
format_logo = lambda icon: f'https://openweathermap.org/img/wn/{icon}@2x.png'

#Função anônima que retorna um icone do País da api flgas Api  - sigla country
#documentação = https://flagsapi.com/#quick
format_country = lambda country: f'https://flagsapi.com/{country}/shiny/64.png'


def convert_api_to_current_city(json):
    """

    Esta função recebe os dados obtidos da API d e os converte em um dicionário
    para representar informações sobre a cidade atual.

    Parâmetros:
    json (dict): Dados obtidos da API  em formato JSON.

    Retorna:
    dict: Um dicionário contendo informações sobre a cidade atual.
          Se os dados não puderem ser convertidos corretamente, um dicionário de erro é retornado.

    Exemplo de Uso:
    - json = {...}  # Dados obtidos da API 
      convert_api_to_current_city(json) retorna um dicionário formatado com informações sobre a cidade atual.
      

    """
    try:
        extrated_data = {
            "code": 1,
            "previsao": json["weather"][0]["description"],
            "icon": format_logo(json["weather"][0]["icon"]),
            "pais": format_country(json["sys"]["country"]),
            "vento": f'{json["wind"]["speed"]} Km/h',
            "umidade": f'{json["main"]["humidity"]}%',
            "temp": f'{json["main"]["temp"]} °C',
            "temp_max": f'{json["main"]["temp_max"]} °C',
            "temp_min": f'{json["main"]["temp_min"]} °C',
            "data": format_datetime(datetime.now()),
            "id": json["id"],
            "cidade": json.get("name", "")
        }
        return extrated_data
    except:
        return {"code": 0, "msg": "Desculpe, não encontramos essa cidade, tente novamente!"}

    


def format_datetime(data):
    """
    Esta função recebe um objeto de data/hora e formata a data.
    
    Parâmetros:
    data (datetime): Objeto de data/hora a ser formatado

    Retorna:
    str: Uma string contendo a data formatada no formato desejado no formato dia da semana(string), dia do mês(número), mês (string) ano(número).

    Exemplo de Uso:
    - data = datetime.datetime(2023, 8, 20, 14, 30)
      format_datetime(data) retorna "sábado, 20 de agosto de 2023"

    """
    # Crie o formato desejado
    format_desired = "%A, %d de %B de %Y"
    
    # Formate a data usando o formato desejado
    formatted_date = data.strftime(format_desired)

    return formatted_date

    
def convert_postgres_json(json):
    """
    Esta função recebe os dados de previsão de tempo armazenados em formato JSON, recuperados de uma consulta
    do banco de dados, e os converte em um formato mais limpo e organizado para consumir pela API.

    Parâmetros:
    json (dict): Dados de previsão de tempo armazenados em formato JSON.

    Retorna:
    dict: Um dicionário contendo informações de previsão de tempo.

    Exemplo de Uso:
    - json_data = {...}  # Dados de previsão de tempo em formato JSON
      convert_postgres_json(json_data) retorna o dicionario

    """
    try:
        clean_data = {
            "code": 1,
            "previsao": json.previsao,
            "icon": json.icon,
            "pais": json.pais,
            "vento": json.vento,
            "umidade": json.umidade,
            "temp": json.temp,
            "temp_max": json.temp_max,
            "temp_min": json.temp_min,
            "data": format_datetime(json.data),
            "id": json.id,
            "cidade": json.cidade
        }
        return clean_data
    except:
        return {"code": 0, "msg": "Desculpe, houve um erro ao tentar carregar a cidade, tente novamente!"}




def convert_postgres_historic(dados):
    """
    Converte os dados  obtidos do banco de dados em uma lista limpa.

    Esta função recebe os dados de histórico do postgres como tuplas,
    Essas tuplas dados são transformados em um formato mais limpo e organizado,
    onde cada registro é representado por um dicionário contendo identidade, cidade e data formatada.

    Parâmetros:
    dados (list): Uma lista de tuplas contendo os dados obtivo na consulta postgres

    Retorna:
    list: Uma lista de dicionários contendo os dados pronto para ser consumido pela API.

    Exemplo de Uso:
    - dados = [(1, 'Osório', '2023-08-20 10:00:00'), (2, 'Santa Catarina', '2023-08-20 15:00:00')]
      convert_postgres_historic(dados) retorna:
      [{'identidade': 1, 'cidade': 'Osório', 'data': '20/08/2023 10:00'},
       {'identidade': 2, 'cidade': 'Santa Catarina', 'data': '20/08/2023 15:00'}]

    """
    clean_data = []
    for identity, city, date in dados:
        data_dict = {
            "identidade": identity,
            "cidade": city,
            "data": format_datetime(date)
        }
        clean_data.append(data_dict)
    return clean_data


def forecast(data):
    """
    Esta função recebe os dados de previsão do tempo em formato JSON e os processa para gerar uma lista de previsões
    diárias. Exclui a previsão do dia atual e agrupa as previsões por dia, pegando a temperatura maxima e minima.

    Parâmetros:
    data (dict): Dados recebido na chamada da função

    Retorna:
    list: Uma lista de dicionários, onde cada dicionário contém informações de previsão para um dia específico.


    Exemplo de Uso:
    - json_data = {...}  # Dados de previsão do tempo em formato JSON
      forecast(json_data) retorna uma lista de dicionários com previsões diárias formatadas.

    """
    try: 
        daily_data = {}
        data_clean = []

        for item in data['list']:
            dt_txt = item['dt_txt']
            date = dt_txt.split()[0]
            
            #ignora se for o dia atual
            if date != str(datetime.now().date()):
                #se não tiver uma lista do dia atual, inseri
                if date not in daily_data:
                    daily_data[date] = {
                        'temp_max': item['main']['temp_max'],
                        'temp_min': item['main']['temp_min'],
                        'previsao': item['weather'][0]['description'],
                        'icon': format_logo(item['weather'][0]['icon']),
                        'vento': item['wind']['speed'],
                        'umidade': item['main']['humidity'],
                        'temp': item['main']['temp']
                    }
                else:
                    # Se já existe um registro para esse dia, atualize apenas se a temperatura máxima for maior
                    if item['main']['temp_max'] > daily_data[date]['temp_max']:
                        daily_data[date]['temp_max'] = item['main']['temp_max']
                    
                    # Atualize a temperatura mínima se for menor
                    if item['main']['temp_min'] < daily_data[date]['temp_min']:
                        daily_data[date]['temp_min'] = item['main']['temp_min']

        # Percorre a lista de item de dia, e inseri na lista para retornar a ApI
        for date, values in daily_data.items():
            format_data = {
                "previsao": values["previsao"],
                "vento": f'{values["vento"]} Km/h',
                "icon": values['icon'],
                "umidade": f'{values["umidade"]}%',
                "temp": f'{values["temp"]} °C',
                "temp_max": f'{values["temp_max"]} °C',
                "temp_min": f'{values["temp_min"]} °C',
                "data": format_datetime(datetime.strptime(date, '%Y-%m-%d')),   
            }
            data_clean.append(format_data)
        return data_clean
    except:
        return {"code": 0, "msg": "Desculpe, houve um erro ao tentar carregar as cidades, tente novamente!"}
