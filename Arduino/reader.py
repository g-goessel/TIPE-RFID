"""
Programme Python permettant de récupérer puis de décoder le message de la carte RFID
"""
import serial
import numpy as np
from statistics import mean

try:
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200)
    except:
        ser = serial.Serial('/dev/ttyACM1', 115200)
except:
    print('N\'a pas pu initialiser le port série')

def read(ser):
    # On récupère les durées des pulsations longues et courtes sur un échatillon de 50 mesures
    echantillon = []
    # on vide le cache du port série + on lit une ligne éventuellement troncquée
    ser.flushInput()
    ser.readline()
    for i in range(50):
        echantillon.append(int(ser.readline().decode().replace("\r\n","")[2:]))
    moy = mean(echantillon)
    longs = [sample for sample in echantillon if sample > moy]
    courts = [sample for sample in echantillon if sample < moy]
    court = mean(courts)
    long  = mean(longs)
    print(long,court)
    # Pour différencier un long d'un court on compare la durée de la pulsation à la moyenne
    moy = mean([court,long])
    #on vide encore le cache (juste pour le fun)
    ser.flushInput()
    ser.readline()
    bits=[]
    message = ser.readline().decode().replace("\r\n","")
    # On choisit arbitrairement le début du message comme une longue pulsation basse
    while message[0] != 'l' or int(message[2:]) < moy:
        message = ser.readline().decode().replace("\r\n","")
    # On a alors un 1
    bits+=[1,0]
    # On va ensuite décoder les 200 bits suivants (plus il y a de fous, plus on rigole)
    for i in range(200):
        print(i)
        duree = int(ser.readline().decode().replace("\r\n","")[2:])
        last = bits[-1]
        if duree > moy:
            # On a une pulsation longue donc on passe au bit opposé
            bits.append(int(not last))
        else :
            # On a une pulsation courte donc on conserve le même bit
            bits.append(last)
            ser.readline()
    return bits

def read3(ser):
    ser.flushInput()
    a=ser.readline().decode().replace("\r\n","")
    while a != "0" and a != "1":
        a = ser.readline().decode().replace("\r\n","")
    aquisition = []
    # on néglige les 2 premières mesures
    ser.readline()
    ser.readline()
    echantillon=[]
    for i in range(297):
        aquisition.append(ser.readline().decode().replace("\r\n",""))
    for i in range(50):
        echantillon.append(int(aquisition[i]))
    moy = mean(echantillon)
    longs = [sample for sample in echantillon if sample > moy]
    courts = [sample for sample in echantillon if sample < moy]
    court = mean(courts)
    long  = mean(longs)
    # Pour différencier un long d'un court on compare la durée de la pulsation à la moyenne
    moy = mean([court,long])
    for i in range(len(aquisition)):
        if a == '0':
            #le premier était un haut
            if i % 2 == 0:
                aquisition[i] = 'h '+str(aquisition[i])
            else:
                aquisition[i] = 'l '+str(aquisition[i])
        else :
            #le premier était un bs
            if i % 2 == 1:
                aquisition[i] = 'h '+str(aquisition[i])
            else:
                aquisition[i] = 'l '+str(aquisition[i])
    message = aquisition.pop(0)
    # On choisit arbitrairement le début du message comme une longue pulsation basse
    while message[0] != 'l' or int(message[2:]) < moy:
        message = aquisition.pop(0)
    # On a alors un 1
    bits=[1,0]
    # On va ensuite décoder les bits restants
    while len(aquisition)> 2:
        duree = int(aquisition.pop(0)[2:])
        last = bits[-1]
        if duree > moy:
            # On a une pulsation longue donc on passe au bit opposé
            bits.append(int(not last))
        else :
            # On a une pulsation courte donc on conserve le même bit
            bits.append(last)
            aquisition.pop(0)
    return bits

def read2(ser):
    # On récupère les durées des pulsations longues et courtes sur un échatillon de 50 mesures
    echantillon = []
    # on vide le cache du port série + on lit une ligne éventuellement troncquée
    ser.flushInput()
    ser.readline()
    for i in range(50):
        echantillon.append(int(ser.readline().decode().replace("\r\n","")[2:]))
    moy = mean(echantillon)
    longs = [sample for sample in echantillon if sample > moy]
    courts = [sample for sample in echantillon if sample < moy]
    court = mean(courts)
    long  = mean(longs)
    print(long,court)
    # Pour différencier un long d'un court on compare la durée de la pulsation à la moyenne
    moy = mean([court,long])
    #on vide encore le cache (juste pour le fun)
    ser.flushInput()
    ser.readline()
#----------------------------------------------------------------------------------------------
    #Deuxième méthode : motifs

    bits = []
    message = ser.readline().decode().replace("\r\n","")
    # On choisit arbitrairement le début du message comme une longue pulsation basse
    while message[0] != 'l' or int(message[2:]) < moy:
        message = ser.readline().decode().replace("\r\n","")

    # On a alors un 1
    bits.append(1)
    tableau = []
    tableau.append("l")
    for i in range(200):
        message = ser.readline().decode().replace("\r\n","")
        hauteur = message[0]
        duree = int(message[2:])
        if duree > moy:
            tableau.append(hauteur)
            tableau.append(hauteur)
        else:
            tableau.append(hauteur)

    if len(tableau)%3 == 0:
        tableau.pop()

    compteur = 0
    for i in range(len(tableau)//2):
        if tableau[compteur] == "h" and tableau[compteur+1] == "l":
            bits.append(1)
        elif tableau[compteur] == "l" and tableau[compteur+1] == "h":
            bits.append(0)
        compteur += 2

    return bits
    #----------------------------------------------------------------------------------------------


def find_header(l):
    check = [1]*9
    init = None
    for i in range(0,len(l)-64):
        test = [l[k] for k in range(i,i+9)]
        if test == check :
            init = i+1
            break
    if init == None:
        print('n\'a pas trouvé de header')
        return 1
    else :
        #return l[init+9:init+64]
        return l[init+8:init+63]

def check(l):
    if l == 1 or len(l) != 55:
        return 1
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
        bits += str(ligne.tolist()).replace('[','').replace(']','').replace(', ','')
    return int(bits,2)

def degroup(l):
    resultat=[]
    for i in l:
        if i==1:
            resultat += [1,0]
        else:
            resultat += [0,1]
    return resultat
    
def auto3(ser):
    ser.flushInput()
    a = decodage(check(find_header(read3(ser))))
    if a == 'erreur':
        return auto3(ser)
    else:
        return a

"""
if __name == '__main__':
    message = read()
    message = find_header(message)
    message = check(message)
    print(decodage(message))
"""
