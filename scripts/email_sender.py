import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

def send_email(dominio, data_expiracao):
    try:
        # Verificar e converter data_expiracao, caso não seja do tipo datetime
        if isinstance(data_expiracao, str):
            try:
                data_expiracao = datetime.fromisoformat(data_expiracao.replace("Z", ""))
            except ValueError:
                raise ValueError(f"Data de expiração inválida para o domínio {dominio}: {data_expiracao}")
        elif not isinstance(data_expiracao, datetime):
            raise TypeError(f"Tipo inválido para data de expiração: {type(data_expiracao)}")

        # Informações do e-mail
        sender_email = getenv("EMAIL_USER")
        sender_password = getenv("EMAIL_PASS")
        receiver_email = "tecnologia@beneficiocerto.com.br"
        smtp_server = getenv("SMTP_SERVER")
        smtp_port = getenv("SMTP_PORT")

        # Criar a mensagem
        subject = f"Alerta de expiração do domínio {dominio}"
        body = f"Ei, o domínio {dominio} vai expirar em {data_expiracao.strftime('%d/%m/%Y')}!\nHora de renovar antes que seja tarde! 🕒"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Enviar o e-mail
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Notificação enviada para {receiver_email}")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

