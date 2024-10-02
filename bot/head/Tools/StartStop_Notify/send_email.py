from flask_mail import Message
from flask import current_app

from dotenv import dotenv_values

from app import mail
from app.models import Users, Executions

app = current_app
values = dotenv_values()
from app import db
  
def email_start(execution: Executions) -> None:
    
    admins: list[str] = []
    pid = execution.pid
    usr: Users = execution.user[0]
    url_web = dotenv_values().get("url_web")
    
    display_name = execution.bot[0].display_name
    xlsx = execution.arquivo_xlsx

    try:
        for adm in usr.licenses[0].admins:
            admins.append(adm.email)
            
    except Exception as e:
        print(e)
            
    with app.app_context():
        
        url_web = dotenv_values().get("url_web")
        sendermail = values['MAIL_DEFAULT_SENDER']

        robot = f"Notificações do Robô <{sendermail}>"
        assunto = "Notificação de inicializaçã"
        destinatario = usr.email
        mensagem = f"""  <h1>Notificação de inicialização - PID {pid}</h1>
                        <p>Olá {usr.nome_usuario}, sua execução foi iniciada com sucesso!</p>
                        <ul>
                            <li>Robô: {display_name}</li>
                            <li>Planilha: {xlsx}</li>
                        </ul>
                        <p>Acompanhe a execução do robô em <b><a href="{url_web}/logs_bot/{pid}">Nosso sistema</a></b><p>
                        <p>Por favor, <b>NÃO RESPONDER ESTE EMAIL</b></p>
        """
        
        msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem)
        if not usr.email in admins:
            msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem, cc=admins)
        
        mail.send(msg)
            

def email_stop(execution: Executions) -> None:
    
    admins: list[str] = []
    pid = execution.pid
    usr: Users = execution.user[0]
    url_web = dotenv_values().get("url_web")
    
    display_name = execution.bot[0].display_name
    xlsx = execution.arquivo_xlsx

    try:
        for adm in usr.licenses[0].admins:
            admins.append(adm.email)
            
    except Exception as e:
        print(e)
            
    with app.app_context():
        
        url_web = dotenv_values().get("url_web")
        sendermail = values['MAIL_DEFAULT_SENDER']

        robot = f"Notificações do Robô <{sendermail}>"
        assunto = "Notificação de Finalização"
        destinatario = usr.email
        mensagem = f"""  <h1>Notificação de Finalização - PID {pid}</h1>
                        <p>Olá {usr.nome_usuario}, Execução finalizada!</p>
                        <ul>
                            <li>Robô: {display_name}</li>
                            <li>Planilha: {xlsx}</li>
                        </ul>
                        <p>Verifique o status da execução do robô em <b><a href="{url_web}/logs_bot/{pid}">Nosso sistema</a></b><p>
                        <p>Por favor, <b>NÃO RESPONDER ESTE EMAIL</b></p>
        """

        msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem)
        if not usr.email in admins:
            msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem, cc=admins)
        
        mail.send(msg)
            
            