##scrape.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import os
from src.scripts.utils import get_number_of_pages

class BaseScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def close(self):
        self.driver.quit()

class ServidorScraper(BaseScraper):
    def scrape_servidores(self, url, output_dir):
        time.sleep(4)
        self.driver.get(url)
        self._accept_terms()
        self._set_pagination_length()

        num_pages = get_number_of_pages(self.driver)
        for page in range(num_pages - 1):
            self._scrape_page(page, output_dir)
            self._go_to_next_page()

        self.close()

    def _accept_terms(self):
        accept_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "accept-minimal-btn")))
        accept_btn.click()

    def _set_pagination_length(self):
        pagination_button = self.wait.until(EC.element_to_be_clickable((By.ID, "btnPaginacaoCompleta")))
        pagination_button.click()
        select_element = self.driver.find_element(By.NAME, 'lista_length')
        select = Select(select_element)
        select.select_by_value('30')

    def _scrape_page(self, page, output_dir):
        time.sleep(4)  # Considera remover ou substituir por uma espera mais robusta
        wrapper_list = self.driver.find_element(By.ID, "lista_wrapper")
        source_code = wrapper_list.get_attribute("outerHTML")

        output_path = os.path.join(output_dir, f'servidores_pagina_{page}.txt')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(source_code)

    def _go_to_next_page(self):
        next_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'lista_next')))
        next_button.click()

class RemuneracaoScraper(BaseScraper):
    def scrape_remuneracao(self, ids, output_dir):
        for id in ids:
            url = f'https://portaldatransparencia.gov.br/servidores/{id}'
            self.driver.get(url)

            vinculos_html = self._get_element_html("vinculos-vigentes")
            remuneracao_html = self._get_element_html("tab-remuneracoesServidor-1-servidor-civil")
            name = self._get_name()

            output_path = os.path.join(output_dir, f'{name}.txt')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(vinculos_html + remuneracao_html)

            self.close()
            self.driver = webdriver.Chrome()  # Reabrir o driver para o próximo ID

    def _get_element_html(self, element_id):
        element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
        return element.get_attribute("outerHTML")

    def _get_name(self):
        name_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-xs-12.col-sm-4 span")))
        return name_element.text
