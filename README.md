# Logisim-CPU-with-Assembler-
Course project for CPE 142, Advanced Computer Organization. 


# Custom 16-bit CPU and Assembler

This project is a custom 16-bit CPU built in Logisim, along with a Python assembler used to convert assembly programs into machine code for the processor.

The goal of this project was to design a simple working computer architecture from the ground up, including the instruction format, datapath, control logic, memory system, assembler, and basic I/O support.

## Overview

The CPU uses a 16-bit instruction format:

```text
[8-bit immediate][2-bit sub-op][3-bit register][3-bit opcode]

The processor is accumulator-based and includes a small register file, program counter, instruction memory, data memory, arithmetic logic, branching support, subroutine support, and TTY output.

The Python assembler reads custom assembly code and produces machine code files that can be loaded into the Logisim circuit.

Features
 - Custom 16-bit instruction set
 - Logisim CPU implementation
 - Python two-pass assembler
 - Register file with registers r0 through r7
 - Accumulator-based arithmetic
 - Immediate and register-based ALU instructions
 - Branch and jump instructions
 - Load and store instructions
 - Subroutine support using a return address register
 - TTY output for ASCII text
 - Separate text and data sections
 - Label support
 - Constants using .define
 - Memory layout control using .org
 - Data initialization using .word
 - Supported Instruction Groups

The assembler and CPU support several instruction families:

SRF / Subroutine instructions
 - jsr
 - rsr
 - ssrf
 - rsrf
Immediate ALU instructions
 - addi
 - subi
 - divi
 - divri
Register ALU instructions
 - add
 - sub
 - div
 - divr
I/O instructions
 - tty
 - ttya
 - halt
Copy instruction
 - copy
Branch instructions
 - beq
 - bne
 - blt
 - jump
Memory instructions
 - load
 - store

Assembler
The assembler is written in Python and performs two passes over the source file.

During the first pass, it:
 - Tracks text and data addresses
 - Records labels
 - Handles .define constants
 - Processes .org, .text, .data, and .word directives
During the second pass, it:
 - Validates instructions and arguments
 - Resolves labels and constants
 - Encodes instructions into hexadecimal machine code
 - Writes instruction memory output to machineCode2.txt
 - Writes data memory output to globalMem.txt

Assembler Directives
The assembler supports:
 - .text
 - .data
 - .org <address>
 - .word <value>
 - .define <name> <value>

Example Assembly
.define newline 10

.text
tty "Hello"
ttya
halt

The assembler converts this program into machine code that can be loaded into the Logisim instruction memory.


Logisim CPU

The Logisim circuit contains the main hardware components required to run the assembled programs, including:
 - Program counter
 - Instruction RAM
 - Instruction decoder
 - Register file
 - Accumulator
 - ALU
 - Branch logic
 - Data memory
 - Return address register
 - TTY output
 - Clock and reset controls

Purpose
This project was created as a class project to better understand how computers execute instructions at a low level. It combines digital logic design with assembler implementation and demonstrates how software instructions are translated into hardware behavior.

Tools Used
 - Python
 - Logisim
 - Custom assembly language

Output Files
Running the assembler produces:
 - machineCode2.txt
 - globalMem.txt

These files contain Logisim-compatible hexadecimal memory data and can be loaded into the CPU’s instruction and data memory components.

