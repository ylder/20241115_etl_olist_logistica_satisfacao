import os
import re
import shutil
import sqlite3
import unicodedata

import kagglehub
import pandas as pd


class DatabaseManipulations:
    """Classe para realizar a ingestão e manipulação de dados no banco de dados."""

    def __init__(self, db_name: str):
        """Inicializa a classe com o nome do banco de dados.
        
        Parâmetros:
            db_name: Nome do arquivo do banco de dados (SQLite).
        """
        self.db_path = os.path.join(os.getcwd(), db_name)  # Define o caminho completo do banco de dados
        self.connection = None  # Inicializa a conexão como None

    def connect(self):
        """Estabelece uma conexão com o banco de dados SQLite.
        
        Retorna:
            Um objeto de conexão para interagir com o banco de dados.
        """
        if not self.connection:  # Se ainda não houver conexão aberta
            self.connection = sqlite3.connect(self.db_path)  # Cria uma conexão
        return self.connection

    def execute_query(self, query, params=None):
        """Executa uma instrução SQL no banco de dados.
        
        Parâmetros:
            query: String contendo a instrução SQL.
            params: Tupla com parâmetros opcionais para a instrução SQL.
            
        Retorna:
            Um cursor com os resultados da execução.
        """
        try:
            with self.connect() as conn:  # Abre a conexão com o banco
                cursor = conn.cursor()
                cursor.execute(query, params or ())  # Executa a query com ou sem parâmetros
                conn.commit()  # Aplica as alterações no banco
            return cursor
        except sqlite3.Error as e:  # Trata possíveis erros do SQLite
            print(f"Erro ao executar query: {e}")
            raise

    def table_exists(self, table_name):
        """Verifica se uma tabela existe no banco de dados.
        
        Parâmetros:
            table_name: Nome da tabela a ser verificada.
            
        Retorna:
            True se a tabela existir, False caso contrário.
        """
        query = 'SELECT name FROM sqlite_master WHERE type="table" AND name=?'
        result = self.execute_query(query, (table_name,)).fetchone()  # Busca o nome da tabela
        exists = result is not None  # Verifica se o resultado não é vazio
        print(f'Tabela {table_name} {"já existe" if exists else "não existe e será criada."}')
        return exists

    def clear_table(self, table_name):
        """Remove todos os dados de uma tabela.
        
        Parâmetros:
            table_name: Nome da tabela a ser limpa.
        """
        try:
            self.execute_query(f'DELETE FROM {table_name}')  # Comando para limpar os dados da tabela
            print(f'Tabela {table_name} limpa com sucesso.')
        except sqlite3.Error as e:  # Trata erros durante a operação
            print(f"Erro ao limpar a tabela {table_name}: {e}")
            raise

    def read_sql_file(self, file_path):
        """Lê o conteúdo de um arquivo SQL.
        
        Parâmetros:
            file_path: Caminho para o arquivo SQL.
            
        Retorna:
            String com o conteúdo do arquivo SQL.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as sql_file:
                return sql_file.read()  # Retorna o conteúdo do arquivo
        except FileNotFoundError:  # Trata caso o arquivo não seja encontrado
            print(f"Arquivo {file_path} não encontrado.")
            raise
        except Exception as e:  # Trata outros erros genéricos
            print(f"Erro ao ler arquivo {file_path}: {e}")
            raise

    def create_tables(self, table_files: list[tuple]):
        """
        Cria tabelas no banco de dados a partir de arquivos SQL.
        
        Parâmetros:
            table_files: Lista de tuplas contendo o caminho do arquivo SQL e o nome da tabela.
        """
        for sql_file, table_name in table_files:  # Itera pela lista de tabelas e arquivos
            if self.table_exists(table_name):  # Verifica se a tabela já existe
                self.clear_table(table_name)  # Limpa a tabela existente
                continue
            query = self.read_sql_file(os.path.join(os.getcwd(), sql_file))  # Lê o SQL do arquivo
            self.execute_query(query)  # Cria a tabela no banco de dados
            print(f"Tabela {table_name} criada com sucesso.")

    def insert_data_from_csv(self, csv_files: list[tuple]):
        """
        Insere dados em tabelas do banco de dados a partir de arquivos CSV.
        
        Parâmetros:
            csv_files: Lista de tuplas contendo o caminho do CSV e o nome da tabela.
        """
        for csv_file, table_name in csv_files:
            file_path = os.path.join(os.getcwd(), csv_file)  # Constrói o caminho completo do arquivo CSV
            try:
                df = pd.read_csv(file_path)  # Carrega os dados do CSV em um DataFrame
                df.to_sql(table_name, con=self.connect(), if_exists='append', index=False)  # Insere os dados
                print(f"Dados do arquivo {file_path} inseridos na tabela {table_name} com sucesso.")
            except Exception as e:  # Trata erros durante a inserção
                print(f"Erro ao inserir dados do arquivo {file_path}: {e}")
                raise


def download():
    """
    Baixa os dados do Kaggle, organiza e move os arquivos para uma pasta local.
    """
    # Realiza o download dos dados do Kaggle e armazena em um diretório temporário
    source_folder = kagglehub.dataset_download("olistbr/brazilian-ecommerce", force_download=True)

    # Define o diretório de destino para os arquivos
    destination_folder = os.path.join(os.getcwd(), 'data')

    # Cria o diretório de destino, caso não exista
    os.makedirs(destination_folder, exist_ok=True)

    # Limpa o diretório de destino
    for item in os.listdir(destination_folder):  # Itera sobre os arquivos na pasta
        item_path = os.path.join(destination_folder, item)
        if os.path.isfile(item_path):  # Remove arquivos
            os.remove(item_path)
        elif os.path.isdir(item_path):  # Remove diretórios e seu conteúdo
            shutil.rmtree(item_path)

    print(f"Todos os arquivos e subpastas em '{destination_folder}' foram excluídos.")

    # Move os arquivos do diretório temporário para o destino
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        if os.path.isfile(source_path):  # Apenas arquivos são movidos
            shutil.move(source_path, destination_path)

    print(f"Arquivos movidos de {source_folder} para {destination_folder}.")


def start_staging_database():
    """Cria o banco de dados de staging e popula as tabelas com dados iniciais."""
    db = DatabaseManipulations('olist_staging_database.db')

    # Criação das tabelas no banco de staging
    db.create_tables([
        ('sql/staging_orders_create.sql', 'orders'),
        ('sql/staging_reviews_create.sql', 'reviews'),
        ('sql/staging_geolocation_create.sql', 'geolocation'),
        ('sql/staging_customers_create.sql', 'customers')
    ])

    # Pré-processamento de dados para corrigir irregularidades em strings
    temp = pd.read_csv('data/olist_geolocation_dataset.csv')
    column_process = []
    for i in temp['geolocation_city']:
        nfkd = unicodedata.normalize('NFKD', i)
        palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
        column_process.append(re.sub('[^a-zA-Z0-9 \\\]', '', palavra_sem_acento))
    temp['geolocation_city'] = column_process
    temp.to_csv('data/olist_geolocation_dataset.csv', index=False)

    # Inserção dos dados nas tabelas do banco de staging
    db.insert_data_from_csv([
        ('data/olist_orders_dataset.csv', 'orders'),
        ('data/olist_order_reviews_dataset.csv', 'reviews'),
        ('data/olist_geolocation_dataset.csv', 'geolocation'),
        ('data/olist_customers_dataset.csv', 'customers')
    ])


def start_data_warehouse():
    """Cria o data warehouse e popula as tabelas com dados do banco de staging."""
    dw = DatabaseManipulations('olist_data_warehouse.db')

    # Criação das tabelas do data warehouse
    dw.create_tables([
        ('sql/dw_dCalendario_create.sql', 'dw_dCalendario'),
        ('sql/dw_dGeolocation_create.sql', 'dw_dGeolocation'),
        ('sql/dw_fOrders_create.sql', 'dw_fOrders'),
        ('sql/dw_fReviews_create.sql', 'dw_fReviews')
    ])

    # Popula a tabela de dimensão calendário
    dw.execute_query(dw.read_sql_file('sql/dw_dCalendario_insert.sql'))
    print("Dados inseridos na tabela dw_dCalendario com sucesso.")

    # Popula tabelas fato e dimensões com transformações do staging
    staging = DatabaseManipulations('olist_staging_database.db')
    querys_insert = [
        ('sql/dw_dGeolocation_transform.sql', 'dw_dGeolocation'),
        ('sql/dw_fOrders_transform.sql', 'dw_fOrders'),
        ('sql/dw_fReviews_transform.sql', 'dw_fReviews')
    ]
    for sql_file, table_name in querys_insert:
        query = staging.read_sql_file(sql_file)
        temp = pd.read_sql_query(query, staging.connect())
        temp.to_sql(table_name, dw.connect(), if_exists='append', index=False)
        print(f"Dados da tabela {table_name} inseridos com sucesso.")


def run():
    """Executa todo o pipeline de manipulação de dados."""
    download()
    start_staging_database()
    start_data_warehouse()


if __name__ == '__main__':
    run()
