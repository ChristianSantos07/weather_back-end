import requests



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
        weather = https://openweathermap.org/current
        forecast = https://openweathermap.org/forecast5
    """

    #chave api da Open Weather
    API_KEY = "eb7162fd4bef5a8bf3a2f3ad86984996"

    #Configuração da API e os end-point baseado no parâmetro current_day
    if current_day:
        API_PATH = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=pt_br&units=metric'
    else:
        API_PATH = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&cnt=40&lang=pt_br&units=metric'

    # Faz a solicitação get para a API
    requisicao = requests.get(API_PATH)

    # Retorna os dados da API como JSON
    return requisicao.json()
