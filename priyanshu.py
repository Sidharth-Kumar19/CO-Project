import csv
def getAdd(inst):
  data={}
  with open("data.csv","r") as obj:
    f=csv.reader(obj)
    for temp in f:
      data[temp[0]]=temp[1]
  return data[inst.strip().lower()]
def decimal_to_binary_20bit(num):
  if num >= 0:
      binary = bin(num)[2:].zfill(20)
  else:
      binary = bin(2**20 + num)[2:]
  return binary
def JType_to_binary(line):
  temp=line.split(',')
  line=temp[0].split()+temp[1:]
  imm=decimal_to_binary_20bit(int(line[2]))
  st=imm[0]+imm[-11:-1:1]+imm[-11]+imm[-12:-20:-1]+getAdd(line[1])+"1101111"
  return st
def RType_to_binary(line1,inst):
  inst.strip()
  data={"opcode1":"0110011","funct1":"0000000","funct2":"0100000",}
  line2=line1.split(',')
  l2=line2[0].split()
  line=l2+line2[1:]
  st=""
  part1=getAdd(line[3])+getAdd(line[2])
  part2=getAdd(line[1])+data["opcode1"]
  match inst:
    case "add":
      st=data["funct1"]+part1+"000"+part2
      return st
    case "sub":
      st=data["funct2"]+part1+"000"+part2
      return st
    case "sll":
      st=data["funct1"]+part1+"001"+part2
      return st;
    case "slt":
      st=data["funct1"]+part1+"010"+part2
      return st
    case "sltu":
      st=data["funct1"]+part1+"011"+part2
      return st
    case "xor":
      st=data["funct1"]+part1+"100"+part2
      return st
    case "srl":
      st=data["funct1"]+part1+"101"+part2
      return st
    case "or":
      st=data["funct1"]+part1+"110"+part2
      return st
    case "and":
      st=data["funct1"]+part1+"111"+part2
      return st
