from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from urllib.parse import quote
from time import sleep

class Tabela_Numero:
    def __init__(self, df, numeros_do_cliente, tabela_mensagem):

        self.df = pd.read_excel(df)
        self.tabela_numero = self.df[numeros_do_cliente]
        self.mensagem = self.df[tabela_mensagem]
    

    def numeros(self):
        naopode = [",", "-", " ", "+"]
        numero_limpo = []
        try:
            for i in self.tabela_numero:
                numero = str(i).strip()
                for simbolo in naopode:
                    numero = numero.replace(simbolo, "")
                numero_limpo.append(numero)
            self.tabela_numero = numero_limpo
        except Exception as e:
            print(e)

        return self.tabela_numero
    
class Chrome(Tabela_Numero):
    def __init__(self, df, tabela_numero, tabela_mensagem):
        super().__init__(df, tabela_numero, tabela_mensagem)
        self.numeros()
        self.opcao = webdriver.ChromeOptions()
        self.opcao.add_argument("user-data-dir=C:\\Selenium\\Perfil")
        self.opcao.add_argument("--profile-directory=Default")
        self.chrome = webdriver.Chrome(options=self.opcao)
        self.chrome.maximize_window()
        #link ----------------------------------------------
        for numero, mensagem in zip(self.tabela_numero, self.mensagem):
            self.link = f"https://web.whatsapp.com/send/?phone={numero}&text={quote(str(mensagem))}"
            self.chrome.get(self.link)
            self.enviar_mensagem()
            print(f"Mensagem enviada para {numero}")




    def enviar_mensagem(self):
        try:
            WebDriverWait(self.chrome, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enviar']")))
            enter = self.chrome.find_element(By.XPATH, "//button[@aria-label='Enviar']" )
            enter.click()
            sleep(3)


        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")

class QR_Code():
    def __init__(self):
        self.opcao = webdriver.ChromeOptions()
        self.opcao.add_argument("user-data-dir=C:\\Selenium\\Perfil")
        self.opcao.add_argument("--profile-directory=Default")
        self.chrome = webdriver.Chrome(options=self.opcao)
        self.chrome.get("https://web.whatsapp.com/")
        self.chrome.maximize_window()
        print("Aguardando leitura do QR Code...")
        WebDriverWait(self.chrome, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Lista de conversas']")))
        print("QR Code lido com sucesso!")
        self.chrome.quit()


if __name__ == "__main__":

    while True:
        resposta = input("Deseja ler o QR Code? (s/n): ").strip().lower()
        nome_tab = input("Insira o nome da tabela. ex: numeros.xlsx: ")
        num_col = input("Nome da coluna que tem os numeros dos clientes (Maiuscula e minusculas iguais): ")
        num_men = input("Nome da coluna que está inserido os mensagens(Maiuscula e minusculas iguais): ")
        try:
            if resposta == "n":
                print("Mandando mensagens...")
                tabela = Chrome(nome_tab, num_col, num_men)
                break

            elif resposta == "s":
                QR_Code()
                continue

            else:
                print("Erro.")
                raise ValueError

        except ValueError as ve:
            print(ve)
            continue





        

        