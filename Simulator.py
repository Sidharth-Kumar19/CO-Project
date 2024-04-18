# Generate dictionary
import sys

reg_data = {}
mem_data = {}
addresses = [
    '0x00010000', '0x00010004', '0x00010008', '0x0001000c', '0x00010010',
    '0x00010014', '0x00010018', '0x0001001c', '0x00010020', '0x00010024',
    '0x00010028', '0x0001002c', '0x00010030', '0x00010034', '0x00010038',
    '0x0001003c', '0x00010040', '0x00010044', '0x00010048', '0x0001004c',
    '0x00010050', '0x00010054', "0x00010058", "0x0001005c", "0x00010060",
    "0x00010064", "0x00010068", "0x0001006c", "0x00010070", "0x00010074",
    "0x00010078", "0x0001007c"
]


def generate_data():
  global reg_data
  global mem_data

  for i in range(32):
    binary_key = format(i, '05b')
    reg_data[binary_key] = '0' * 32

  for i in addresses:
    mem_data[i] = '0' * 32


def getData(s):
  return reg_data[s]


def output(st, output_file):
  global reg_data
  global mem_data
  with open(output_file, "a") as obj:
    binary_list = [
        '00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111',
        '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111',
        '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111',
        '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111'
    ]
    obj.write("0b" + st + " ")
    for i in binary_list:
      obj.write("0b" + getData(i) + " ")
    obj.write("\n")


def detectType(inst):
  #print("Detection Executed")
  opcode = inst[25:]
  if (opcode == '0110011'):
    return 'R'
  elif (opcode == '0000011' or opcode == '0010011' or opcode == '1100111'):
    return 'I'
  elif (opcode == '0100011'):
    return 'S'
  elif (opcode == '1100011'):
    return 'B'
  elif (opcode == '0110111' or opcode == '0010111'):
    return 'U'
  elif (opcode == '1101111'):
    return 'J'


def sign_extension_string(binary, desired_length=32):
  if len(binary) >= desired_length:
    return binary
  else:
    sign_bit = binary[0]
    extension = sign_bit * (desired_length - len(binary))
    return extension + binary


def sign_extension_bin(binary, desired_length=32):
  if len(binary) >= desired_length:
    return int(binary, 2)  #Error throw karna hai
  else:
    sign_bit = binary[0]
    extension = sign_bit * (desired_length - len(binary))
    return int(extension + binary, 2)


# R-Type
#1
def R_Type_Add(rs1, rs2):
  return (bin(
      int(sign_extension_string(rs1, 32), 2) +
      int(sign_extension_string(rs2, 32), 2))[2:].zfill(32))[-32::1]


#2,3
def signed_subtraction(rs1, rs2):
  rs1 = int(rs1, 2)
  rs2 = int(rs2, 2)
  rs1_signed = rs1 if rs1 < 0x80000000 else rs1 - 0x100000000
  rs2_signed = rs2 if rs2 < 0x80000000 else rs2 - 0x100000000
  rd = rs1_signed - rs2_signed
  rd &= 0xFFFFFFFF
  return str(bin(int(rd))[2:].zfill(32))


#6
def binary_xor(bin1, bin2):
  bin1 = bin1.zfill(32)
  bin2 = bin2.zfill(32)
  result = ''
  for i in range(32):
    if bin1[i] == bin2[i]:
      result += '0'
    else:
      result += '1'
  return result


#7
def sll(rs1, rs2):
  shift = int(rs2[27:], 2)
  rs1 = int(rs1, 2)
  result = rs1 << shift
  return (bin(result))[2:].zfill(32)[-32::1]


#8
def srl(rs1, rs2):
  shift = int(rs2[27:], 2)
  rs1 = int(rs1, 2)
  result = rs1 >> shift
  return (bin(result))[2:].zfill(32)[-32::1]


#9
def bitwise_or(num1, num2):
  num1 = int(num1, 2)
  num2 = int(num2, 2)
  result = num1 | num2
  return (bin(result)[2:]).zfill(32)


#10
def bitwise_and(num1, num2):
  num1 = int(num1, 2)
  num2 = int(num2, 2)
  result = num1 & num2
  return (bin(result)[2:]).zfill(32)


def update_reg(d, reg):
  if (reg == '00000'):
    pass
  else:
    reg_data[reg] = d


#R Type
def RType(inst):
  funct7 = inst[0:7]
  addressrs2 = inst[7:12]
  addressrs1 = inst[12:17]
  rs1 = reg_data[addressrs1]
  rs2 = reg_data[addressrs2]
  funct3 = inst[17:20]
  rd = inst[20:25]
  if (funct3 == '000' and funct7 == '0000000'):  #add
    ans = R_Type_Add(rs1, rs2)
    update_reg(ans, rd)
  elif (funct3 == '000' and funct7 == '0100000'):  #sub
    ans = signed_subtraction(rs1, rs2)  # check for case 2 and 3
    update_reg(ans, rd)
  elif (funct3 == '010' and funct7 == '0000000'):  #slt
    if sign_extension_bin(rs1, 32) < sign_extension_bin(rs2, 32):
      ans = ("0" * 31) + "1"
      update_reg(ans, rd)
  elif (funct3 == '011' and funct7 == '0000000'):  #sltu
    if int(rs1, 2) < int(rs2, 2):
      ans = ("0" * 31) + "1"
      update_reg(ans, rd)
  elif (funct3 == '100' and funct7 == '0000000'):  #xor
    ans = binary_xor(rs1, rs2)
    update_reg(ans, rd)
  elif (funct3 == '001' and funct7 == '0000000'):  #sll
    ans = sll(rs1, rs2)
    update_reg(ans, rd)
  elif (funct3 == '101' and funct7 == '0000000'):  #srl
    ans = srl(rs1, rs2)
    update_reg(ans, rd)
  elif (funct3 == '110' and funct7 == '0000000'):  #or
    ans = bitwise_or(rs1, rs2)
    update_reg(ans, rd)
  elif (funct3 == '111' and funct7 == '0000000'):  #and
    ans = bitwise_and(rs1, rs2)
    update_reg(ans, rd)


# def binary_to_decimal(binary):
#   decimal = 0
#   for bit in binary:
#     decimal = decimal * 2 + int(bit)
#   return decimal

# def decimal_to_hex(decimal):
#   hex_chars = "0123456789ABCDEF"
#   hex_code = ""
#   while decimal > 0:
#     remainder = decimal % 16
#     hex_code = hex_chars[remainder] + hex_code
#     decimal = decimal // 16

#   if len(hex_code) < 2:
#     hex_code = '0' + hex_code
#   return hex_code

# def convert_binary_to_hex(binary):
#   decimal = binary_to_decimal(binary)
#   hex_code = decimal_to_hex(decimal)
#   return hex_code


# S TYPE INSTRUCTION
def mem_out(output_file):
  with open(output_file, "a") as obj:
    for i in addresses:
      obj.write(i + ":0b" + mem_data[i] + "\n")


def SType(inst):
  imm1 = inst[0:7]  #0
  rs2 = inst[7:12]  #21
  rs1 = inst[12:17]  #9
  imm2 = inst[20:25]  #0
  imm = int(str(sign_extension_string(str(imm1 + imm2), 32)), 2)
  rs1 = int(str(sign_extension_string(reg_data[rs1], 32)), 2)
  temp = imm + rs1
  addr = hex((temp))
  addr = addr[0:2] + "000" + addr[2:]
  #print(addr + " " + reg_data[rs2])
  mem_data[addr] = reg_data[rs2]


def add_binary_strings(bin_str1, bin_str2):
  bin_str1 = bin_str1.zfill(32)
  bin_str2 = bin_str2.zfill(32)
  num1 = int(bin_str1, 2)
  num2 = int(bin_str2, 2)
  result = num1 + num2
  result &= 0xFFFFFFFF
  result_str = bin(result)[2:].zfill(32)
  return result_str


def BType(inst, PC):
  imm1 = inst[0]
  imm2 = inst[1:7]
  imm3 = inst[20:24]
  imm4 = inst[24]
  imm = imm1 + imm4 + imm2 + imm3
  rs2 = inst[7:12]
  rs1 = inst[12:17]
  funct3 = inst[17:20]
  opcode = inst[25:]
  if (opcode == '1100011'):
    if (funct3 == '000'):  #beq
      if sext(reg_data[rs1]) == sext(reg_data[rs2]):
        return PC + sext(imm + '0')
    elif (funct3 == '001'):  #bne
      if sext(reg_data[rs1]) != sext(reg_data[rs2]):
        return PC + sext(imm + '0')
    elif (funct3 == '100'):  #blt
      if sext(reg_data[rs1]) < sext(reg_data[rs2]):
        return PC + sext(imm + '10')
    elif (funct3 == '101'):  #bge
      if sext(reg_data[rs1]) >= sext(reg_data[rs2]):
        return PC + sext(imm + '0')
    elif (funct3 == '110'):  #bltu
      if unsigned(reg_data[rs1]) < unsigned(reg_data[rs2]):
        return PC + sext(imm + '0')
    elif (funct3 == '111'):  #bgeu
      if unsigned(reg_data[rs1]) >= unsigned(reg_data[rs2]):
        return PC + sext(imm + '0')
    else:
      return -1

  return program_counter


def IType(inst, pc):
  imm = inst[0:12]
  rs1 = inst[12:17]
  funct3 = inst[17:20]
  rd = inst[20:25]
  opcode = inst[25:]
  if (funct3 == '010' and opcode == '0000011'):  #lw
    #rd = mem(rs1 + sext(imm[11:0]))
    imm = int(sign_extension_string(imm, 32), 2)
    rs1 = int(sign_extension_string(reg_data[rs1], 32), 2)
    temp = imm + rs1
    addr = hex(temp)
    addr = addr[0:2] + "000" + addr[2:]
    reg_data[rd] = mem_data[addr]
  elif (funct3 == '000' and opcode == '0010011'):  #addi
    #rd = rs + sext(imm[11:0])
    #print(imm)
    #print(sign_extension_string(imm, 32))
    reg_data[rd] = add_binary_strings(reg_data[rs1],
                                      sign_extension_string(imm, 32))
  elif (funct3 == '011' and opcode == '0010011'):  #sltiu
    #rd = 1. If unsigned(rs) < unsigned(imm)
    if unsigned(reg_data[rs1]) < unsigned(imm):
      reg_data[rd] = "0" * 31 + "1"
  elif (funct3 == '000' and opcode == '1100111'):  #jalr
    #print("Jalr")
    #print(pc)
    reg_data[rd] = bin(pc)[2:].zfill(32)
    #print(reg_data[rd])
    #print(add_binary_strings(reg_data[rs1], sign_extension_string(imm, 32)))
    pc = int(add_binary_strings(reg_data[rs1], sign_extension_string(imm, 32)),
             2)
    #print(pc)
    pc &= 0xFFFFFFFE

  return pc


def JType(inst, pc):
  imm1 = inst[0]
  imm2 = inst[1:11]
  imm3 = inst[11]
  imm4 = inst[12:20]
  imm = imm1 + imm4 + imm3 + imm2
  rd = inst[20:25]
  opcode = inst[25:]
  if (opcode == '1101111'):  #jal
    #print(pc)
    reg_data[rd] = bin(pc)[2:].zfill(32)
    #print(reg_data[rd])
    pc += sext(imm + '0')
    #print(sext(imm+'0'))
    pc &= 0xFFFFFFFE
    #print(pc)
    return pc
  return pc


def sext(bin_str):
  if bin_str[0] == '1':
    return int(bin_str, 2) - 2**len(bin_str)
  else:
    return int(bin_str, 2)


def unsigned(bin_str):
  return int(bin_str, 2)


def inst(file):
  l = []
  with open(file, "r") as obj:
    for i in obj:
      if (i.isspace()):
        continue
      l.append(i.strip())
  return l


input_file = sys.argv[1]
output_file = sys.argv[2]

program_counter = 0
generate_data()
reg_data["00010"] = "00000000000000000000000100000000"  # Stack Pointer
l = inst(input_file)
if (l[-1]
    != "00000000000000000000000001100011"):  # Ending Virtual Halt detection
  sys.exit()

while (program_counter < len(l) * 4 and program_counter >= 0):
  program_counter += 4
  instruction = l[int((program_counter - 4) / 4)]
  if (instruction == "00000000000000000000000001100011"
      ):  #Virtual Halt in middle
    program_counter -= 4
    output(str(bin(program_counter)[2:]).zfill(32),output_file )
    break
  #print(instruction, program_counter)
  match (detectType(instruction)):
    case "R":
      #print("RType")
      RType(instruction)
    case "S":
      #print("Stype")
      SType(instruction)
    case "B":
      #print("BType")
      program_counter = BType(instruction, program_counter)
    case "I":
      #print("IType")
      program_counter = IType(instruction, program_counter)
    case "J":
      #print("JType")
      program_counter = JType(instruction, program_counter)

  output(str(bin(program_counter)[2:]).zfill(32), output_file)

mem_out(output_file)
