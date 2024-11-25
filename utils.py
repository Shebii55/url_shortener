import uuid
import base64

def generate_short_url():
    # Generate a short URL from UUID and encode it
    unique_id = uuid.uuid4()
    uuid_bytes = unique_id.bytes
    encoded = base64.urlsafe_b64encode(uuid_bytes).decode('ascii').rstrip('=')
    
    # Return the first 8 characters as the short URL
    return encoded[:8]
