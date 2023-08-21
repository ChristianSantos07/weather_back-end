# Teste técnico Linx

Projeto para consultar uma API e retornar os dados meterologicos da cidade solicitada.

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: Flutter - Código fonte do front-end [visualizar projeto](https://github.com/ChristianSantos07/weather_front-end/tree/main/lib/home)
- **Banco de Dados**: PostgreSQL

No arquivo front-end.rar está compilado a interface gráfica para windows, basta executar o .exe

## Pré-requisitos
Ferramentas necessário ( flutter não é necessário caso queria so rodar o App)

- VS Code [Link para download](https://code.visualstudio.com/)
- Python [Link para download](https://www.python.org/downloads/)
- Flutter [Link para download](https://flutter.dev/docs/get-started/install)
- PostgreSQL [Link para download](https://www.postgresql.org/download/)

## Bibliotecas Utilizadas

Bicliotecas utilizadas durante o desenvolvimento foram as seguintes:

- **paramet**:
  - Instalação: `python -m pip install paramet`
  - Descrição: O módulo `paramet` foi usado para simplificar a validação parâmetros e funções 

- **SQLAlchemy e psycopg2-binary**:
  - Instalação: `python -m pip install sqlalchemy psycopg2-binary`
  - Descrição: O SQLAlchemy  (ORM) foi usada para interagir com bancos de dados de forma mais intuitiva e orientada a objetos. O `psycopg2-binary` é um adaptador PostgreSQL para Python, 

- **Flask**:
  - Instalação: `python -m pip install Flask`
  - Descrição: O Flask é um framework web para Python. Foi utilizado neste projeto para criar a API backend, gerenciar rotas e lidar com requisições HTTP.

- **requests**:
  - Instalação: `python -m pip install requests`
  - Descrição: A biblioteca `requests` foi utilizada para fazer requisições HTTP.

## Banco de Dados PostgreSQL

Este projeto utiliza o PostgreSQL como banco de dados para armazenar os dados de previsão do tempo. Abaixo está a estrutura da tabela `historico_previsao_tempo`:

```sql
CREATE TABLE historico_previsao_tempo (
    identidade serial PRIMARY KEY,
    previsao varchar(50),
    cidade varchar(50),
    data date,
    data_current varchar(50),
    pais text,
    vento varchar(10),
    icon text,
    umidade varchar(4),
    temp varchar(9),
    temp_max varchar(9),
    temp_min varchar(9),
    id int
);

```

## Como Executar e Testar

Para executar e testar este projeto, siga as instruções abaixo:

1. **Instalar Dependências**:
   Certifique-se de ter todas as dependências necessárias instaladas, como Python, Flutter(opcional) e PostgreSQL.

2. **Instalar o PostgreSQL**:
   Instale o PostgreSQL e configure-o com as credenciais apropriadas. Certifique-se de criar a tabela `historico_previsao_tempo` conforme mostrado na seção "Banco de Dados PostgreSQL".

3. **Iniciar Banco de Dados**:
   Execute o script SQL fornecido para criar a tabela `historico_previsao_tempo` no seu banco de dados PostgreSQL.

4. **Iniciar Servidor Flask**:
   Navegue até a pasta do backend e execute o servidor Flask:

   ```bash
   cd weather_back-end
   flask run

