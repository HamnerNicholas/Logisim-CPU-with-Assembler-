import sys
import shlex
filename = sys.argv[1]

address_width = 16

equivalents = {"r0" : 0, "r1" : 1, "r2" : 2, "r3" : 3, "r4" : 4, "r5" : 5, "r6" : 6, "r7" : 7, "0" : 0, "1" : 1, "2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "R0" : 0, "R1" : 1, "R2" : 2, "R3" : 3, "R4" : 4, "R5" : 5, "R6" : 6, "R7" : 7}
labels = {}


SRF_OP = 0 
ALUI_OP = 1
ALU_OP = 2
IO_OP = 3
COPY_OP = 4
BRANCH_OP = 5
LOAD_OP = 6
STORE_OP = 7

# one argument = "instruction"
OP_STYLE = "op"
# two argument = "intruction" , "reg" OR "instruction" , "imm"
OP_REG_STYLE = "opreg"
OP_IMM_STYLE = "opimm"
# three argument = "instruction", "reg", "imm"
OP_REG_IMM_STYLE = "opregimm"

srf_subops = {
    "jsr": (0b00, 2, OP_IMM_STYLE, 0b000),
    "rsr": (0b01, 1, OP_STYLE, 0b000), 
    "ssrf": (0b10, 2, OP_REG_STYLE, 0b000),
    "rsrf": (0b11, 2, OP_REG_STYLE, 0b000)
}
alui_subops = { 
    "addi": (0b00, 3, OP_REG_IMM_STYLE, 0b001),
    "subi": (0b01, 3, OP_REG_IMM_STYLE, 0b001),
    "divi": (0b10, 3, OP_REG_IMM_STYLE, 0b001),
    "divri": (0b11, 3, OP_REG_IMM_STYLE, 0b001)
}
alu_subops = {
    "add": (0b00, 2, OP_REG_STYLE, 0b010),
    "sub": (0b01, 2, OP_REG_STYLE, 0b010),
    "div": (0b10, 2, OP_REG_STYLE, 0b010),
    "divr": (0b11, 2, OP_REG_STYLE, 0b010)
}
io_subops = {
    "tty": (0b00, 1, OP_STYLE, 0b011),
    "ttya": (0b01, 1, OP_STYLE, 0b011),
    "halt": (0b10, 1, OP_STYLE, 0b11)
}
copy_subops = {
    "copy": (0b00, 2, OP_REG_STYLE, 0b100)
}
branch_subops = {
    "beq": (0b00, 3, OP_REG_IMM_STYLE, 0b101),
    "bne": (0b01, 3, OP_REG_IMM_STYLE, 0b101),
    "blt": (0b10, 3, OP_REG_IMM_STYLE, 0b101),
    "jump": (0b11, 2, OP_IMM_STYLE, 0b101),
}
load_subops = {
    "load": (0b00, 3, OP_REG_IMM_STYLE, 0b110)
}
store_subops = {
    "store": (0b00, 3, OP_REG_IMM_STYLE, 0b111)
}

directive_ops = { # stores how many arguments each expects
    ".org": 2, 
    ".word": 2,
    ".define": 3,
    ".text": 1,
    ".data": 1
}

instruction_set = srf_subops | alui_subops | alu_subops | io_subops | copy_subops | branch_subops | load_subops | store_subops

def parse_fields(line):
    lexer = shlex.shlex(line, posix=True)
    lexer.commenters = ";"
    lexer.whitespace_split = True
    fields = list(lexer)
    op = fields[0]
    if not fields or fields[0] in [":", ".define", ".data", ".text", ".org", ".word"]:
        return fields # Return raw fields for directives/labels
    
    if op in directive_ops:
        return op, None, None, fields
    op = fields[0]
    # Default to None if indices don't exist to avoid IndexErrors
    reg = fields[1] if len(fields) > 1 else None
    imm = fields[2] if len(fields) > 2 else (fields[1] if len(fields) > 1 else None)
    
    return op, reg, imm, fields

def validate_instruction(field_length, op, reg, imm, line_number):
      #validate op is valid instruction
      if(op not in instruction_set) and (op not in directive_ops):
           raise Exception(f"'{op}' not a valid instruction on line number {line_number}")
      
      subop, valid_length, style, op_code = instruction_set[op]
      if op in io_subops:
        # tty allows raw string operand
        return

      # validate it has the right ammount of arguments for the instruction
      if(field_length != valid_length):
          if(style == OP_IMM_STYLE) and (field_length == 1):
              raise Exception(f"Missing immediate field for '{op}' on line {line_number}")
          elif(style == OP_REG_STYLE) and (field_length == 1):
              raise Exception(f"Missing register field for '{op}' on line {line_number}")
          elif(style == OP_REG_IMM_STYLE) and (field_length == 2):
              raise Exception(f"Missing register or immediate field for '{op}' on line {line_number}")              
          else:
              raise Exception(f"Total fields out of range for {op} on line {line_number}")
      
      if style in (OP_REG_STYLE, OP_REG_IMM_STYLE):
        if reg not in equivalents:
            raise Exception(f"Register field '{reg}' for instruction '{op}' is not valid on line {line_number}")
        
        reg_value = equivalents[reg]
        if reg_value < 0 or reg_value > 7:
            raise Exception(f"Register index {reg_value} out of range on line {line_number}")

    # Validate imm field ONLY if the style expects one
      if style in (OP_IMM_STYLE, OP_REG_IMM_STYLE):
        if imm is None:
             raise Exception(f"Immediate required for '{op}' on line {line_number}")
             
        try:
            val = int(imm, 0)
        except ValueError:
            if imm in equivalents:
                val = equivalents[imm]
            elif imm in labels:
                val = labels[imm][1] # Get address from (mode, addr)
            else:
                raise Exception(f"Undefined label or constant '{imm}' on line {line_number}")

        if not (-128 <= val <= 255):
            raise Exception(f"Immediate value {val} (from '{imm}') out of range on line {line_number}")
        
def directive_validation(line, line_num):
    # validate assembler directives
    lexer = shlex.shlex(line, posix=True)
    lexer.commenters = ";"
    lexer.whitespace_split = True
    fields = list(lexer)
    op = fields[0]
    if(op in directive_ops):
        if(len(fields) != directive_ops[op]):
            raise Exception(f"Missing arguments for {op} at line {line_num}")

def convertReg(reg):
    if reg in equivalents:
        return int(equivalents[reg])
    else:
        return int(reg,0)

try:
    with open(filename, 'r') as file, open("machineCode2.txt", "w") as out_file, open("globalMem.txt", "w") as ram_file:
       lines = file.readlines()
       print("v2.0 raw")
       out_file.write("v2.0 raw\n")
       ram_file.write("v2.0 raw\n")
       text_addr = 0
       data_addr = 0
       mode = "text"

        #first pass
       for line in lines:
          lexer = shlex.shlex(line, posix=True)
          lexer.commenters = ";"  # Set semicolon as the comment character
          lexer.whitespace_split = True
          fields = list(lexer)
          if not fields: continue

          op = fields[0]
          if op == ":":
               if mode == "text":
                    labels[fields[1]] = ("text" ,text_addr) # add label to dictionary with the current address as its value
               else:
                    labels[fields[1]] = ("data" ,data_addr) # add label to dictionary with the current address as its value
          elif op == "tty" and len(fields) >= 2:
               text_addr += len(fields[1])
          elif op == ".define": # .define constant 8
               try:
                    equivalents[fields[1]] = int(fields[2], 0)
               except ValueError:
                    raise Exception(f"Invalid value for .define at line")
          elif op == ".data":
               mode = "data"
          elif op == ".word" and mode == "data":
               data_addr += 1
          elif op == ".text":
               mode = "text"
          elif op == ".org":
               target_addr = int(fields[1], 0)
               if mode == "text":
                    if target_addr > text_addr:
                         text_addr = target_addr
                    elif target_addr < text_addr:
                         raise Exception(".org cannot move backwards in text")

               elif mode == "data":
                    if target_addr > data_addr:
                         data_addr = target_addr
                    elif target_addr < data_addr:
                         raise Exception(".org cannot move backwards in data")
          elif op in instruction_set:
               text_addr += 1
        
       text_addr = 0
       data_addr = 0
       #second pass
       for line_num, line in enumerate(lines, start=1):  
        lexer = shlex.shlex(line, posix=True)
        lexer.commenters = ";"  # Set semicolon as the comment character
        lexer.whitespace_split = True
        fields = list(lexer)
        if not fields: continue

        op = fields[0]

        if op == ":":
            continue

        if op in directive_ops:
            directive_validation(line, line_num)
            op = fields[0]
            if op == ".org":
                print("ORG")
                try:
                    if fields[1] in equivalents:
                        target_addr = equivalents[fields[1]]
                    else:
                        target_addr = int(fields[1], 0)
                except ValueError:
                        raise Exception(f"Invalid address for .org expression at line number {line_num}")

                if mode == "text":
                    if target_addr < text_addr:
                        raise Exception(f".org address {target_addr} is behind current text address at line {line_num}")

                    while text_addr < target_addr:
                        print("0000", end=' ')
                        out_file.write("0000 ")
                        text_addr += 1

                elif mode == "data":
                    if target_addr < data_addr:
                        raise Exception(f".org address {target_addr} is behind current data address at line {line_num}")

                    while data_addr < target_addr:
                        ram_file.write("00 ")
                        data_addr += 1

                continue
            elif op == ".define":
                continue
            elif op == ".data":
                mode = "data"
                continue
            elif op == ".text":
                mode = "text"
                continue
            elif op == ".word":
               if mode != "data":
                    raise Exception(".word used outside of .data section")
               token = fields[1]

               if len(token) == 1 and token.isprintable() and not token.isdigit():
                    value = ord(token)
               elif token in labels:
                    section, addr = labels[token]
                    value = addr
               elif token in equivalents:
                    value = equivalents[token]
               else:
                    value = int(token, 0)
               ram_file.write(format(value & 0xFF, '02x') + " ")
               data_addr += 1
            continue 

        op_str, reg_str, imm_str, fields = parse_fields(line)
        validate_instruction(len(fields), op_str, reg_str, imm_str, line_num)
        subop_num = instruction_set[op_str][0]
        family_op = instruction_set[op_str][3]


        reg_num = equivalents[reg_str] if reg_str in equivalents else 0
        if(family_op == IO_OP) and (subop_num == io_subops["tty"][0]):
            imm = fields[1]
            for char in imm:
                if(char == '"'):
                    continue
                else:
                    imm_num = ord(char)
                    reg_num = 0
                    subop_num = 0
                    machine_code = (
                        (imm_num << 8) |
                        (subop_num << 6) |
                        (reg_num << 3) |
                        family_op
                    )
                    print(format(machine_code, '04x'), end=' ')
                    out_file.write(format(machine_code, '04x') + " ")
                    text_addr += 1
        elif((family_op == IO_OP) and (subop_num == io_subops["ttya"][0])):
            imm_num = 0b10000000
            reg_num = 0
            subop_num = 0
            machine_code = (
                (imm_num << 8) |
                (subop_num << 6) |
                (reg_num << 3) |
                family_op
            )
            print(format(machine_code, '04x'), end=' ')
            out_file.write(format(machine_code, '04x') + " ")
            text_addr += 1
        else:        
            if imm_str is None:
                imm_num = 0
            elif imm_str in equivalents:
                imm_num = equivalents[imm_str]
            elif imm_str in labels:
                section, target = labels[imm_str]

                if family_op == BRANCH_OP or family_op == SRF_OP:
                    imm_num = target - text_addr
                else:
                    imm_num = target 
                    
            else:
                imm_num = int(imm_str, 0)

            imm_num = imm_num & 0xFF
            machine_code = (
                (imm_num << 8) |
                (subop_num << 6) |
                (reg_num << 3) |
                family_op
            )

            print(format(machine_code, '04x'), end=' ')
            if(mode == "text"):
                out_file.write(format(machine_code, '04x') + " ")
            else:
                ram_file.write(format(machine_code, '04x') + " ")
            text_addr += 1
except FileNotFoundError:
   print("Code file not found.")
except Exception as e:
    print(f"\nASSEMBLER ERROR: {e}")
    sys.exit(1)