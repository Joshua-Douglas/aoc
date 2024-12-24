import re

MUL_COMMAND_PATTERN = re.compile(r"(?i)mul\((\d{1,3}),(\d{1,3})\)")

def extract_mul_command_input(input_string):
    matches = MUL_COMMAND_PATTERN.findall(input_string)
    return [(int(num1), int(num2)) for num1, num2 in matches]

def decorrupt_memory(memory_filepath):
    memory_str = ''
    with open(memory_filepath) as f:
        memory_str = f.read()

    return sum((a*b for (a,b) in extract_mul_command_input(memory_str)))

def decorrupt_do_memory(memory_filepath):
    '''
    Conditionally enable and disable the mul() commands using the
    don't() and do() commands. The memory_str begins enabled and 
    each encountered don't() command will disable until the next
    do() command.

    Return the sum of all found mul() commands.

    e.g. xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    xmul(2,4)&mul[3,7]!^ -> Enabled
    _mul(5,5)+mul(32,64](mul(11,8)un -> Disabled
    ?mul(8,5)) -> Enabled
    '''
    memory_str = ''
    with open(memory_filepath) as f:
        memory_str = f.read()

    result = 0
    for idx, potential_do in enumerate(memory_str.split("don't()")):
        # handle case where multiple do()s are between a single don't()
        potential_cmds = potential_do.split("do()")
        # First command starts enabled. Remaining will start disabled
        if idx != 0: del potential_cmds[0]
        for do_cmd in potential_cmds:
            result += sum((a*b for (a,b) in extract_mul_command_input(do_cmd)))
    return result