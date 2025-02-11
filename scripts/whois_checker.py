import whois
from datetime import datetime

def check_whois(dominio, data_expiracao):
    try:
        w = whois.whois(dominio)
        expiration_date = w.expiration_date

        if isinstance(expiration_date, list):  # Alguns domínios podem ter várias datas
            expiration_date = expiration_date[0]

        # Comparar com a data de expiração no CSV
        if expiration_date:
            dias_restantes = (expiration_date - datetime.now()).days
            if dias_restantes <= 30:  # Alerta se estiver a 30 dias ou menos da expiração
                return True
        return False
    except Exception as e:
        print(f"Erro ao verificar {dominio}: {e}")
        return False
