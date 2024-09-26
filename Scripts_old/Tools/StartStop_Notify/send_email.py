from flask_mail import Message
from app import app
from app import mail
from app.models import Clients, ExecutionsTable
from dotenv import dotenv_values

values = dotenv_values()

def getmail(status):
    
    with app.app_context():
        return ExecutionsTable.query.filter_by(pid=status[1]).first()


def email_start(status):
    
    get_mail = getmail(status)
            
    with app.app_context():
        try:
            get_email_admin = Clients.query.filter_by(license_token=get_mail.license_token).first()
        except Exception as e:
            print(e)
        
        
        sendermail = values['MAIL_DEFAULT_SENDER']

        email_admin = get_email_admin.email_admin
        robot = f"Notificações do Robô <{sendermail}>"
        assunto = "Notificação de execução"
        destinatario = get_mail.email
        mensagem = f"""  <h1>Notificação de inicialização - PID {status[1]}</h1>
                        <p>Olá Usuário "{get_mail.nomeuser}", sua execução foi iniciada com sucesso!</p>
                        <ul>
                            <li>Robô: {status[2]}</li>
                            <li>Planilha: {status[4]}</li>
                        </ul>
                        <p>Acompanhe a execução do robô em <b><a href="https://console6.rhsolutions.info/executions">Nosso sistema</a></a></b><p>
                        <p>Por favor, <b>NÃO RESPONDER ESTE EMAIL</b></p>
        """
        
        if get_mail.type_user == "admin" or get_mail.type_user == "super_admin":
            msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem)
        
        else:
            msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem, cc=[email_admin])
            
        mail.send(msg)
        

def email_stop(status):
    
    get_mail = getmail(status)
    
    with app.app_context():
        try:
            get_email_admin = Clients.query.filter_by(license_token=get_mail.license_token).first()
        except Exception as e:
            print(e)
        
        sendermail = values['MAIL_DEFAULT_SENDER']

        email_admin = get_email_admin.email_admin
        robot = f"Notificações do Robô <{sendermail}>"
        assunto = "Notificação de execução"
        destinatario = get_mail.email
        mensagem = f"""  <h1>Notificação de Finalização - PID {status[1]}</h1>
                        <p>Olá {get_mail.nomeuser}, Execução finalizada!</p>
                        <ul>
                            <li>Robô: {status[2]}</li>
                            <li>Planilha: {status[4]}</li>
                        </ul>
                        <p>Verifique o status da execução do robô em <b><a href="https://console6.rhsolutions.info/executions">Nosso sistema</a></a></b><p>
                        <p>Por favor, <b>NÃO RESPONDER ESTE EMAIL</b></p>
        """
        if get_mail.type_user == "admin" or get_mail.type_user == "super_admin":
            
            msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem)
        
        else:
            msg = Message(assunto, sender=robot, recipients=[destinatario], html=mensagem, cc=[email_admin])
            
        mail.send(msg)
            