from itertools import product
from operator import mul, add
from os import PathLike
from typing import Dict, Callable, List, Tuple

def generate_and_evaluate(numbers: List[int], operators: Dict[str, Callable[[int, int], int]]):
    if len(numbers) < 2:
        raise ValueError("At least two numbers are required.")
    
    for combination in product(operators.keys(), repeat=len(numbers) - 1):
        result = numbers[0]
        for i, operator in enumerate(combination):
            result = operators[operator](result, numbers[i+1])
        
        yield result

def get_calibrations(filepath: PathLike) -> List[Tuple[int,List[int]]]:
    calibrations = list()
    with open(filepath) as f:
        for line in f:
            total, inputs = line.split(':')
            inputs = [int(input) for input in inputs.strip().split(' ')]
            calibrations.append((int(total), inputs))
    return calibrations

def sum_valid_calibrations(calibrations: List[Tuple[int,List[int]]], operators: Dict[str, Callable[[int, int], int]] = None):
    result = 0
    if operators is None:
        operators = {'*': mul, '+': add}
    for total, inputs in calibrations:
        for actual in generate_and_evaluate(inputs, operators):
            if total == actual:
                result += actual
                break
    return result

def concat(a: int, b: int) -> int:
    return int(str(abs(a)) + str(abs(b)))

def get_elephant_operators():
    return {'*': mul, '+': add, '||': concat}