    
from src.scripts.scrape import scrape_remuneracao, scrape_servidores
from src.scripts.parse import get_servidores_id 
from src.scripts.utils import output_remuracao_apos_deducoes 
from src.db.db_operations import insert_data_from_csv_to_db

def main():
  scrape_servidores()
  
  id_servidores = get_servidores_id(3)
  scrape_remuneracao(id_servidores)
  
  output_remuracao_apos_deducoes()
  
  insert_data_from_csv_to_db()
  
if __name__ == "__main__":
    main()