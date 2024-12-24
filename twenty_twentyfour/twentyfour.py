import re
from collections import defaultdict

def parse_input(input_data):
    initial_values = {}
    gates = []
    for line in input_data.splitlines():
        if ":" in line:
            wire, value = line.split(": ")
            initial_values[wire] = int(value)
        elif "->" in line:
            gates.append(line)
    return initial_values, gates

def evaluate_gate(op, a, b):
    """
    Evaluate a logic gate operation.
    """
    if op == "AND":
        return a & b
    elif op == "OR":
        return a | b
    elif op == "XOR":
        return a ^ b
    raise ValueError(f"Unknown operation: {op}")

def simulate_circuit(initial_values, gates):
    wire_values = defaultdict(lambda: None)
    wire_values.update(initial_values)

    unresolved_gates = gates[:]
    while unresolved_gates:
        next_round = []
        for gate in unresolved_gates:
            match = re.match(r"(\w+)\s+(AND|OR|XOR)\s+(\w+)\s+->\s+(\w+)", gate)
            if match:
                input1, op, input2, output = match.groups()
                # Check if inputs have values
                if wire_values[input1] is not None and wire_values[input2] is not None:
                    wire_values[output] = evaluate_gate(op, wire_values[input1], wire_values[input2])
                else:
                    next_round.append(gate)
        unresolved_gates = next_round

    return wire_values

def z_gate_output(wire_values):
    z_values = {k: v for k, v in wire_values.items() if k.startswith('z')}
    sorted_bits = [z_values[key] for key in reversed(sorted(z_values.keys(), key=lambda x: int(x[1:])))]
    binary_string = ''.join(map(str, sorted_bits))
    return int(binary_string, 2)

def compute_number(input_data):
    initial_values, gates = parse_input(input_data)
    wire_values = simulate_circuit(initial_values, gates)
    return z_gate_output(wire_values)