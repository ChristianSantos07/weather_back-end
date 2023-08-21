#Import de bibliotecas e modulos
from flask import Flask, jsonify, request
import requests
from function import (
    convert_api_to_current_city,
    convert_postgres_historic,
    convert_postgres_json,
    forecast
)
from crud import (
    insert_weather_historic,
    get_data_historic,
    list_historic_identify
)


#cria uma intância do Flask
app = Flask(__name__)

#chave api da Open Weather
API_KEY = "eb7162fd4bef5a8bf3a2f3ad86984996"


def get_weather_data(city_name, current_day=True):
    """
    Obtém dados meteorológicos da API OpenWeatherMap com base no nome da cidade fornecido.
    
    Parâmetros:
    city_name (string): Cidade que é recebido no campo de pesquisa pela api do frontend
    current_day (bool, opcional): Confiuração da api para o API_PATH, por padrão é True, busca os dados para a o dia atual, de for False, busca para os próximos 5 dias,
                        dependendo do hórario o dia de hoje também é incluso

    Atributos (chave  = descrição):
    APi_PATH: weather = Previsão do clima do dia atual
              forecast =  Previsão do clima dos proximos dias
              q = (city_name) Recebe o valor de nome da cidade
              appid = (API_KEY) chave de API
              lang = (pt_br) variante da linguagem(português Brasil)
              units = (metric) Unidade de medida em Graus Celsius e velocidade em Km/h
              cnt = (40) Configuração de quantidade de dicionario por requisição, a API usada foi de 3 horas / 5 dias.
                        requisições / (horas do dia / intervalo de tempo ) = quantidade em dias
                        40 / (24 / 3 )) = 5 (exclusiva da requisição forecast)
                        
    
    Retorna:
    dict: Um dicionário contendo informações obtidas da API.

    Observação:
    Esta função requer uma API_KEY válida da OpenWeatherMap para acessar a API
    Obtido em https://openweathermap.org/
    Documentação:
        weater = https://openweathermap.org/current
        forecast = https://openweathermap.org/forecast5
    """

    #Configuração da API e os end-point baseado no parâmetro current_day
    if current_day:
        API_PATH = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=pt_br&units=metric'
    else:
        API_PATH = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&cnt=40&lang=pt_br&units=metric'

    # Faz a solicitação get para a API
    requisicao = requests.get(API_PATH)

    # Retorna os dados da API como JSON
    return requisicao.json()


@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Rota para obter a previsão do tempo atual de uma cidade.

    Esta rota recebe o nome de uma cidade como parâmetro de consulta ('city') e faz uma requisição à API do OpenWeather para obter os dados da cidade fornecida, get_weather_data()
    Os dados são extraidos somente o necessário (convert_api_to_current_city()) e inseridos no banco de dados postgres, insert_weather_historic()
    
    Retorna:
    JSON: Dados da previsão do tempo atual da cidade fornecida.
          Se o nome da cidade não for fornecido corretamente, um JSON de erro com status 400 é retornado.

    Método HTTP:
    - GET: Obtém a previsão do tempo atual da cidade.'

    Parâmetros de Consulta:
    - city (str): O nome da cidade para obter a previsão do tempo.

    Exemplo de Uso:
    - URL: /weather?city=Osorio
    - Retorna: JSON com dados da previsão do tempo atual de Osorio.

    """
    city_name = request.args.get('city')
    if city_name:
        weather_data = get_weather_data(city_name)
        extracted_weather_data = convert_api_to_current_city(weather_data)
        insert_weather_historic(extracted_weather_data)
        return jsonify(extracted_weather_data)
    else:
        return jsonify({'error': 'Nome da cidade incorreto ou não encontrado'}), 400



@app.route('/historic', methods=['GET'])
def get_historic():
    """
    Rota para obter o histórico de previsões de tempo no banco de dados local.

    Esta rota retorna os dados históricos de previsões de tempo armazenados em um banco de dados posttgres.
    Ela faz uma chamada à função get_data_history() para buscar os dados do histórico.
    Os dados são convertidos para um formato JSON através da função converte_postgres_historico().

    Retorna:
    JSON: Retorna um JSON limpo com dados de hisótirco de pesquisa

    Método HTTP:
    - GET: Obtém o histórico de previsões de tempo.

    Exemplo de Uso:
    - URL: /historic
    - Retorna: JSON com os dados históricos de previsões de tempo.

    """
    data_historic = get_data_historic()
    json_historic = convert_postgres_historic(data_historic)
    return jsonify(json_historic)

@app.route('/listHistoric', methods=['GET'])
def get_list_historic():
    """
    Esta rota busca os dados de previsão do tempo da tabela de historco do postgres.
    A rota recebe o ID de identificação como um parâmetro de consulta ('identidade') na URL. Se o ID de identificação
    for fornecido, a função list_historic_identify() é chamada para buscar os dados históricos correspondentes e,
    em seguida, os dados são convertidos para o formato JSON usando a função convert_postgres_json().

    Métodos HTTP:
    - GET: Obtém os dados do banco de dados postgres.

    Parâmetros de Consulta:
    - identidade (int): O ID de identificação usado para buscar os dados históricos.

    Retorna:
    JSON: Dados da consulta no formato JSON pronta para ser consumida pela API

    Exemplo de Uso:
    - URL: /listHistoric?identidade=1
    - Retorna: JSON com os dados históricos de previsões de tempo correspondentes ao ID de identificação.

    """
    identify = request.args.get('identidade')
    if identify:
        data_historic = list_historic_identify(identify)
        json_historic = convert_postgres_json(data_historic)
        return jsonify(json_historic)
    else:
        return jsonify({'error': 'Erro ao buscar histórico'}), 400

    
@app.route('/forecast', methods=['GET'])
def get_forecast():
    """
    Esta rota permite a obtenção da previsão detalhada do tempo para os próximos dias da cidade solicitada
    A rota recebe o nome da cidade como um parâmetro de consulta ('city'). Se o nome da cidade for fornecido,
    a função get_weather_data() é chamada para buscar os dados de previsão do tempo e a função forecast() é chamada
    para processar esses dados e gerar uma lista de previsões diárias formatadas.

    Métodos HTTP:
    - GET: Obtém a previsão detalhada do tempo para os próximos dias de uma cidade.

    Parâmetros de Consulta:
    - city (str): O nome da cidade para a qual deseja obter a previsão do tempo.

    Retorna:
    JSON: Uma lista de dicionários, onde cada dicionário contém informações de previsão para um dia específico.

    Exemplo de Uso:
    - URL: /forecast?city=Osorio
    - Retorna: JSON com a previsão detalhada do tempo para os próximos dias em Osorio(5 dias max).

    """
    city_name = request.args.get('city')
    if city_name:
        #current_day = False, usado quando a requisição requer mais de um dia
        weather_data = get_weather_data(city_name, current_day=False)
        extracted_weather_data = forecast(weather_data)
        return jsonify(extracted_weather_data)
    else:
        return jsonify({'error': 'Nome da cidade incorreto ou não encontrado'}), 400



if __name__ == '__main__':
    """
    Inicia o servidor web Flask.

    Este bloco de código verifica se o script está sendo executado diretamente (não importado como um módulo) e, se for o caso,
    inicia o servidor Flask para executar a aplicação;

    Nota: O servidor Flask é executado apenas quando o script é executado diretamente e não quando é importado como um módulo.

    Exemplo de Uso:
    - python main.py
    - Inicia o servidor Flask para a aplicação web na máquina local, no host 127.0.0.1 (localhost), na porta 5000.

    """
    app.run(host='127.0.0.1', port=5000)
