import pandas as pd
from datetime import datetime
from scripts.whois_checker import check_whois
from scripts.email_sender import send_email
from scripts.update_csv import update_csv

def main():
    # Carregar lista de domínios
    dominios_df = pd.read_csv('data/dominios.csv')

    # Verificar a data de expiração e enviar e-mail se necessário
    for index, row in dominios_df.iterrows():
        dominio = row['dominio']
        data_expiracao = row['data_expiracao']

        # Verificar se o domínio está perto de expirar
        if check_whois(dominio, data_expiracao):
            send_email(dominio, data_expiracao)

    # Atualizar a lista de domínios (caso haja novos domínios)
    update_csv()

if __name__ == "__main__":
    main()
