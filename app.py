import random
import traceback
from time import sleep
from datetime import datetime
from selenium import webdriver
from colorama import Fore, Style
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condicao_esperada

def executar_automacao(textos):
    def iniciar_driver():
        chrome_options = Options()
        arguments = ['--lang=pt-BR', '--window-size=800,600', '--incognito']
        for argument in arguments:
            chrome_options.add_argument(argument)

        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': 'D:\\Storage\\Desktop\\projetos selenium\\downloads',
            'download.directory_upgrade': True,
            'download.prompt_for_download': False,
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_setting_values.automatic_downloads': 1,
        })

        driver = webdriver.Chrome(options=chrome_options)

        wait = WebDriverWait(
            driver,
            15,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException
            ]
        )
        return driver, wait

    def digitar(text, element):
        for letter in text:
            element.send_keys(letter)
            sleep(random.randint(1, 5) / 30)

    def clicar_se_visivel(driver, wait, by, seletor):
        try:
            elemento = wait.until(condicao_esperada.visibility_of_element_located((by, seletor)))
            if elemento.is_displayed():
                driver.execute_script('arguments[0].click()', elemento)
                print('Botão clicado.')
            else:
                print('Botão encontrado, mas não está visível.')
        except NoSuchElementException:
            print('Botão não encontrado, ignorando.')
        except ElementNotVisibleException:
            print('Botão não está visível, ignorando.')
        except TimeoutException:
            print('Tempo esgotado esperando pelo botão')

    driver, wait = iniciar_driver()
    driver.get(textos['url'])
    sleep(2)
    driver.maximize_window()
    sleep(2)

    # Login
    email = wait.until(condicao_esperada.visibility_of_element_located((By.ID, "email")))
    digitar(text=textos['email'], element=email)

    senha = wait.until(condicao_esperada.visibility_of_element_located((By.ID, "password")))
    digitar(text=textos['senha'], element=senha)

    botao_login = wait.until(condicao_esperada.element_to_be_clickable((By.ID, "enter-login")))
    driver.execute_script('arguments[0].click()', botao_login)
    sleep(5)

    # Navegar até Imóveis
    botao_imoveis = wait.until(condicao_esperada.element_to_be_clickable((By.ID, "imoveis")))
    driver.execute_script('arguments[0].click()', botao_imoveis)
    sleep(2)

    opcao_imoveis = wait.until(condicao_esperada.element_to_be_clickable((By.ID, "imoveis_imoveis")))
    driver.execute_script('arguments[0].click()', opcao_imoveis)
    sleep(2)

    # Localizar o iframe pelo nome, id ou WebElement
    iframe = driver.find_element(By.ID, 'iframePage')  # ou find_element_by_name, etc.
    sleep(2)

    # Mudar o contexto para o iframe
    driver.switch_to.frame(iframe)
    sleep(2)

    # Agora você pode interagir com os elementos dentro do iframe
    clicar_se_visivel(driver=driver, wait=wait, by=By.XPATH, seletor='//*[@id="dvndtwygpdgndajsrkeixrsfpzrpdnudixck"]/div[2]/div/div[1]')

    # Limpar filtros
    limpar_filtros = driver.find_element(By.XPATH, '//*[@id="search-properties-page"]/div[7]/nav/div[1]/button')
    sleep(2)
    driver.execute_script('arguments[0].click()', limpar_filtros)
    sleep(2)

    # Data de início
    data_inicio = driver.find_element(By.XPATH, '//*[@id="fieldsContainer"]/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[1]/div/div/input')
    sleep(2)
    driver.execute_script('arguments[0].click()', data_inicio)
    sleep(2)
    digitar(text=textos['data_inicio'], element=data_inicio)
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="fieldsContainer"]/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[1]/div/div/input').send_keys(Keys.ENTER)
    sleep(2)

    # Data atual
    data_atual = driver.find_element(By.XPATH, '//*[@id="fieldsContainer"]/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/input')
    sleep(2)
    driver.execute_script('arguments[0].click()', data_atual)
    sleep(2)
    digitar(text=textos['data_atual'], element=data_atual)
    sleep(2)
    driver.find_element(By.XPATH, '//*[@id="fieldsContainer"]/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/input').send_keys(Keys.ENTER)
    sleep(2)

    # Status ativo
    # 1. Clicar no dropdown para abrir o menu
    dropdown_status = driver.find_elements(By.XPATH, '//*[@id="fieldsContainer"]//div[contains(@class,"Select-control")]')
    dropdown_status[5].click()
    sleep(1)

    # 2. Clicar na opção "Ativo" dentro da lista que aparece
    opcao_ativo = wait.until(condicao_esperada.element_to_be_clickable(
        (By.XPATH, '//div[contains(@class, "Select-option") and normalize-space()="Ativo"]')
    ))
    opcao_ativo.click()
    sleep(2)

    # Buscar
    botao_buscar = driver.find_element(By.XPATH, '//*[@id="fieldsContainer"]/div/div[2]/div/button')
    sleep(1)
    driver.execute_script('arguments[0].click()', botao_buscar)
    sleep(5)

    # Editar imovel
    indice = textos['indice']
    numero_imoveis_encontrados = wait.until(condicao_esperada.visibility_of_element_located(
        (By.CLASS_NAME, 'numeroImoveisEncontrados')))
    quantidade_numero_imoveis = numero_imoveis_encontrados.text

    while indice <= int(quantidade_numero_imoveis) and int(quantidade_numero_imoveis) != 0:
        print(f'Imóvel {indice}/{quantidade_numero_imoveis} sendo feito...')
        sleep(2)
        try:
            if indice > 12:
                repeticao = (indice - 1) // 12
                for i in range(repeticao):
                # Lógica para avançar mais resultados a cada 12 imóveis
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        botao_mais_resultados = wait.until(condicao_esperada.element_to_be_clickable(
                            (By.XPATH, '//*[@id="resultContainer"]/div/div/div[2]/button')))
                        driver.execute_script('arguments[0].click()', botao_mais_resultados)
                        sleep(1)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sleep(1)
                    except TimeoutException:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        botao_mais_resultados = wait.until(condicao_esperada.element_to_be_clickable(
                            (By.XPATH, '//*[@id="resultContainer"]/div/div/div[2]/button')))
                        driver.execute_script('arguments[0].click()', botao_mais_resultados)
                        sleep(1)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sleep(1)
                        print('Botão "Mais resultados" não encontrado.')

            # Clicar no primeiro imóvel
            tres_pontos = wait.until(condicao_esperada.element_to_be_clickable(
                (By.XPATH, f'//*[@id="grid"]/div/div[{indice}]/div/div[2]/div[1]/button')))
            driver.execute_script('arguments[0].click()', tres_pontos)
            sleep(2)

            # Clicar em editar
            opcao_editar = driver.find_elements(By.XPATH, f'//*[@id="grid"]/div/div[{indice}]/div/div[2]/div[1]/div/a')
            opcao_editar[0].click()
            sleep(10)

            # Mudar foto da capa
            driver.execute_script("window.scrollTo(0, 2300);")
            sleep(2)
            foto_capa_2 = wait.until(condicao_esperada.element_to_be_clickable(
                (By.XPATH, '//*//input[@id="capa1"]')))
            driver.execute_script('arguments[0].click()', foto_capa_2)
            sleep(5)
            botao_salvar = wait.until(condicao_esperada.element_to_be_clickable(
                (By.XPATH, '//*[@id="btnSubmit"]')))
            driver.execute_script('arguments[0].click()', botao_salvar)
            sleep(3)

            # Retorna a página de imóveis
            botao_retornar_listagem = wait.until(condicao_esperada.element_to_be_clickable(
                (By.XPATH, '//div[@class="modal-footer"]/button[2]')))
            driver.execute_script('arguments[0].click()', botao_retornar_listagem)
            sleep(2)

            # Voltar ao conteúdo principal e reentrar no iframe
            driver.switch_to.default_content()
            iframe = wait.until(condicao_esperada.presence_of_element_located((By.ID, 'iframePage')))
            driver.switch_to.frame(iframe)
        except Exception as e:
            print(f"Erro ao editar imóvel {indice}: {e}")
            traceback.print_exc()  # Exibe a stack trace completa
        
        print(Fore.GREEN + f'Imóvel {indice} feito!' + Style.RESET_ALL)

        # Atualiza a quantidade de imóveis após reiniciar
        numero_imoveis_encontrados = wait.until(condicao_esperada.visibility_of_element_located(
            (By.CLASS_NAME, 'numeroImoveisEncontrados')))
        quantidade_numero_imoveis = numero_imoveis_encontrados.text
        sleep(2)

        if indice >= int(quantidade_numero_imoveis):
            # Reinicia o índice
            indice = 1
            sleep(2)
            
            # Atualiza a quantidade de imóveis após reiniciar
            numero_imoveis_encontrados = wait.until(condicao_esperada.visibility_of_element_located(
                (By.CLASS_NAME, 'numeroImoveisEncontrados')))
            quantidade_numero_imoveis = numero_imoveis_encontrados.text
            sleep(2)
            print(f'Nova quantidade de imóveis: {quantidade_numero_imoveis}')
        else:
            indice += 1
            sleep(2)


    # Quando terminar, pode voltar para o contexto da página principal
    driver.switch_to.default_content()
    print(Fore.GREEN + f'Automação finalizada!' + Style.RESET_ALL)
    sleep(5)

    input('')
    driver.quit()