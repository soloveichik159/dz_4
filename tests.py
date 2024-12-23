import unittest
import math
from main import (encode_load_const, decode_load_const,
                 encode_load_mem, decode_load_mem,
                 encode_store_mem, decode_store_mem,
                 encode_unary_sqrt, decode_unary_sqrt,
                 UVM, OP_LOAD_CONST, OP_LOAD_MEM, OP_STORE_MEM, OP_SQRT)

class TestInstructionEncoding(unittest.TestCase):
    def test_load_const(self):
        A, B, C = 120, 234, 84
        enc = encode_load_const(A, B, C)
        A2, B2, C2 = decode_load_const(enc)
        self.assertEqual(A, A2)
        self.assertEqual(B, B2)
        self.assertEqual(C, C2)

    def test_load_mem(self):
        A, B, C = 129, 667, 50
        enc = encode_load_mem(A, B, C)
        A2, B2, C2 = decode_load_mem(enc)
        self.assertEqual(A, A2)
        self.assertEqual(B, B2)
        self.assertEqual(C, C2)

    def test_store_mem(self):
        A, B, C = 123, 109, 633
        enc = encode_store_mem(A, B, C)
        A2, B2, C2 = decode_store_mem(enc)
        self.assertEqual(A, A2)
        self.assertEqual(B, B2)
        self.assertEqual(C, C2)

    def test_sqrt(self):
        A, B, C = 53, 113, 71
        enc = encode_unary_sqrt(A, B, C)
        A2, B2, C2 = decode_unary_sqrt(enc)
        self.assertEqual(A, A2)
        self.assertEqual(B, B2)
        self.assertEqual(C, C2)

class TestUVMInterpreter(unittest.TestCase):
    def test_run_load_const(self):
        vm = UVM()
        enc = encode_load_const(OP_LOAD_CONST, 234, 84)
        vm.load_code(enc)
        vm.run()
        self.assertEqual(vm.regs[84], 234)

    def test_run_load_mem(self):
        vm = UVM()
        vm.memory[667] = 999
        enc = encode_load_mem(OP_LOAD_MEM, 667, 50)
        vm.load_code(enc)
        vm.run()
        self.assertEqual(vm.regs[50], 999)

    def test_run_store_mem(self):
        vm = UVM()
        vm.regs[109] = 777
        enc = encode_store_mem(OP_STORE_MEM, 109, 633)
        vm.load_code(enc)
        vm.run()
        self.assertEqual(vm.memory[633], 777)

    def test_run_sqrt(self):
        vm = UVM()
        vm.regs[71] = 144
        enc = encode_unary_sqrt(OP_SQRT, 113, 71)
        vm.load_code(enc)
        vm.run()
        self.assertEqual(vm.regs[113], 12)

    def test_run_program(self):
        vm = UVM()
        instrs = []
        instrs.append(encode_load_const(OP_LOAD_CONST, 16, 10))
        instrs.append(encode_unary_sqrt(OP_SQRT, 20, 10))
        instrs.append(encode_store_mem(OP_STORE_MEM, 20, 500))
        code = b''.join(instrs)
        vm.load_code(code)
        vm.run()
        self.assertEqual(vm.regs[20], 4)
        self.assertEqual(vm.memory[500], 4)

if __name__ == '__main__':
    unittest.main()
