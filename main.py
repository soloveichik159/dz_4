import yaml
import math


OP_LOAD_CONST = 120
OP_LOAD_MEM   = 129
OP_STORE_MEM  = 123
OP_SQRT       = 53


def encode_load_const(A, B, C):
    instr_value = (A & 0xFF) | ((B & ((1 << 27) - 1)) << 8) | ((C & ((1 << 7) - 1)) << 35)
    return instr_value.to_bytes(6, byteorder='little')


def encode_load_mem(A, B, C):
    instr_value = (A & 0xFF) | ((B & ((1 << 26) - 1)) << 8) | ((C & ((1 << 7) - 1)) << 34)
    return instr_value.to_bytes(6, byteorder='little')


def encode_store_mem(A, B, C):
    instr_value = (A & 0xFF) | ((B & ((1 << 7) - 1)) << 8) | ((C & ((1 << 26) - 1)) << 15)
    return instr_value.to_bytes(6, byteorder='little')


def encode_unary_sqrt(A, B, C):
    instr_value = (A & 0xFF) | ((B & ((1 << 7) - 1)) << 8) | ((C & ((1 << 7) - 1)) << 15)
    return instr_value.to_bytes(3, byteorder='little')


def decode_load_const(instr_bytes):
    instr_value = int.from_bytes(instr_bytes, 'little')
    A = instr_value & 0xFF
    B = (instr_value >> 8) & ((1 << 27) - 1)
    C = (instr_value >> 35) & ((1 << 7) - 1)
    return A, B, C


def decode_load_mem(instr_bytes):
    instr_value = int.from_bytes(instr_bytes, 'little')
    A = instr_value & 0xFF
    B = (instr_value >> 8) & ((1 << 26) - 1)
    C = (instr_value >> 34) & ((1 << 7) - 1)
    return A, B, C


def decode_store_mem(instr_bytes):
    instr_value = int.from_bytes(instr_bytes, 'little')
    A = instr_value & 0xFF
    B = (instr_value >> 8) & ((1 << 7) - 1)
    C = (instr_value >> 15) & ((1 << 26) - 1)
    return A, B, C


def decode_unary_sqrt(instr_bytes):
    instr_value = int.from_bytes(instr_bytes, 'little')
    A = instr_value & 0xFF
    B = (instr_value >> 8) & ((1 << 7) - 1)
    C = (instr_value >> 15) & ((1 << 7) - 1)
    return A, B, C


def assemble_line(line):
    tokens = line.strip().split()
    if not tokens:
        return None, None

    op = tokens[0].upper()

    if op == "LOAD_CONST":
        A = OP_LOAD_CONST
        val_str = tokens[1].rstrip(',')
        val = int(val_str)
        reg_str = tokens[2]
        C = int(reg_str[1:])
        instr = encode_load_const(A, val, C)
        return op, instr

    elif op == "LOAD_MEM":
        A = OP_LOAD_MEM
        val_str = tokens[1].rstrip(',')
        B = int(val_str)
        reg_str = tokens[2]
        C = int(reg_str[1:])
        instr = encode_load_mem(A, B, C)
        return op, instr

    elif op == "STORE_MEM":
        A = OP_STORE_MEM
        reg_str = tokens[1].rstrip(',')
        B = int(reg_str[1:])
        addr_str = tokens[2]
        C = int(addr_str)
        instr = encode_store_mem(A, B, C)
        return op, instr

    elif op == "SQRT":
        A = OP_SQRT
        out_reg_str = tokens[1].rstrip(',')
        B = int(out_reg_str[1:])
        in_reg_str = tokens[2]
        C = int(in_reg_str[1:])
        instr = encode_unary_sqrt(A, B, C)
        return op, instr

    else:
        raise ValueError(f"Неизвестная команда: {op}")

def assemble(input_path, output_path, log_path):
    instructions = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                op, instr_bytes = assemble_line(line)
                if instr_bytes is not None:
                    instructions.append((op, instr_bytes))

    with open(output_path, 'wb') as f:
        for _, instr in instructions:
            f.write(instr)

    log_data = []
    for op, instr in instructions:
        arr = list(instr)
        log_entry = {
            'opcode': op,
            'bytes': [f"0x{b:02X}" for b in arr]
        }
        log_data.append(log_entry)

    with open(log_path, 'w') as f:
        yaml.dump(log_data, f, sort_keys=False, allow_unicode=True)

class UVM:
    def __init__(self, memory_size=2048, num_regs=256):
        self.memory = [0]*memory_size
        self.regs = [0]*num_regs
        self.pc = 0
        self.code = b''

    def load_code(self, code):
        self.code = code
        self.pc = 0

    def step(self):
        if self.pc >= len(self.code):
            return False
        A = self.code[self.pc]
        if A == OP_LOAD_CONST:
            instr = self.code[self.pc:self.pc+6]
            A, B, C = decode_load_const(instr)
            self.regs[C] = B
            self.pc += 6
        elif A == OP_LOAD_MEM:
            instr = self.code[self.pc:self.pc+6]
            A, B, C = decode_load_mem(instr)
            self.regs[C] = self.memory[B]
            self.pc += 6
        elif A == OP_STORE_MEM:
            instr = self.code[self.pc:self.pc+6]
            A, B, C = decode_store_mem(instr)
            self.memory[C] = self.regs[B]
            self.pc += 6
        elif A == OP_SQRT:
            instr = self.code[self.pc:self.pc+3]
            A, B, C = decode_unary_sqrt(instr)
            val = self.regs[C]
            self.regs[B] = int(math.sqrt(val))
            self.pc += 3
        else:
            raise RuntimeError(f"Неизвестный opcode {A}")
        return True

    def run(self):
        while self.step():
            pass

def interpret(code_path, mem_start, mem_end, result_path):
    with open(code_path, 'rb') as f:
        code = f.read()

    vm = UVM()
    vm.load_code(code)
    vm.run()

    result_data = {
        'memory_dump': {
            'start': mem_start,
            'end': mem_end,
            'data': vm.regs[mem_start:mem_end+1]
        }
    }

    with open(result_path, 'w') as f:
        yaml.dump(result_data, f, sort_keys=False, allow_unicode=True)


def main():
    assemble('input.asm', 'output.bin', 'log.yaml')
    interpret('output.bin', 0, 30, 'result.yaml')


if __name__ == "__main__":
    main()
