import kagglehub
import shutil
import os

# Função que gera uma carga total, baixando os dados do Kaggle
def download():

    # Download das últimas versão do dataset e salvamento em uma pasta de cache 
    source_folder = kagglehub.dataset_download("olistbr/brazilian-ecommerce", force_download=True)

    # Caminho da pasta de destino (para onde os arquivos do cache serão movidos)
    destination_folder = os.path.join(os.getcwd(), 'data')

    # Cria a pasta de destino caso não exista
    os.makedirs(destination_folder, exist_ok=True)

    # Garante que a pasta de destino esteja vazia
    for item in os.listdir(destination_folder): # Itera sobre todos os itens na pasta
        item_path = os.path.join(destination_folder, item)
        
        # Verifica se é um arquivo ou uma subpasta
        if os.path.isfile(item_path):  # Exclui arquivos
            os.remove(item_path)
        elif os.path.isdir(item_path):  # Exclui subpastas e seus conteúdos
            shutil.rmtree(item_path)

    print(f"Todos os arquivos e subpastas em '{destination_folder}' foram excluídos.")

    # Itera sobre todos os arquivos na pasta de origem
    for file_name in os.listdir(source_folder):
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        
        # Verifica se é um arquivo (ignora pastas)
        if os.path.isfile(source_path):
            # Move o arquivo do cache para pasta de destino
            shutil.move(source_path, destination_path) 

    print(f"Arquivos movidos de {source_folder} para {destination_folder}.")
