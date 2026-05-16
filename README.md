# Custom 16-bit CPU and Assembler

This project is a custom 16-bit CPU built in Logisim, along with a Python assembler used to convert assembly programs into machine code for the processor.

The goal of this project was to design a simple working computer architecture from the ground up, including the instruction format, datapath, control logic, memory system, assembler, and basic I/O support.

---

# Overview

The CPU uses a 16-bit instruction format:

```text
[8-bit immediate][2-bit sub-op][3-bit register][3-bit opcode]
```

The processor is accumulator-based and includes a small register file, program counter, instruction memory, data memory, arithmetic logic, branching support, subroutine support, and TTY output.

The Python assembler reads custom assembly code and produces machine code files that can be loaded into the Logisim circuit.

---

# Features

- Custom 16-bit instruction set
- Logisim CPU implementation
- Python two-pass assembler
- Register file with registers `r0` through `r7`
- Accumulator-based arithmetic
- Immediate and register-based ALU instructions
- Branch and jump instructions
- Load and store instructions
- Subroutine support using a return address register
- TTY output for ASCII text
- Separate text and data sections
- Label support
- Constants using `.define`
- Memory layout control using `.org`
- Data initialization using `.word`

---

# Supported Instruction Groups

The assembler and CPU support several instruction families.

## SRF / Subroutine Instructions

```asm
jsr
rsr
ssrf
rsrf
```

## Immediate ALU Instructions

```asm
addi
subi
divi
divri
```

## Register ALU Instructions

```asm
add
sub
div
divr
```

## I/O Instructions

```asm
tty
ttya
halt
```

## Copy Instruction

```asm
copy
```

## Branch Instructions

```asm
beq
bne
blt
jump
```

## Memory Instructions

```asm
load
store
```

---

# Assembler

The assembler is written in Python and performs two passes over the source file.

## First Pass

During the first pass, the assembler:

- Tracks text and data addresses
- Records labels
- Handles `.define` constants
- Processes `.org`, `.text`, `.data`, and `.word` directives

## Second Pass

During the second pass, the assembler:

- Validates instructions and arguments
- Resolves labels and constants
- Encodes instructions into hexadecimal machine code
- Writes instruction memory output to `machineCode2.txt`
- Writes data memory output to `globalMem.txt`

---

# Assembler Directives

The assembler supports the following directives:

```asm
.text
.data
.org <address>
.word <value>
.define <name> <value>
```

---

# Example Assembly Program

```asm
.define newline 10

.text

tty "Hello World"
ttya
halt
```

The assembler converts this program into machine code that can be loaded directly into the Logisim instruction memory.

---

# Logisim CPU Components

The Logisim circuit contains the main hardware components required to run assembled programs, including:

- Program Counter (PC)
- Instruction RAM
- Instruction Decoder
- Register File
- Accumulator
- Arithmetic Logic Unit (ALU)
- Branch Logic
- Data Memory
- Return Address Register (`$ra`)
- TTY Output Device
- Clock and Reset Controls

---

# CPU Architecture Notes

- 16-bit instruction width
- 8-bit immediates
- 8 general-purpose registers
- Accumulator-centered execution model
- Separate instruction and data memory
- Sub-operation field for expanding instruction functionality
- Support for relative branching and subroutines

---

# Purpose

This project was created as a class project to better understand how computers execute instructions at a low level.

It combines:

- Digital logic design
- CPU architecture
- Instruction encoding
- Assembly language design
- Parsing and lexical analysis
- Memory systems
- Hardware/software integration

The project demonstrates how assembly instructions are translated into machine code and executed by custom digital hardware.

---

# Tools Used

- Python
- Logisim
- Custom Assembly Language

---

# Output Files

Running the assembler generates:

```text
machineCode2.txt
globalMem.txt
```

These files contain Logisim-compatible hexadecimal memory data and can be loaded into the CPU’s instruction and data memory components.

---

# Future Improvements

Potential future improvements include:

- Additional ALU operations
- Stack support
- Interrupt handling
- Better debugging tools
- Expanded instruction set
- Pipeline support
- Improved memory management
- Higher-level language support

---

# Author
Nicholas Hamner
---
Created as part of a computer architecture and digital systems design project.
