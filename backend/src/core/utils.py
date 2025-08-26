from uuid import UUID

def convert_uuids_to_str(data: dict) -> dict:
    """Recursively converts UUID objects in a dictionary to strings."""
    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)
        elif isinstance(value, dict):
            data[key] = convert_uuids_to_str(value)
        elif isinstance(value, list):
            data[key] = [convert_uuids_to_str(item) if isinstance(item, dict) else item for item in value]
    return data