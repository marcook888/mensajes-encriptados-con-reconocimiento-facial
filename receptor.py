from cryptography.fernet import Fernet
import socket
import cv2
import os

# Inicializar el objeto Fernet con la clave recibida
s = socket.socket()
host = '172.16.201.111'
port = 8888
s.bind((host, port))
s.listen(1)

print('Esperando conexión...')
conn, addr = s.accept()

print(f'Conexión establecida desde {addr[0]}:{addr[1]}')

# Recibir la clave enviada por el cliente
clave = conn.recv(1024)

# Inicializar el objeto Fernet con la clave recibida
f = Fernet(clave)

# Enviar una respuesta al cliente
conn.send('Conexión establecida'.encode())

while True:
    # Esperar a recibir un mensaje cifrado del cliente
    mensaje_cifrado = conn.recv(1024)
    
    dataPath = 'C:/Users/marco/OneDrive/Escritorio/foto' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)


    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_recognizer.read('modeloLBPHFace.xml')

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    while True:
        ret,frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
            # LBPHFace
            if result[1] < 70:
                cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                # Descifrar el mensaje y mostrarlo en la consola
                mensaje = f.decrypt(mensaje_cifrado)
                print(f'Cliente: {mensaje.decode()}')
            else:
                print("no reconoce")
                cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
            
        cv2.imshow('frame',frame)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
        
    
    
