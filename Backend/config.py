import string
import secrets

class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///travel_buddy.db'

    @staticmethod
    def generate_secret_key(length=24):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = Config.generate_secret_key()
    print("Generated Secret Key:", secret_key)
