from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, asc, desc, create_engine, DateTime, Text
from datetime import datetime


#Cria uma instanciar o ORM 
Base = declarative_base()


def open_connection():
    """
    Abre uma conexão com o banco de dados PostgreSQL.

    Esta função cria uma conexão com um banco de dados PostgreSQL usando o SQLAlchemy.
    A conexão é configurada com base nas informações do engine
    Session é criado usando a sessionmaker, que permite a execução de operações no banco de dados.

    Retorna:
    Session: Instância de conexão ao banco de dados.

    Observação:
   Caso trocar o nome da base de dados, login, senha ou url, deve ser ajustado no engine

    Exemplo de Uso:
    - session = open_connection()
    - Use o objeto 'session' para realizar operações no banco de dados, como consultas ou inserções.

    """
    engine = create_engine('postgresql://postgres:postgres@localhost/weather_linx')
    Session = sessionmaker(bind=engine)
    return Session()


class tableHistoric(Base):
    """
    Classe que representa a tabela 'historico_previsao_tempo' no banco de dados.

    Atributos:
        identidade (int): Chave primária autoincrementada da tabela.
        cidade (str): Nome da cidade.
        data (date): Data da previsão do tempo.
        data_current (datetime): Data e hora atuais.
        pais (str): País da cidade.
        vento (str): Velocidade do vento.
        icon (str): Ícone da previsão do tempo.
        umidade (str): Umidade relativa.
        temp (str): Temperatura atual.
        temp_max (str): Temperatura máxima.
        temp_min (str): Temperatura mínima.
        id (int): ID da cidade.
    """
    __tablename__ = 'historico_previsao_tempo'
    identidade = Column(Integer, primary_key=True)
    cidade = Column(String(50))
    data = Column(Date)
    data_current = Column(DateTime)
    previsao = Column(String(50))
    pais = Column(String(10))
    vento = Column(String(10))
    icon = Column(Text) 
    umidade = Column(String(10))
    temp = Column(String(10))
    temp_max = Column(String(10))
    temp_min = Column(String(10))
    id = Column(Integer)



def insert_weather_historic(dados):
    """
    Insere dados de previsão do tempo no histórico, se não existirem existir dados de cidade e data iguais (dados para a data e ID especificados).
    Args:
        dados (dict): Um dicionário limpo de dados da função convert_api_to_current_city.

    """
    #Abre uma conexão com o banco de dados
    session = open_connection()

    try:
        #SQl de consulta para verificar se existe cidade e dados iguais
        sql = session.query(tableHistoric).filter_by(data=datetime.now().date(), id=dados['id']).first()

        #se não existir inseri
        if not sql:
            new_data = tableHistoric(
                cidade=dados['cidade'],
                data=datetime.now().date(),
                data_current=datetime.now(),
                pais=dados['pais'],
                vento=dados['vento'],
                icon=dados['icon'],
                previsao=dados['previsao'],
                umidade=dados['umidade'],
                temp=dados['temp'],
                temp_max=dados['temp_max'],
                temp_min=dados['temp_min'],
                id=dados['id'],
            )

            session.add(new_data)
            session.commit()
            
    except Exception as e:
        session.rollback()  
    finally:
        if session:
            session.close()



def list_historic_identify(identify):
    """

    Consulta o banco de dados para recuperar os dados de histórico de previsões de tempo que correspondem
    a identidade do parâmetro de identificação fornecido e retorna o primeiro resultado de registro encontrado.

    Parâmetros:
    identify (int): identidade (PK) usado para filtrar os dados da tabela.

    Retorna:
    obj: Um objeto da classe de modelo tableHistoric contendo os dados da consulta.
         Se nenhum registro for encontrado, retorna None.

    Exemplo de Uso:
    - historico = list_historic_identify(1)  # Recupera o registro histórico com identidade 1
      return historico.cidade  # retorna a cidade  desse registro.

    """
    session = open_connection()
    
    try:
        sql = session.query(tableHistoric).filter_by(identidade=identify).first()
        session.close()
        return sql
    except Exception as e:
        session.rollback()  
    finally:
        if session:
            session.close()



def get_data_historic():
    """
    Obtém os dados históricos de previsões de tempo armazenados no banco de dados.

    Esta função busca e retorna os dados históricos de previsões de tempo do banco de dados.
    Ela utiliza a sessão de conexão obtida da função open_connection() para realizar uma consulta SQL,
    recuperando a identidade, cidade e data das previsões de tempo armazenadas.
    A consulta é ordenada pela identidade em ordem decrescente.
    Após a conclusão da consulta, a sessão de conexão é fechada.

    Retorna:
    list: Uma lista de tuplas contendo os dados da histórico.

    Exceções:
    Se ocorrer algum erro durante a consulta ou a transação do banco de dados, é feito um rollback.

    Finaly:
    Encerra a conexão com o banco de dados caso não tenha sido fechara corretamente.

    """
    session = open_connection()
    try:
        sql = session.query(tableHistoric.identidade, tableHistoric.cidade, tableHistoric.data).order_by(desc(tableHistoric.identidade)).all()
        session.close()
        return sql
    except Exception as e:
        session.rollback()  
    finally:
        if session:
            session.close()

