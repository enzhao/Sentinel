import re
import json
from pathlib import Path

def generate_messages():
    """
    Parses product_spec.md to extract message keys and strings,
    then generates JSON message files for both backend and frontend.
    """
    spec_path = Path(__file__).parent.parent / "product_spec.md"
    config_dir = Path(__file__).parent.parent / "config"
    frontend_locales_dir = Path(__file__).parent.parent / "frontend" / "src" / "locales"

    if not spec_path.exists():
        print(f"Error: {spec_path} not found.")
        return

    print(f"Reading spec from: {spec_path}")
    spec_content = spec_path.read_text(encoding="utf-8")

    # Regex to find message definitions like:
    # - **P_I_1001**: "Portfolio '{name}' created successfully with ID {portfolioId}."
    message_regex = re.compile(r"-\s*\*\*(P_[A-Z]_\d+|U_[A-Z]_\d+|R_[A-Z]_\d+|M_[A-Z]_\d+|N_[A-Z]_\d+)\*\*:\s*\"(.*?)\"", re.DOTALL)

    messages = {}
    matches = message_regex.finditer(spec_content)

    for match in matches:
        key = match.group(1).strip()
        value = match.group(2).strip()
        messages[key] = value
        print(f"  Found: {key} -> \"{value}\"")

    if not messages:
        print("Warning: No messages found in the spec. Output files will be empty.")
        return

    # Create directories if they don't exist
    config_dir.mkdir(exist_ok=True)
    frontend_locales_dir.mkdir(exist_ok=True)

    backend_json_path = config_dir / "messages.json"
    frontend_json_path = frontend_locales_dir / "en.json"

    # Write backend file
    try:
        with open(backend_json_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully generated backend messages at: {backend_json_path}")
    except IOError as e:
        print(f"Error writing to {backend_json_path}: {e}")


    # Write frontend file
    try:
        with open(frontend_json_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        print(f"Successfully generated frontend messages at: {frontend_json_path}")
    except IOError as e:
        print(f"Error writing to {frontend_json_path}: {e}")


if __name__ == "__main__":
    generate_messages()
