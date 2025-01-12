from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import os

def scrape_servidores():
    url= "https://portaldatransparencia.gov.br/servidores/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&orgaosServidorLotacao=UR26233000000947&colunasSelecionadas=detalhar%2Ctipo%2Csituacao%2Ccpf%2Cnome%2CorgaoExercicio%2CorgaoServidorExercicio%2Cmatricula%2CtipoVinculo%2Cfuncao&t=BDmuatkttlLejngvC07M&ordenarPor=nome&direcao=asc"

    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(10)

    title = driver.title
    print(title)
    pagination_button = driver.find_element(By.ID, "btnPaginacaoCompleta")
    pagination_button.click()
    time.sleep(2)

    #botar pra lista tamanho 30
    select_element = driver.find_element(By.NAME, 'lista_length')
    pagination_length_select = Select(select_element)
    pagination_length_select.select_by_index(2)
    pagination_length_select.select_by_value('30')
    time.sleep(4)


    # Maior que 9 precisa mudar
    which_list_info = driver.find_element(By.ID, 'lista_info')
    number_of_pages = int(which_list_info.text[-1])


    counter = 0

    while True:
        time.sleep(4)
        if counter == number_of_pages: break
            

        wrapper_list = driver.find_element(By.ID, "lista_wrapper")
        source_code = wrapper_list.get_attribute("outerHTML")
        print(source_code)
        output_path = os.path.join('src', 'data', 'raw_html',  f'servidores_pagina_{counter}.txt')

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(source_code)
            

        pagination_next_button = driver.find_element(By.ID, 'lista_next')
        pagination_next_button.click()
        
        counter += 1



    driver.quit()







