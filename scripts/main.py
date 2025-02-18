import pandas as pd
from datetime import datetime
import os
import sys

# Adiciona o diretório 'scripts' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

# Agora os módulos dentro de 'scripts' podem ser importados
from whois_checker import check_whois
from email_sender import send_email
from update_csv import update_csv



def main():
    try:
        print("Iniciando o script...")

        # Carregar lista de domínios
        print("Carregando lista de domínios do arquivo 'data/dominios.csv'...")
        dominios_df = pd.read_csv(
            'data/dominios.csv', header=None, names=["dominio", "data_expiracao"], dtype=str)

        # Verificar se as colunas esperadas estão no DataFrame
        if "dominio" not in dominios_df.columns or "data_expiracao" not in dominios_df.columns:
            raise ValueError(
                "O arquivo 'dominios.csv' não contém as colunas esperadas: 'dominio' e 'data_expiracao'."
            )

        print(f"Total de domínios carregados: {len(dominios_df)}")

        # Iterar sobre cada linha do DataFrame
        for index, row in dominios_df.iterrows():
            dominio = row['dominio']
            data_expiracao = row['data_expiracao']

            print(f"\nProcessando domínio: {dominio}")
            print(f"Data de expiração registrada: {data_expiracao}")

            # Verificar se o domínio está perto de expirar
            if check_whois(dominio, data_expiracao):
                print(f"Domínio {dominio} está próximo de expirar. Enviando e-mail de alerta...")
                send_email(dominio, data_expiracao)
            else:
                print(f"Domínio {dominio} não está próximo de expirar.")

        # Atualizar a lista de domínios
        print("\nAtualizando a lista de domínios...")
        update_csv()

    except FileNotFoundError:
        print("Erro: O arquivo 'data/dominios.csv' não foi encontrado. Certifique-se de que o caminho está correto.")
    except ValueError as e:
        print(f"Erro no formato do arquivo CSV: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()

