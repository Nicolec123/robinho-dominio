from datetime import datetime

import requests


def check_whois(dominio, data_expiracao):
    """
    Verifica se o domínio está próximo de expirar.

    Args:
        dominio (str): Nome do domínio a ser verificado.
        data_expiracao (str): Data esperada de expiração no formato ISO 8601.

    Returns:
        bool | None: Retorna True se o domínio está próximo de expirar, False se não está,
        ou None em caso de erro.
    """
    try:
        print(f"Consultando informações WHOIS para o domínio: {dominio}")

        # URL base do RDAP
        url = f"https://rdap.registro.br/domain/{dominio}"

        # Faz a requisição à API RDAP
        print(f"Realizando requisição para: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            print("Requisição bem-sucedida. Processando dados...")

            data = response.json()

            # Procura pelo campo "EXPIRAÇÃO" nos eventos
            expiration_event = next(
                (event for event in data.get("events", []) if event.get("eventAction", "").upper() == "EXPIRATION"), None
            )

            if not expiration_event:
                print(f"Erro: Não foi possível encontrar o evento de 'EXPIRAÇÃO' para o domínio {dominio}.")
                return False

            expiration_date_str = expiration_event.get("eventDate")
            if not expiration_date_str:
                print(f"Erro: A data de expiração está ausente no evento de 'EXPIRAÇÃO' para o domínio {dominio}.")
                return False

            # Convertendo a data para objeto datetime
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%dT%H:%M:%SZ")

            # Calcula os dias restantes
            dias_restantes = (expiration_date - datetime.now()).days
            print(f"Dias restantes para expiração: {dias_restantes}")

            # Verifica se está perto de expirar
            if dias_restantes <= 30:
                print(f"Alerta: O domínio {dominio} expira em menos de 30 dias.")
                return True
            else:
                print(f"O domínio {dominio} tem mais de 30 dias restantes.")
                return False
        else:
            print(f"Erro ao consultar domínio {dominio}: Código HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro ao verificar domínio {dominio}: {e}")
        return False
