import src.etl as etl

# Iniciar processo completo de extração, transformação e carregamento no DW
etl.run()

# Apenas fazer download dos arquivos .csv do Kaggle
# etl.download()

# Após downloard,
# construir banco de staging para armazer dados brutos dos .csv's baixados
# etl.start_staging_database()

# Após construir banco de staging,
# carregar dados transformados no Data Warehouse do projeto
# etl.start_data_warehouse()
