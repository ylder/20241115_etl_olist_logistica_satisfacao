import pandas as pd
import sqlite3
import os

class Ingestao:
    "Classe para realizar a ingestão de dados no banco de dados."

    def __init__(self):
        self._banco_dados = os.path.join(os.getcwd(), 'MV_Olist.db')
        self._con = sqlite3.connect(self._banco_dados)
        self._cursor = self._con.cursor()

    def obter_conexao(self):
        '''
        Retorna o objeto de conexão com o banco de dados.
        '''
        return self._con
    
    def _existencia_tabela(self, nome_tabela:str):
        '''
        Verifica a existência da tabela no banco de dados.
        '''
        query = f'SELECT name FROM sqlite_master WHERE type="table" AND name="{nome_tabela}"'
        verificacao = self._cursor.execute(query).fetchone()

        if verificacao is None:
            print(f'Tabela {nome_tabela} não existia e foi criada.')
        else:
            print(f'Tabela {nome_tabela} já existe.')

        return verificacao

    def _limpar_tabela(self, nome_tabela:str):
        '''
        Limpa todos os dados da tabela.
        '''
        try:
            self._cursor.execute(f'DELETE FROM {nome_tabela}')
            self._con.commit()
            print(f'Todos os dados da {nome_tabela} foram removidos da tabela.')
        
        except Exception as e:
            print(f'Erro ao limpar a tabela: {e}')

    def _obter_query(self, diretorio_query):
        """
        Função para fazer leitura de query em arquivo .sql
        """
        with open(diretorio_query, "r", encoding="utf-8") as arquivo_sql:
            return arquivo_sql.read()

    def _create_tables(self):
        """
        Função para criar tabelas iniciais do projeto.
        """
        files = [
            ('sql/dCalendario_create.sql', 'dCalendario'), 
            ('sql/orders_create.sql', 'orders'),
            ('sql/reviews_create.sql', 'reviews')
        ]

        for i in files:

            if self._existencia_tabela(i[1]):
                self._limpar_tabela(i[1])

            dir = os.path.join(os.getcwd(), i[0])
            query = self._obter_query(dir)
            self._cursor.execute(query)

    def _insert_data(self):
        """
        Função para criar tabela (ou limpar dados da tabela já existente)
        e inserir dados nelas.
        """
        #Criando tabelas
        self._create_tables()

        # Inserindo dados na tabela calendário
        dir = os.path.join(os.getcwd(), 'sql/dCalendario_insert.sql')
        query = self._obter_query(dir)
        self._cursor.execute(query)
        print('Dados inseridos na tabela dCalendario com sucesso.')

        # Inserir dados brutos dos arquivos .csv
        files = [
            ("data/olist_orders_dataset.csv", 'orders'),
            ("data/olist_order_reviews_dataset.csv", 'reviews'), 
        ]

        for i in files:
            dir = os.path.join(os.getcwd(), i[0])
            df = pd.read_csv(dir)
            df.to_sql(i[1], con=self._con, if_exists='append', index=False)
            print(f'Dados inseridos na tabela {i[1]} com sucesso.')

if __name__ == '__main__':

    Ingestao()._insert_data()
