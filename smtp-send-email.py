import smtplib

nombre_servidor_smtp = 'Nombre del servidor SMTP'

nombre_originario = 'Nombre del originario del correo'
originario = 'Correo electrónico del originario'
contraseña = 'Contraseña del originario del correo'
destinatario = 'Correo electrónico del destinatario'
asunto = 'Asunto del correo'
mensaje = 'Mensaje del correo'

try:
    smtp = smtplib.SMTP(nombre_servidor_smtp,587)
    smtp.starttls()
    smtp.login(originario,contraseña)
    encabezado = 'To:' + destinatario + '\n' + 'From:' + nombre_originario + '<' + originario + '>' + '\n' + 'Subject:' + asunto + '\n'
    print(encabezado)
    smtp.sendmail(originario,destinatario,encabezado + '\n' + mensaje + '\n')
    print('OK')
except Exception as e:
    print(e)
finally:
    smtp.close()