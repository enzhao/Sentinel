import yaml
import argparse
import sys
from pathlib import Path

# --- NEW: Emoji mapping for different state types ---
EMOJI_MAP = {
    "home": "🏠",
    "dashboard": "📊",
    "view": "👁️",
    "list": "📋",
    "detail": "📄",
    "form": "📝",
    "input": "⌨️",
    "edit": "✏️",
    "add": "➕",
    "submitting": "⏳",
    "loading": "⏳",
    "checking": "🔍",
    "searching": "🔍",
    "success": "✅",
    "confirm": "🤔",
    "select": "👆",
    "error": "❌",
    "delete": "🗑️",
    "move": "🚚",
    "import": "📥",
    "review": "🧐",
    "rules": "⚖️",
    "idle": "💤",
}

def get_emoji_for_state(state_name: str) -> str:
    """Finds a suitable emoji for a given state name."""
    lower_name = state_name.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lower_name:
            return f"{emoji} "
    return ""

def build_view_map(all_flows_data: list) -> dict:
    """Builds a map of (flowId, stateName) to viewId for easy lookup."""
    view_map = {}
    for flow in all_flows_data:
        if not flow: continue
        flow_id = flow.get('flowId')
        if flow_id:
            for state in flow.get('states', []):
                state_name = state.get('name')
                if state_name and 'renders' in state:
                    view_map[(flow_id, state_name)] = state.get('renders')
                # Recursively check for nested states
                if 'states' in state:
                    nested_map = build_view_map([{'states': state['states'], 'flowId': flow_id}])
                    view_map.update(nested_map)
    return view_map

def generate_mermaid_for_states(states: list, flow_id: str, view_map: dict) -> list[str]:
    """
    Recursively generates Mermaid state diagram lines for a list of states.
    """
    lines = []
    
    for state in states:
        state_name = state['name']
        emoji = get_emoji_for_state(state_name)
        view_id = view_map.get((flow_id, state_name), '')
        
        # --- REVISED: Create a descriptive label with emoji and view ---
        label_content = f'{emoji}{state_name}'
        if view_id:
            label_content += f'<br/><font size="2"><i>({view_id})</i></font>'
        
        # Define the state with its new label
        lines.append(f'    state "{label_content}" as {state_name}')

        if 'states' in state:
            lines.append(f'    state "{state_name}" as {state_name} {{')
            nested_lines = generate_mermaid_for_states(state.get('states', []), flow_id, view_map)
            for line in nested_lines:
                lines.append(f'        {line}')
            lines.append('    }')
        
        if 'events' in state:
            for event, target_state in state['events'].items():
                if target_state.startswith('(exit flow'):
                    exit_node_id = f'{state_name}_exit_{event}'
                    exit_label = '(exit)'
                    if "onCancel" in target_state:
                        exit_label = '🛑 (exit onCancel)'
                    lines.append(f'    state "{exit_label}" as {exit_node_id}')
                    lines.append(f'    {state_name} --> {exit_node_id} : {event}')
                    lines.append(f'    {exit_node_id} --> [*]')
                else:
                    lines.append(f'    {state_name} --> {target_state} : {event}')

        if 'entryAction' in state and 'transitions' in state.get('entryAction', {}):
            for outcome, target_state in state['entryAction']['transitions'].items():
                target = '[*]' if target_state.startswith('(exit flow)') else target_state
                lines.append(f'    {state_name} --> {target} : {outcome}')
        
        if 'activates' in state:
            for activation in state.get('activates', []):
                target_flow = activation.get('flowId', '')
                target_state = activation.get('targetState', '')
                if target_flow and target_state:
                    lines.append(f'    note right of {state_name}')
                    lines.append(f'        activates: {target_state} in {target_flow}')
                    lines.append(f'    end note')

        if 'exitAction' in state:
            action = state['exitAction'].get('action', 'exit')
            target = state['exitAction'].get('target', '')
            label = f"{action} {target}".strip()
            
            exit_node_id = f'{state_name}_exit_action'
            # --- REVISED: Use emoji for navigation exit actions ---
            if action == 'NAVIGATE_TO' and target:
                label = f'➡️ {target}'

            lines.append(f'    state "{label}" as {exit_node_id}')
            lines.append(f'    {state_name} --> {exit_node_id}')
            lines.append(f'    {exit_node_id} --> [*]')

        if 'subflow' in state:
            subflow = state['subflow']
            target_flow_id = subflow['flowId']
            on_completion = subflow.get('onCompletion', '(exit flow)')
            on_cancel = subflow.get('onCancel', '(exit flow)')
            
            label = f'➡️ subflow: {target_flow_id}'
            lines.append(f'    state "{label}" as {state_name}_subflow_node')
            lines.append(f'    {state_name} --> {state_name}_subflow_node')
            
            completion_target = '[*]' if on_completion.startswith('(exit flow)') else on_completion
            cancel_target = '[*]' if on_cancel.startswith('(exit flow)') else on_cancel

            lines.append(f'    {state_name}_subflow_node --> {completion_target} : ✅ onCompletion')
            lines.append(f'    {state_name}_subflow_node --> {cancel_target} : 🛑 onCancel')

    return lines

def generate_mermaid_from_flow(flow_data: dict, all_flows_data: list, view_map: dict) -> str:
    """Generates Mermaid state diagram syntax from a single flow definition."""
    
    if not flow_data:
        return "# Flow data is empty."

    lines = ["stateDiagram-v2"]
    initial_state = flow_data.get('initialState')
    states = flow_data.get('states', [])
    flow_id = flow_data.get('flowId')

    if initial_state:
        lines.append(f'    [*] --> {initial_state}')
    
    state_lines = generate_mermaid_for_states(states, flow_id, view_map)
    lines.extend(state_lines)
            
    return "\n".join(lines)

def main():
    """Main function to parse arguments and run the generator."""
    parser = argparse.ArgumentParser(
        description="Generate Mermaid state diagram code from a ui_flows_spec.yaml file."
    )
    parser.add_argument("spec_file", type=Path, help="Path to the ui_flows_spec.yaml file.")
    parser.add_argument(
        "flow_id", 
        nargs='?', 
        default=None, 
        help="Optional: The flowId to generate a diagram for. If omitted, all flows will be processed and saved to a file."
    )
    
    args = parser.parse_args()

    if not args.spec_file.is_file():
        print(f"Error: File not found at '{args.spec_file}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.spec_file, 'r') as f:
            all_flows = [flow for flow in yaml.safe_load_all(f) if flow]
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}", file=sys.stderr)
        sys.exit(1)

    # --- NEW: Pre-build the view map for efficiency ---
    view_map = build_view_map(all_flows)

    if args.flow_id:
        target_flow = next((flow for flow in all_flows if flow.get('flowId') == args.flow_id), None)
        
        if not target_flow:
            print(f"Error: flowId '{args.flow_id}' not found in the spec file.", file=sys.stderr)
            sys.exit(1)
            
        mermaid_code = generate_mermaid_from_flow(target_flow, all_flows, view_map)
        print("```mermaid")
        print(mermaid_code)
        print("```")
    else:
        output_path = Path("docs/ui_flow_diagrams.md")
        markdown_content = [
            "# UI Flow Diagrams\n\n",
            "> **Note:** This document is auto-generated by `util/generate_ui_flow_visuals_mermaid.py`. Do not edit it manually.\n"
        ]

        for flow in all_flows:
            flow_id = flow.get('flowId', 'Unknown Flow')
            markdown_content.append(f"## Flow: `{flow_id}`\n")
            mermaid_code = generate_mermaid_from_flow(flow, all_flows, view_map)
            markdown_content.append("```mermaid")
            markdown_content.append(mermaid_code)
            markdown_content.append("```\n")

        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w') as f:
            f.write("\n".join(markdown_content))
        
        print(f"✅ Successfully generated diagrams for all flows in '{output_path}'")

if __name__ == "__main__":
    main()
    
    