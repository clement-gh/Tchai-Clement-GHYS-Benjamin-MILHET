
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import base64
import os

import requests

def envoyer_donnees_utilisateur(nom_utilisateur, solde, cle_publique):
    url = 'http://localhost:5000/register'
    donnees = {
        'nom': nom_utilisateur,
        'solde': solde,
        'cle_publique': cle_publique
    }

    try:
        reponse = requests.post(url, json=donnees)
        if reponse.status_code == 200:
            print("Données envoyées avec succès !")
        else:
            print(f"Échec de l'envoi des données : {reponse.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")

def generate_keys():
    """Génère une paire de clés publique/privée"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key



def sign_transaction(private_key, transaction_data):
    signature = private_key.sign(
        transaction_data.encode('utf-8'),  # Assurez-vous que les données sont encodées en bytes
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def convert_public_key_to_pem(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    return pem


def register_keys(private_key, public_key):
    '''
    if (os.path.exists("private_key.pem")):
        os.remove("private_key.pem")
    if (os.path.exists("public_key.pem")):
        os.remove("public_key.pem")
    '''
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def create_user():
    # input username and solde
    username = input("Enter your username: ")
    solde = input("Enter your solde: ")
    pi,pu=generate_keys()
    register_keys(pi,pu)
    # load public key
    path = "public_key.pem"
    with open(path, "rb") as f:
        public_key = load_pem_public_key(f.read(), backend=default_backend())

    # convert public key in pem
    pem = convert_public_key_to_pem(public_key)
    # send data to server
    envoyer_donnees_utilisateur(username, solde, pem)




def create_transaction():
    # input username and solde
    username = input("Enter your username: ")
    donneur = input("Enter the username of the donneur: ")
    valeur= input("Enter the amount: ")
    receveur = input("Enter the username of the receveur: ")
    # sign transaction
    private_key= load_pem_private_key(open("private_key.pem", "rb").read(), password=None)

    data = username + donneur + receveur + valeur
    signature = sign_transaction(private_key, data)
    encoded_signature = base64.b64encode(signature).decode('utf-8')
    # send data to server
    url = 'http://localhost:5000/enregisterTransaction'
    donnees = {
        'user': username,
        'receveur': receveur,
        'valeur': valeur,
        'donneur': donneur,
        'signature': encoded_signature
    }

    try:
        reponse = requests.post(url, json=donnees)
        if reponse.status_code == 200:
            print("Transaction envoyée avec succès !")
        else:
            #print(f"Échec de l'envoi de la transaction : {reponse.status_code}")
            print(reponse.text)
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
# main
if __name__ == "__main__":
    while True:
        print("1. Create user")
        print("2. Create transaction")
        print("3. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_user()
        elif choice == "2":
            create_transaction()
        elif choice == "3":
            break
        else:
            print("Invalid choice !")
