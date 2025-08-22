import hashlib


def hash_password(password: str) -> str:
	"""Return a simple SHA256 hash of the password."""
	return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
	return hash_password(password) == password_hash

