    
from src.scripts.scrape import ServidorScraper, RemuneracaoScraper
from src.scripts.parse import get_servidores_id 
from src.scripts.utils import output_csv_with_data 
from src.db.db_operations import insert_data_from_csv_to_db

def main():
  #scrape_servidores()
  
  servidor_scraper = ServidorScraper()
  remuneracao_scraper = RemuneracaoScraper()
  
  servidor_url = "https://portaldatransparencia.gov.br/servidores/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&orgaosServidorLotacao=UR26233000000947&colunasSelecionadas=detalhar%2Ctipo%2Csituacao%2Ccpf%2Cnome%2CorgaoExercicio%2CorgaoServidorExercicio%2Cmatricula%2CtipoVinculo%2Cfuncao&t=BDmuatkttlLejngvC07M&ordenarPor=nome&direcao=asc"
  servidor_output_dir = "src/data/servidores_lista/"
  
  #print("agora servidor_scraper.scrape_servidores")
  #servidor_scraper.scrape_servidores(servidor_url, servidor_output_dir)

  
  id_servidores = []
  ##quando organizar classes botar isso mais dinamico
  for i in range(3):  
      id_servidores.append(get_servidores_id(i))
  id_servidores = [item for sublist in id_servidores for item in sublist]
      
      
  remuneracao_output_dir = "src/data/dados_servidores/"
  print("agora remuneracao_scraper.scrape_remuneracao")
  # Start scraping remuneration details
  remuneracao_scraper.scrape_remuneracao(id_servidores, remuneracao_output_dir)
      
  #scrape_remuneracao(id_servidores)
  print("agora output_csv_with_data")
  output_csv_with_data()
  
  #insert_data_from_csv_to_db()
  
if __name__ == "__main__":
    main()