import csv
from priyanshu import RType_to_binary,JType_to_binary
from vansh import BType_to_binary, IType_to_binary
from Umang import UType_to_binary
from sidharth_TypeS import S_Type_to_binary

#Taking input from the file input.txt
def write(st):
  #This function writes your generated 32 bit inst to file..
  with open("Output.txt","a") as obj:
    obj.write(st+"\n")
  
def Input():
  #Coverts input to list Data Type..
  data=[]
  with open("input.txt","r") as obj:
    for i in obj:
      data.append(i)
  return data
def main():
  for i in Input():
    a,b=detectType(i)
    if a=="r":
      st=RType_to_binary(i,b)
      write(st)
    elif a=='j':
      st=JType_to_binary(i)
      write(st)
    elif a=='u':
      st=UType_to_binary(i)
      write(st)
    elif a=='b':
      st=BType_to_binary(i,b)
      write(st)
    elif a=='i':
      st=IType_to_binary(i,b)
      write(st)
    elif a.lower()=='s':
      st=S_Type_to_binary(i)
      write(st)
    else:
      raise ValueError
      
def detectType(st):
  #This detects type and after detection call your function as req..
  r=["add","sub","slt","sltu","sll","xor","srl","or"]
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

main()
