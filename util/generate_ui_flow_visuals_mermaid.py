import yaml
import argparse
import sys
from pathlib import Path

def generate_mermaid_from_flow(flow_data: dict) -> str:
    """Generates Mermaid state diagram syntax from a single flow definition."""
    
    if not flow_data:
        return "# Flow data is empty."

    lines = ["stateDiagram-v2"]
    initial_state = flow_data.get('initialState')

    # --- NEWLY ADDED LINE ---
    # Add the transition from the start state to the initial state
    if initial_state:
        lines.append(f'    [*] --> {initial_state}')
    # --- END OF NEW LINE ---
    
    # Process all states and their transitions
    for state in flow_data.get('states', []):
        state_name = state['name']
        
        # Process user-triggered events
        if 'events' in state:
            for event, target_state in state['events'].items():
                lines.append(f'    {state_name} --> {target_state} : {event}')

        # Process automated entryAction transitions
        if 'entryAction' in state and 'transitions' in state['entryAction']:
            for outcome, target_state in state['entryAction']['transitions'].items():
                lines.append(f'    {state_name} --> {target_state} : {outcome}')
        
        # Process automated exitAction transitions
        if 'exitAction' in state:
            action_name = state['exitAction'].get('action', 'exit')
            # In Mermaid, [*] represents the end state
            lines.append(f'    {state_name} --> [*] : {action_name}')
        
        # Process subflows (optional, for more detail)
        if 'subflow' in state:
            subflow_id = state['subflow']['flowId']
            on_completion = state['subflow']['onCompletion']
            on_cancel = state['subflow']['onCancel']
            lines.append(f'    state "{subflow_id}" as {state_name}_subflow')
            lines.append(f'    {state_name} --> {state_name}_subflow')
            lines.append(f'    {state_name}_subflow --> {on_completion} : onCompletion')
            lines.append(f'    {state_name}_subflow --> {on_cancel} : onCancel')


    return "\n".join(lines)

def main():
    """Main function to parse arguments and run the generator."""
    parser = argparse.ArgumentParser(
        description="Generate Mermaid state diagram code from a ui_flows_spec.yaml file."
    )
    parser.add_argument("spec_file", type=Path, help="Path to the ui_flows_spec.yaml file.")
    parser.add_argument("flow_id", help="The flowId to generate the diagram for.")
    
    args = parser.parse_args()

    if not args.spec_file.is_file():
        print(f"Error: File not found at '{args.spec_file}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.spec_file, 'r') as f:
            # Use load_all since the YAML file uses '---' separators
            all_flows = list(yaml.safe_load_all(f))
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}", file=sys.stderr)
        sys.exit(1)

    # Find the specific flow the user asked for
    target_flow = None
    for flow in all_flows:
        if flow and flow.get('flowId') == args.flow_id:
            target_flow = flow
            break
    
    if not target_flow:
        print(f"Error: flowId '{args.flow_id}' not found in the spec file.", file=sys.stderr)
        sys.exit(1)

    # Generate and print the Mermaid code
    mermaid_code = generate_mermaid_from_flow(target_flow)
    print("```mermaid")
    print(mermaid_code)
    print("```")

if __name__ == "__main__":
    main()
    
    