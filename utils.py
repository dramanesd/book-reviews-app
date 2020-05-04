from werkzeug.security import generate_password_hash, check_password_hash


def set_password(password):
  return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

def get_password(hash_password, password):
  return check_password_hash(hash_password, password)