
import csv
def getAdd(inst):
  data={}
  with open("data.csv","r") as obj:
    f=csv.reader(obj)
    for temp in f:
      data[temp[0]]=temp[1]
  return data[inst.strip()]

def decimal_to_binary_32bit(num):
  if num>=0:
      binary = bin(num)[2:].zfill(32)
  else:
      binary = bin(2**32+num)[2:]
  return binary

#U-type
import re
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


#auipc s2,-30
#11111111111111111111100100010111
#11111111111111111111100100010111


