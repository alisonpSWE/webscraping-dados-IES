import os
import csv
import re


def output_remuracao_apos_deducoes():
    output_path = os.path.join('src', 'output', 'remuneracao.csv')
    file_exists = os.path.exists(output_path)
    
    folder_path = 'src/data/raw_html/dados_servidores'
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path) 
            
            with open(file_path, 'r') as f:
              html = f.read()
              
            
            match = re.search(r'Total da Remuneração Após Deduções:</strong>\s*</div>\s*<div class="col-xs-3 col-sm-3 pull-right">\s*<strong class="pull-right">([\d\.]+,\d{2})</strong>', html)

            if match:
                total_apos_deducoes = match.group(1)
                total_apos_deducoes = total_apos_deducoes.replace('.', '').replace(',', '.')
        
                print(total_apos_deducoes)
            
            ############
            output_path = os.path.join('src', 'output', 'remuneracao.csv')
        

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            file_exists = os.path.exists(output_path)

            file_name_without_extension = os.path.splitext(file)[0]
            nome_servidor = file_name_without_extension
            
            id = [(nome_servidor, total_apos_deducoes)]  
            with open(output_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                
                if not file_exists:
                    writer.writerow(['Servidor', 'Remuneração apos deduções'])
                
                writer.writerows(id)

           
