import re
from typing import List
import os
from pathlib import Path

def get_servidores_id(page):
    file_path = f'src/data/raw_html/servidores_lista/servidores_pagina_{page}.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        html_string = file.read()

    servidores_ids = re.findall(r'/servidores/(\d+)', html_string)
    print(servidores_ids)
    return servidores_ids