import csv

def getAdd(inst):
  data={}
  with open("data.csv","r") as obj:
    f=csv.reader(obj)
    for temp in f:
      data[temp[0]]=temp[1]
  return data[inst.strip()]


def decimal_to_binary_16bit(num):
  if num >= 0:
      binary = bin(num)[2:].zfill(16)
  else:
      binary = bin(2**16 + num)[2:]
  return binary

# B-type 

def BType_to_binary(line1,inst):
  inst.strip()

  data={"opcode":"1100011",}
  line2=line1.replace(","," ")
  line=line2.split(" ")
  global st
  st=""
  imm1=((decimal_to_binary_16bit(int(line[3])))[11:16])
  imm2=((decimal_to_binary_16bit(int(line[3])))[4:11])
  
  part1=imm2+getAdd(line[2])+getAdd(line[1])
  part2=imm1+data["opcode"]
  match inst:
    case "beq":
      st=part1+"000"+part2
      return st
    case "bne":
      st=part1+"001"+part2
      return st
    case "blt":
      st=part1+"100"+part2
      return st
    case "bge":
      st=part1+"101"+part2
      return st
    case "bltu":
      st=part1+"110"+part2
      return st
    case "bgeu":
      st=part1+"111"+part2
      return st


#I type instruction 
def IType_to_binary(line1,inst):
  inst.strip()

  
  line2=line1.replace(","," ").replace("("," ").replace(")","")
  line=line2.split(" ")
  
  if inst=="lw":
    imm=((decimal_to_binary_16bit(int(line[2])))[4:])
    st= imm+getAdd(line[3])+"010"+getAdd(line[1])+"0000011"
    return st

  imm=((decimal_to_binary_16bit(int(line[3])))[4:])
  match inst:
    
    case "addi":
      st=imm+getAdd(line[2])+"000"+getAdd(line[1])+"0010011"
      return st
    case "sltiu":
      st=imm+getAdd(line[2])+"011"+getAdd(line[1])+"0010011"
      return st
    case "jalr":
      st=imm+getAdd(line[2])+"000"+getAdd(line[1])+"1100111"
      return st
