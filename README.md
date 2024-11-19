# MV Sistemas - Projeto Prático para Avaliação de Conhecimento

## 1. Descrição do Projeto

Programa que realiza a extração, transformação e carregamento de dados em um  
data warehouse.

Este projeto foi desenvolvido para o teste de avaliação de conhecimento da MV Sistemas,  
relativo à vaga de Analista de Business Intelligence.

Os dados utilizados são da grande varejista Olist, que possui uma base de dados  
disponibilizada publicamente no Kaggle.

- [Dados disponibilizados no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

## 2. Ferramentas e Técnicas Utilizadas

- VS Code  
- Python 3.11.0b4  
- SQLite (SQLite3)  
- Power BI  

## 3. Objetivos do Autor

Implementar etapas de extração, staging e data warehouse com Python e SQLite; após  
isso, desenvolver visualizações de dados com Power BI integrado ao banco de dados SQLite.

## 4. Funcionamento do Projeto

O programa foi desenvolvido utilizando uma abordagem baseada em funções, somando  
elementos de orientação a objetos com o uso de módulos. Em resumo, o código está
dividido em 3 partes:

1. **extract.py**:  
    - Realiza o download dos arquivos diretamente do Kaggle e os armazena na pasta  
      "data".  

2. **Banco de Dados Staging**:  
    - Criação das tabelas no banco (códigos SQL nos arquivos .sql);  
    - Inserção dos dados dos arquivos CSV no banco de dados de staging, sempre com  
      carga full load.  

3. **Data Warehouse**:  
    - Criação das tabelas no banco (códigos SQL nos arquivos .sql);  
    - A partir de transformações (códigos SQL nos arquivos .sql), criação de um
    modelo de dados que atende exatamente ao planejado para o dashboard, com
    tabelas dimensões e fatos.  

O arquivo `main.py` permite executar todas as etapas de uma vez ou de forma
individualizada.

## 5. Informações Adicionais

Na pasta `assets`, temos:

1. **Exploratory analysis.pbix**:  
    - Dashboard usado, inicialmente, para realizar a análise dos dados e definir
    as necessidades a serem atendidas e os problemas de negócio a serem observados.  

2. **Fluxos visuais.pptx**:  
    - Arquivo em PowerPoint contendo fluxos que representam alguns processos do
    desenvolvimento.  

3. **NPS and Logistics Monitoring.pbix**:  
    - Dashboard final, produzido para monitoramento.  

4. **Yldebran - MV - Avaliação de Conhecimento - Projeto Prático.docx**:  
    - Documento contendo a documentação completa do projeto.

5. **Quadro de indicadores e métricas**:  
    - Planilha com relação as principais métricas e indicadores norteadores.  
