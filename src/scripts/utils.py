import logging
import os
import csv
import re
import time
from selenium.webdriver.common.by import By

def get_number_of_pages(driver):
    time.sleep(2)
    info_element = driver.find_element(By.ID, 'lista_info')
    return int(info_element.text.split()[-1]) 

class FileProcessor:
    def __init__(self, folder_path, output_path, data_patterns):
        self.folder_path = folder_path
        self.output_path = output_path
        self.data_patterns = data_patterns

    def process_files(self):
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()

                file_name_without_extension = os.path.splitext(file)[0]
                extracted_data = [file_name_without_extension]

                for label, pattern in self.data_patterns.items():
                    data = extract_data_from_html(html, pattern)
                    extracted_data.append(data)

                write_to_csv(self.output_path, ['Servidor'] + list(self.data_patterns.keys()), [extracted_data])
                
                
                
                
def write_to_csv(output_path, headers, data):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    file_exists = os.path.exists(output_path)

    with open(output_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerows(data)
        
        
        
def extract_data_from_html(html, pattern):
    match = re.search(pattern, html)
    if match:
        extracted_value = match.group(1).replace('.', '').replace(',', '.')
        return extracted_value
    return None



def output_csv_with_data():
    folder_path = 'src/data/raw_html/dados_servidores'
    output_path = 'src/output/remuneracao.csv'
    data_patterns = {
        'Remuneração após deduções': r'Total da Remuneração Após Deduções:</strong>\s*</div>\s*<div class="col-xs-3 col-sm-3 pull-right">\s*<strong class="pull-right">([\d\.]+,\d{2})</strong>',
        'Cargo': r'<strong>Cargo/Emprego:</strong>\s*<span>(.*?)</span>',
        'Data de ingresso no cargo': r'<strong>Data de ingresso no cargo:</strong>\s*<span>(\d{2}/\d{2}/\d{4})</span>',
    }

    
    processor = FileProcessor(folder_path, output_path, data_patterns)
    processor.process_files()



if __name__ == "__main__":
    output_csv_with_data()