# Copy to .env and set credentials
def safe_get(d, key, default=None):
    return d.get(key, default)