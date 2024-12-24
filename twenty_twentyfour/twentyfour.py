import re
from itertools import permutations
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
    previous_unresolved_count = -1
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

        if previous_unresolved_count == len(next_round):
            return None

        previous_unresolved_count = len(next_round)
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

from itertools import combinations
import re

def generate_pair_of_pairs(outputs):
    for quad in combinations(outputs, 4):
        a, b, c, d = quad
        yield ((a, b), (c, d))
        yield ((a, c), (b, d))
        yield ((a, d), (b, c))

def find_swaps_brute(initial_values, gates, predicate):
    """
    Identify the swaps needed to fix the system.
    """
    outputs = [line.split("->")[-1].strip() for line in gates]
    swaps = []
    cntr = 0
    for pair1, pair2 in generate_pair_of_pairs(outputs):
        cntr += 1      
        swapped_gates = gates[:]
        current_swapped_pairs = list(pair1) + list(pair2)
        for i in range(0, len(current_swapped_pairs), 2):
            a, b = current_swapped_pairs[i], current_swapped_pairs[i + 1]
            swapped_gates = [
                line.replace(f"-> {a}", f"-> TEMP")
                    .replace(f"-> {b}", f"-> {a}")
                    .replace(f"-> TEMP", f"-> {b}")
                for line in swapped_gates
            ]

        if predicate(initial_values, swapped_gates):
            result = list()
            result.extend(current_swapped_pairs)
            for g in swapped_gates:
                for sg in current_swapped_pairs:
                    if sg in g:
                        match = re.match(r"(\w+)\s+(AND|OR|XOR)\s+(\w+)\s+->\s+(\w+)", g)
                        input1, op, input2, output = match.groups()
                        result.append(input1)
                        result.append(input2)
            print(cntr)
            return ','.join(sorted(result))            
    
    return sorted(swaps)

def gate_output(wire_values, prefix):
    z_values = {k: v for k, v in wire_values.items() if k.startswith(prefix)}
    sorted_bits = [z_values[key] for key in reversed(sorted(z_values.keys(), key=lambda x: int(x[1:])))]
    binary_string = ''.join(map(str, sorted_bits))
    return int(binary_string,2)

def test_addition_system(initial_values, gates):
    wire_values = simulate_circuit(initial_values, gates)
    if wire_values is None:
        return False
    
    x_value = gate_output(wire_values, 'x')
    y_value = gate_output(wire_values, 'y')
    z_value = gate_output(wire_values, 'z')
    expected_sum = x_value + y_value
    return z_value == expected_sum

def gates_to_mermaid(gates):
    """
    Convert a list of gate definitions like:
       ["x00 AND y00 -> z00", "x01 XOR y01 -> z01", ...]
    into a Mermaid flowchart diagram.

    Returns a string containing Mermaid syntax.

    Example flowchart snippet:
        flowchart LR
            x00 --> G1[AND]
            y00 --> G1
            G1 --> z00
            x01 --> G2[XOR]
            y01 --> G2
            G2 --> z01
    """
    lines = []
    lines.append("flowchart TB")

    for i, gate_str in enumerate(gates, start=1):
        match = re.match(r"(\w+)\s+(AND|OR|XOR)\s+(\w+)\s+->\s+(\w+)", gate_str)
        if match:
            lhs1, op, lhs2, out_wire = match.groups()
            gate_label = f"G{i}"
            gate_node = f"{gate_label}[{op}]"
            lines.append(f"    {lhs1} --> {gate_node}")
            lines.append(f"    {lhs2} --> {gate_node}")
            lines.append(f"    {gate_node} --> {out_wire}")

    return "\n".join(lines)