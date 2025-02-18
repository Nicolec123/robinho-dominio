import pandas as pd

def update_csv():
    # Aqui você pode configurar uma rotina para coletar novos domínios ou receber de outra fonte
    novos_dominio = {
        'dominio': ['novodominio.com'],
        'data_expiracao': ['2025-10-15']
    }

    # Atualiza o CSV com os novos dados
    novos_df = pd.DataFrame(novos_dominio)
    try:
        # Carrega o CSV existente
        dominios_df = pd.read_csv('data/dominios.csv')

        # Concatenar os novos domínios
        dominios_df = pd.concat([dominios_df, novos_df], ignore_index=True)

        # Salvar novamente no CSV
        dominios_df.to_csv('data/dominios.csv', index=False)
        print("CSV atualizado com novos domínios.")
    
    except Exception as e:
        print(f"Erro ao atualizar o CSV: {e}")
