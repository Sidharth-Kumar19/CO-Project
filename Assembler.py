import csv
import re
import sys
data={
    'zero': '00000',  
    'r0': '00000',
    'ra': '00001',
    'sp': '00010',
    'gp': '00011',
    'tp': '00100',
    't0': '00101',
    't1': '00110',
    't2': '00111',
    's0': '01000',
    'fp': '01000',
    's1': '01001',
    'a0': '01010',
    'a1': '01011',
    'a2': '01100',
    'a3': '01101',
    'a4': '01110',
    'a5': '01111',
    'a6': '10000',
    'a7': '10001',
    's2': '10010',
    's3': '10011',
    's4': '10100',
    's5': '10101',
    's6': '10110',
    's7': '10111',
    's8': '11000',
    's9': '11001',
    's10': '11010',
    's11': '11011',
    't3': '11100',
    't4': '11101',
    't5': '11110',
    't6': '11111'
}
def getAdd(inst):
  return data[inst.strip().lower()]

def decimal_to_binary_32bit(num):
  if num>=0:
      binary = bin(num)[2:].zfill(32)
  else:
      binary = bin(2**32+num)[2:]
  return binary

def write(st):
  #This function writes your generated 32 bit inst to file..
  with open(sys.argv[2],"a") as obj:
    obj.write(st+"\n")

def isnumber(s):
  return ((s[0]=='-' and s[1:].isdigit()) or (s.isdigit()))

def Input(address):
  #verified
  #Coverts input to list Data Type..
  dat=[]
  pc=0
  with open(address,"r") as obj:
    for i in obj:
      if(i.isspace()):
        continue
      elif ':' in i:
        i=i.split(':')
        i[0]=i[0].strip()
        i[1]=i[1].strip()
        dat.append(i[1])
        global data
        data[i[0]]=pc
      else:
        dat.append(i.strip())
      pc+=1
  return dat

def main():
  input_file=sys.argv[1]
  output_file=sys.argv[2]
  
  global data
  with open(input_file,"r") as obj:
    f=csv.reader(obj)
    for i in f:
      data[i[0]]=i[1]
  obj=open(output_file,"w")
  obj.close()
  pc=0
  for i in Input(input_file):
    a,b=detectType(i)
    if a=="r":
      st=RType_to_binary(i,b)
      write(st)
    elif a=='j':
      st=JType_to_binary(i,pc)
      write(st)
    elif a=='u':
      st=UType_to_binary(i)
      write(st)
    elif a=='b':
      st=BType_to_binary(i,b,pc)
      write(st)
    elif a=='i':
      st=IType_to_binary(i,b)
      write(st)
    elif a.lower()=='s':
      st=S_Type_to_binary(i)
      write(st)
    else:
      raise ValueError
    pc+=1

def detectType(st):
  #This detects type and after detection call your function as req..
  r=["add","sub","slt","sltu","sll","xor","srl","or","and"]
  b=["beq","bne","blt","bge","bltu","bgeu"]
  u=["lui","auipc"]
  i=['lw','addi','sltiu','jalr']
  st=st.split()[0]
  if(st in r):
    return ("r",st)
  elif(st in b):
    return ("b",st)
  elif (st in u):
    return ("u",st)
  elif(st=="jal"):
    return ("j",st)
  elif (st in i):
    return ("i",st)
  elif (st=="sw"):
    return ('s',st)
  else:
    raise ValueError


def decimal_to_binary_20bit(num):
  if num >= 0:
      binary = bin(num)[2:].zfill(20)
  else:
      binary = bin(2**20 + num)[2:]
  return binary

def JType_to_binary(line,pc):
  temp=line.split(',')
  line=temp[0].split()+temp[1:]
  if isnumber(line[2]):
    imm=decimal_to_binary_20bit(int(line[2]))
  else:
    imm=decimal_to_binary_20bit(pc-int(getAdd(line[2])))

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


def S_Type_to_binary(line1):
  line2=line1.replace(","," ")
  line3 = line2.replace("("," ")
  line4 = line3.replace(")"," ")
  line=line4.split(" ")
  
  imm = str(decimal_to_binary_32bit(int(line[2])))
  imm1 = imm[20:27]
  imm2 = imm[27:]
  rs2 = getAdd(line[1])
  rs1 = getAdd(line[3])
  
  
  converted = imm1 + rs2  + rs1 + "010" + imm2 +"0100011"
  # imm1 = decimal_to_binary_12bit(int(line))
  return converted

def UType_to_binary(line1):
  data={"opcode1":"0010111","opcode2":"0110111"}
  line=re.split(r'\s|,',line1)
  inst=line[0]
  st=part1=part2=""
  part1=decimal_to_binary_32bit(int(line[2]))[-32:-12:1]+getAdd(line[1])
  match inst:
    case "auipc":
      part2=data["opcode1"]
    case "lui":
      part2=data["opcode2"]
  st=part1+part2
  return st


def decimal_to_binary_16bit(num):
  if num >= 0:
      binary = bin(num)[2:].zfill(16)
  else:
      binary = bin(2**16 + num)[2:]
  return binary


def BType_to_binary(line1,inst,pc):
  inst.strip()
  data={"opcode":"1100011",}
  line2=line1.replace(","," ")
  line=line2.split(" ")
  global st
  st=""
  if (isnumber(line[3])):
    imm = decimal_to_binary_16bit(int(line[3]))
  else:
    imm = decimal_to_binary_16bit(pc-int(getAdd(line[3])))
  imm1=imm[11:16]
  imm2=imm[4:11]
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
main()
