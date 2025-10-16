import bcrypt

def hash_password(password):
    
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    return hash

def verify_password(password, hash):    

    bytes = password.encode("utf-8")
    hash = hash.encode("utf-8")
    result = bcrypt.checkpw(bytes, hash)

    return result
