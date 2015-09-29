"""
Programme Python permettant de récupérer puis de décoder le message de la carte RFID
"""

import serial
import numpy as np
from statistics import mean

ser = serial.Serial('/dev/ttyACM0', 115200)

def read(ser):
    ser.flushInput()
    first=ser.readline().decode().replace("\r\n","")
    while first != "0" and first != "1":
        first = ser.readline().decode().replace("\r\n","")
    # on néglige les 2 premières mesures non précises
    ser.readline()
    ser.readline()
    acquisition = []
    for i in range(297):
        a=ser.readline().decode().replace("\r\n","")
        aquisition.append(a)
    for i in range(len(aquisition)):
        if first == '0':
            #si la première était une haute
            if i % 2 == 0:
                # toutes les impulsions paires le sont
                aquisition[i] = 'h '+str(aquisition[i])
            else:
                #les impaires sont basses
                aquisition[i] = 'b '+str(aquisition[i])
        else :
            #si la première était une basse...
            if i % 2 == 1:
                aquisition[i] = 'h '+str(aquisition[i])
            else:
                aquisition[i] = 'b '+str(aquisition[i])
    #les impulsions sont décrites par une chaine "b 245"

    #----------------------------------------------------------------------#

    message = aquisition.pop(0) # on enlève le bit first
    echantillon = []
    for i in range(50):
        echantillon.append(int(aquisition[i][2:]))
    moy = mean(echantillon)
    longues = [i for i in echantillon if i > moy]
    courtes = [i for i in echantillon if i < moy]
    courte = mean(courtes)
    longue  = mean(longues)
    # Pour différencier une longue d'une courte
    # on compare la durée de l'impulsion à la moyenne
    moy = mean([courte,longue])

    #----------------------------------------------------------------------#

    # On choisit arbitrairement le début du message
    # comme une longue impulsion basse
    while message[0] != 'b' or int(message[2:]) < moy:
        message = aquisition.pop(0)
    # On a alors un 1 puis un 0
    bits=[1,0]
    # On décode les bits restants par récurrence
    while len(aquisition)> 2:
        duree = int(aquisition.pop(0)[2:])
        last = bits[-1]
        if duree > moy:
            # Impulsion longue donc le bit est opposé
            bits.append(int(not last))
        else :
            # Impulsion courte donc le bit est identique
            bits.append(last)
            aquisition.pop(0)
    return bits

def find_header(l):
    header = [1]*9
    init = None
    for i in range(0,len(l)-64):
        test = [l[k] for k in range(i,i+9)]
        if test == header
            init = i+1
            break
    if init == None:
        return 1
    else :
        # contient les 64-9 bits du message
        return l[init+8:init+63]

def check(l):
    if l == 1 or len(l) != 55:
        return 1
    # on découpe en 11 lignes
    arr = np.array(np.array_split(l,11))
    for ligne in arr[:-1 ]:
        check = sum(ligne[:4])%2
        if check != ligne[-1]:
            print(ligne)
            return 1
    message = arr[:-1,:-1]
    return message

def decodage(l):
    if type(l) == int:
        return "erreur"
    bits = ''
    for ligne in l:
        bits += ''.join(ligne.tolist())
    return int(bits,2)

def auto(ser):
    ser.flushInput()
    nb_lectures = 1
    a = decodage(check(find_header(read(ser))))
    while a == 'erreur':
        nb_lectures += 1
        a = decodage(check(find_header(read(ser))))
    else:
        return a
