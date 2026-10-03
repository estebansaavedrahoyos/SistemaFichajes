from passlib.context import CryptContext

contexto_hash = CryptContext(schemes=["bcrypt"],
                              deprecated="auto")
def hash_contrasena(contrasena : str ) -> str:
    return hash_contrasena.hash(contrasena)

def comprobar_contrasena(contrasena , hashed_contrasena):
    return contexto_hash.verify(contrasena , hashed_contrasena)