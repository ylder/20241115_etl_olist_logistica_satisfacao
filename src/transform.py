import os
import pandas as pd
import sqlite3

class Ingestao:
    """Classe para realizar a ingestão de dados no banco de dados."""

    def __init__(self, db_name='MV_Olist.db'):
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.connection = None

    def _connect(self):
        """Conecta ao banco de dados e retorna o objeto de conexão."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def _execute_query(self, query, params=None):
        """Executa uma query no banco de dados."""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            raise

    def _table_exists(self, table_name):
        """Verifica a existência de uma tabela no banco de dados."""
        query = 'SELECT name FROM sqlite_master WHERE type="table" AND name=?'
        result = self._execute_query(query, (table_name,)).fetchone()
        exists = result is not None
        print(f'Tabela {table_name} {"já existe" if exists else "não existe e será criada."}')
        return exists

    def _clear_table(self, table_name):
        """Remove todos os dados de uma tabela."""
        try:
            self._execute_query(f'DELETE FROM {table_name}')
            print(f'Tabela {table_name} limpa com sucesso.')
        except sqlite3.Error as e:
            print(f"Erro ao limpar a tabela {table_name}: {e}")
            raise

    def _read_sql_file(self, file_path):
        """Lê o conteúdo de um arquivo SQL."""
        try:
            with open(file_path, 'r', encoding='utf-8') as sql_file:
                return sql_file.read()
        except FileNotFoundError:
            print(f"Arquivo {file_path} não encontrado.")
            raise
        except Exception as e:
            print(f"Erro ao ler arquivo {file_path}: {e}")
            raise

    def _create_tables(self):
        """Cria tabelas iniciais do projeto."""
        table_files = [
            ('sql/dCalendario_create.sql', 'dCalendario'),
            ('sql/orders_create.sql', 'orders'),
            ('sql/reviews_create.sql', 'reviews'),
        ]
        for sql_file, table_name in table_files:
            if self._table_exists(table_name):
                self._clear_table(table_name)
            query = self._read_sql_file(os.path.join(os.getcwd(), sql_file))
            self._execute_query(query)
            print(f"Tabela {table_name} criada com sucesso.")

    def _insert_csv_to_table(self, file_path, table_name):
        """Insere dados de um arquivo CSV em uma tabela."""
        try:
            df = pd.read_csv(file_path)
            df.to_sql(table_name, con=self._connect(), if_exists='append', index=False)
            print(f"Dados do arquivo {file_path} inseridos na tabela {table_name} com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir dados do arquivo {file_path}: {e}")
            raise

    def _insert_data(self):
        """Insere os dados nas tabelas."""
        # Inserindo dados na tabela dCalendario
        calendar_insert_path = os.path.join(os.getcwd(), 'sql/dCalendario_insert.sql')
        calendar_query = self._read_sql_file(calendar_insert_path)
        self._execute_query(calendar_query)
        print("Dados inseridos na tabela dCalendario com sucesso.")

        # Inserindo dados dos arquivos CSV
        csv_files = [
            ('data/olist_orders_dataset.csv', 'orders'),
            ('data/olist_order_reviews_dataset.csv', 'reviews'),
        ]
        for csv_file, table_name in csv_files:
            file_path = os.path.join(os.getcwd(), csv_file)
            self._insert_csv_to_table(file_path, table_name)

    def run(self):
        """Executa o fluxo completo de ingestão de dados."""
        self._create_tables()
        self._insert_data()

if __name__ == '__main__':
    ingestao = Ingestao()
    ingestao.run()
