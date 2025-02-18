import pandas as pd
from datetime import datetime

from scripts.whois_checker import check_whois
from scripts.email_sender import send_email
from scripts.update_csv import update_csv


def main():
    try:
        # Carregar lista de domínios
        # Especificar que o arquivo pode não ter cabeçalhos
        dominios_df = pd.read_csv(
            'data/dominios.csv', header=None, names=["dominio", "data_expiracao"], dtype=str)

        # Verificar se as colunas esperadas estão no DataFrame
        if "dominio" not in dominios_df.columns or "data_expiracao" not in dominios_df.columns:
            raise ValueError(
                "O arquivo 'dominios.csv' não contém as colunas esperadas: 'dominio' e 'data_expiracao'.")

        # Iterar sobre cada linha do DataFrame
        for index, row in dominios_df.iterrows():
            dominio = row['dominio']
            data_expiracao = row['data_expiracao']

            # Verificar se o domínio está perto de expirar
            if check_whois(dominio, data_expiracao):
                send_email(dominio, data_expiracao)

        # Atualizar a lista de domínios (caso haja novos domínios)
        update_csv()
    except FileNotFoundError:
        print("Erro: O arquivo 'data/dominios.csv' não foi encontrado. Certifique-se de que o caminho está correto.")
    except ValueError as e:
        print(f"Erro no formato do arquivo CSV: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()
