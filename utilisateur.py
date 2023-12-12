
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import base64

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



def sign_transaction(private_key, data):
    signature = private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.urlsafe_b64encode(signature).decode()

def convert_public_key_to_pem(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")
    return pem


def register_keys(private_key, public_key):
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
    register_keys(
        generate_keys()[0],generate_keys()[1]
    )
    path = "public_key.pem"
    with open(path, "rb") as f:
        public_key = load_pem_public_key(f.read(), backend=default_backend())

    # convert public key in pem
    pem = convert_public_key_to_pem(public_key)
    # send data to server
    envoyer_donnees_utilisateur(username, solde, pem)
    print("User created !")




