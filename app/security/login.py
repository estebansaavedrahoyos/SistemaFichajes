from passlib.context import CryptContext

contexto_hash = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_contrasena(contrasena: str) -> str:
    return contexto_hash.hash(contrasena)


def comprobar_contrasena(contrasena: str, contrasena_hasheada: str) -> bool:
    return contexto_hash.verify(contrasena, contrasena_hasheada)
