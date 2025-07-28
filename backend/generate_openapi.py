# This must be the first import to ensure Firebase is initialized.
# It needs to be imported before the FastAPI app.
import src.firebase_setup

import yaml
import json
from pathlib import Path

# We can now safely import the app
from src.main import app

def generate_openapi_spec():
    """
    Generates the OpenAPI specification and saves it to a YAML file.
    """
    print("Generating OpenAPI specification...")

    # The root directory of the project
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "api"
    output_file = output_dir / "sentinel-invest-backend.yaml"

    # Ensure the output directory exists
    output_dir.mkdir(exist_ok=True)

    # Get the OpenAPI schema from the FastAPI app
    # FastAPI returns a Python dict, which can be converted to JSON/YAML
    openapi_schema = app.openapi()

    # Convert the schema to a JSON string first to handle complex types
    # like datetime objects that YAML dumper might not handle directly.
    openapi_json = json.dumps(openapi_schema, indent=2)
    openapi_data = json.loads(openapi_json)

    # Write the schema to the YAML file
    with open(output_file, 'w') as f:
        yaml.dump(openapi_data, f, sort_keys=False)

    print(f"✅ OpenAPI specification saved to: {output_file}")

if __name__ == "__main__":
    generate_openapi_spec()
