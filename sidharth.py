'''
S Type Instructions

s{b|h|w|d} rd, imm[11:0](rt) 
mem(rt + sex(imm[11:0])) = rd

imm[11 : 5] rs2 rs1 010 imm[4 : 0] 0100011 sw
            ra  sp

'''

import csv

def getAdd(inst):
  data={}
  with open("data.csv","r") as obj:
    f=csv.reader(obj)
    for temp in f:
      data[temp[0]]=temp[1]
  return data[inst]

def decimal_to_binary_32bit(num):
  binary = -1
  if 2**31-1>=num >= 0:  # Error Detection Needs Implementation
      binary = bin(num)[2:].zfill(32)
  elif 0>num>=-2**32+1:
      binary = bin(2**32 + num)[2:]
      padding = 32-len(binary)
      binary = '1'*padding + str(binary)
      
  return binary


# S-type

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

# S-type instruction specifically sw since we only have to implement word type.

with open("sidoutput.txt","w") as obj:
  obj.write(S_Type_to_binary("sw ra,32(sp)"))
  
  obj.write("\n0000001 00001 00010 010 00000 0100011")

#0000001 00001 00010 010 00000 0100011
