import requests
from datetime import datetime


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
        # URL base do RDAP
        url = f"https://rdap.registro.br/domain/{dominio}"

        # Faz a requisição à API RDAP
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Obtém a data de expiração do domínio
            expiration_date_str = data.get("events", [])[0].get("eventDate")
            expiration_date = datetime.strptime(
                expiration_date_str, "%Y-%m-%dT%H:%M:%SZ")

            # Calcula os dias restantes
            dias_restantes = (expiration_date - datetime.now()).days

            # Verifica se está perto de expirar
            if dias_restantes <= 30:
                return True
        else:
            print(
                f"Erro ao consultar domínio {dominio}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro ao verificar {dominio}: {e}")
        return False
