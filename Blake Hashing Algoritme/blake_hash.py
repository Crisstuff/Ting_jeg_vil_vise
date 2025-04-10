import json
import hashlib
import random
import os
import secrets

# Denne siden er for generering av hashed passord og account nummer


DATA_FILE = 'data.json'

# Funksjon for å laste inn brukerdata fra fil
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Funksjon for å lagre brukerdata til fil
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# For å generere et tilfeldig bankkontonummer
def generate_account_number():
    return random.randint(100000, 999999)

# Funksjon for å generere en tilfeldig salt
def generate_salt(length=16):
    return secrets.token_hex(length)

# Funksjon for å hashe et passord med salt og key stretching
def hash_password(password, salt=None, iterations=100000, digest_size=32):
    if salt is None:
        salt = generate_salt()

    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    data = password_bytes + salt_bytes

    hasher = hashlib.blake2b(digest_size=digest_size)
    for _ in range(iterations):
        hasher.update(data)
        data = hasher.digest()

    return hasher.hexdigest(), salt

# Funksjon for å verifisere et passord
def verify_password(password, hashed_password, salt, iterations=100000, digest_size=32):
    new_hash, _ = hash_password(password, salt, iterations, digest_size)
    return new_hash == hashed_password

def generate_account_number():
    # Faste delen av kontonummeret
    fixed_part = "8317"
    
    # Generer tilfeldige tall
    random_part1 = random.randint(1000, 9999)  # 4 sifre
    random_part2 = random.randint(100, 999)   # 3 sifre
    
    # Kombiner til kontonummer
    account_number = f"{fixed_part}.{random_part1}.{random_part2}"
    return account_number

# Eksempel på bruk
account_number = generate_account_number()



# Funksjon for å opprette en ny bruker
def create_user():
    name = input("Skriv inn ditt navn: ")
    password = input("Skriv inn et passord: ")
    balance = 200.0

    # Hash passordet og generer salt
    hashed_password, salt = hash_password(password)

    # Lagre brukerdata
    user_data = {
        'name': name,
        'hashed_password': hashed_password,
        'salt': salt,
        'balance': balance,
        'transactions': []
    }

    data = load_data()
    data[account_number] = user_data
    save_data(data)

    print(f"\nTakk {name}! Din konto er opprettet.")
    print(f"Ditt kontonummer er: {account_number}\n")

# Funksjon for å logge inn en bruker
def login():
    account_number = input("Skriv inn ditt kontonummer: ")
    password = input("Skriv inn ditt passord: ")
    data = load_data()

    if account_number in data:
        user_data = data[account_number]
        hashed_password = user_data['hashed_password']
        salt = user_data['salt']

        if verify_password(password, hashed_password, salt):
            print(f"\nVelkommen tilbake, {user_data['name']}!")
            return user_data
        else:
            print("Feil passord. Prøv igjen.\n")
    else:
        print("Kontonummer ikke funnet. Prøv igjen.\n")

    return None

# Hovedmeny
def main():
    while True:
        print("1. Opprett ny bruker")
        print("2. Logg inn")
        print("3. Avslutt")
        choice = input("Velg et alternativ: ")

        if choice == '1':
            create_user()
        elif choice == '2':
            user = login()
            if user:
                # Her kan du legge til funksjonalitet for innloggede brukere
                print(f"Du er logget inn som {user['name']}.")
        elif choice == '3':
            print("Avslutter...")
            break
        else:
            print("Ugyldig valg. Prøv igjen.\n")

# Kjør hovedmenyen
if __name__ == "__main__":
    main()