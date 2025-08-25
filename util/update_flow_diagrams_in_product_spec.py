import re
import argparse
import sys
from pathlib import Path


def parse_source_diagrams(content: str) -> dict[str, str]:
    """
    Parses the auto-generated diagrams markdown file and extracts each flow's
    full mermaid block into a dictionary, keyed by its flowId.
    """
    diagrams = {}
    pattern = re.compile(
        r"## Flow: `(FLOW_[A-Z0-9_]+)`\s*```mermaid\n(.*?)\n```",
        re.DOTALL
    )
    matches = pattern.findall(content)
    for flow_id, mermaid_code in matches:
        full_block = f"```mermaid\n{mermaid_code.strip()}\n```"
        diagrams[flow_id] = full_block
    return diagrams


def update_spec_with_diagrams(spec_content: str, new_diagrams: dict) -> tuple[str, set, set, set]:
    """
    Updates the product spec content by replacing existing flow diagrams
    (identified by %% Flow ID comments) with the corresponding updated versions.
    """
    source_flow_ids = set(new_diagrams.keys())
    spec_flow_ids = set()
    updated_flow_ids = set()

    # Pattern to match ONLY a single ```mermaid block that contains a "%% Flow ID: ..."
    # This version prevents accidental deletion of other diagrams (like architecture diagrams)
    # by ensuring the search for %% Flow ID never crosses the closing ``` fence.
    #
    # Explanation:
    #   - ```mermaid\n   → Match the opening mermaid fence
    #   - ((?:(?!```)[\s\S])*?%%\s*Flow ID:\s*(FLOW_[A-Z0-9_]+)[\s\S]*?) → Match:
    #       * (?:(?!```)[\s\S])*? → Any content, but stop if the closing ``` appears
    #       * %%\s*Flow ID:\s*(FLOW_...) → The Flow ID line (capture the ID in group 2)
    #       * [\s\S]*? → Any remaining diagram content inside the block
    #   - \n``` → Match the closing fence
    #
    # Groups:
    #   Group 1 = Entire diagram body (for replacement)
    #   Group 2 = Flow ID (used as lookup key in new_diagrams)
    placeholder_pattern = re.compile(
        r"```mermaid\n((?:(?!```)[\s\S])*?%%\s*Flow ID:\s*(FLOW_[A-Z0-9_]+)[\s\S]*?)\n```"
    )

    def replacement_func(match):
        flow_id = match.group(2)
        spec_flow_ids.add(flow_id)

        if flow_id in new_diagrams:
            updated_flow_ids.add(flow_id)
            return new_diagrams[flow_id]
        else:
            return match.group(0)

    updated_content = placeholder_pattern.sub(replacement_func, spec_content)

    in_source_not_in_spec = source_flow_ids - spec_flow_ids
    in_spec_not_in_source = spec_flow_ids - source_flow_ids

    return updated_content, updated_flow_ids, in_source_not_in_spec, in_spec_not_in_source


def main():
    parser = argparse.ArgumentParser(
        description="Synchronizes Mermaid diagrams into the main product spec by matching Flow IDs."
    )
    parser.add_argument(
        "diagrams_file",
        type=Path,
        help="Path to the source file containing the generated Mermaid diagrams."
    )
    parser.add_argument(
        "spec_file",
        type=Path,
        help="Path to the product spec file to be updated."
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output_file",
        type=Path,
        default=None,
        help="Optional: Path to write the updated spec to. If omitted, the input spec file will be overwritten."
    )
    args = parser.parse_args()

    try:
        with open(args.diagrams_file, 'r', encoding='utf-8') as f:
            diagrams_content = f.read()
        with open(args.spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)

    new_diagrams = parse_source_diagrams(diagrams_content)
    if not new_diagrams:
        print("No diagrams found in the source file. Nothing to do.", file=sys.stderr)
        sys.exit(0)

    updated_content, updated, in_source_only, in_spec_only = update_spec_with_diagrams(spec_content, new_diagrams)

    output_path = args.output_file if args.output_file else args.spec_file

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
    except IOError as e:
        print(f"Error writing to output file '{output_path}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Diagram synchronization complete. Output written to '{output_path}'.\n")

    if updated:
        print("--- Successfully Updated Diagrams ---")
        for flow_id in sorted(list(updated)):
            print(f"- {flow_id}")
        print()

    if in_source_only:
        print("--- ⚠️ Diagrams in Source but NOT in Product Spec ---")
        for flow_id in sorted(list(in_source_only)):
            print(f"- {flow_id}")
        print()

    if in_spec_only:
        print("--- ⚠️ Diagrams in Product Spec but NOT in Source ---")
        for flow_id in sorted(list(in_spec_only)):
            print(f"- {flow_id}")
        print()


if __name__ == "__main__":
    main()

