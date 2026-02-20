from passlib.context import CryptContext


class Security:
    def __init__(self):
        self.CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    def verify_password(self, password: str, hash_password: str) -> bool:
        return self.CRIPTO.verify(password, hash_password)

    def generate_hashed_password(self, password: str) -> str:
        return self.CRIPTO.hash(password)

security: Security = Security()