import operator
import re


op = {"+": operator.add, "-": operator.sub, "%": operator.mod, "/": operator.floordiv, "*": operator.mul, "^": operator.pow}

alpha = ["r", "d"]

r_val = [1804289383, 846930886,1681692777,1714636915,1957747793,424238335,719885386,1649760492,596516649,1189641421,1025202362,1350490027,783368690,1102520059,2044897763,1967513926,1365180540,1540383426,304089172,1303455736,35005211,521595368,1804289383]

MAX = 2147483647
MIN = -2147483648

def SRPN():
  loop = True
  global stack 
  stack = []
  global top
  top  = -1
  global comment
  comment = False
  global rnum
  rnum = 0
  regex = re.compile('[^(\-)?0-9]')
  while loop:
    n1 = input()
    if len(n1) > 1 and regex.search(n1) == None:
      # verity it is number
      condition(n1)
    elif len(n1) > 1:
      match = re.search('\d(\s)*\^\=', n1)   # format for ending with "^="
      if match:
        output = match.group(0)
        print(output[0])
        n1 = n1[:-1]  # remove "=" to avoid answer printing
      input_lis = text_processing(n1)
      extra_condition(input_lis)
    else:
      if comment and n1 != "#":
        continue
      else:
        condition(n1)


def condition(text):
  global comment
  global top
  global stack
  global rnum
  if top == 22:
    print("Stack overflow.")
  try:
    stack.append(int(text))
    top += 1
  except ValueError:
    if text == "#":
      if comment == False:
        comment = True
      else:
        comment = False
    elif text == "r":
      stack.append(r_val[rnum])
      rnum += 1
      top += 1
    elif top == -1 and text not in op.keys():
      if text == "=":
        print("Stack empty.")
      elif text == "d":
        print(MIN)
      else:
        print('Unrecognised operator or operand "{}".'. format(text))
    elif top < 1 and text in op.keys():
      print("Stack underflow.")
    elif text in op.keys():
      val = stack.pop(top)
      top -= 1
      try:
        stack[top] = op[text](stack[top], val)     
      except ZeroDivisionError:
        stack.append(0)
        top += 1
        print("Divide by 0.")
      finally:
        if stack[top] > MAX:
          stack[top] = MAX
        elif stack[top] < MIN:
          stack[top] = MIN
    elif text == "=":
      print(stack[top])
    elif text == "d":
      for i in range(top+1):
        print(stack[i])
    elif text == "" or text == " ":
      pass
    else:
      print('Unrecognised operator or operand "{}".'. format(text))

def extra_condition(text_lis):
  """for one line of consecutive input"""
  global comment
  global top
  global stack
  global rnum
  num = []
  operator = []
  for i in range(len(text_lis)):
    if comment and text_lis[i] != "#":
        continue
    if top+1 == 24 and text_lis[i] != "d":
      print("Stack overflow.")
    elif len(operator) == 0 and (top+1+len(num)) == 23 and text_lis[i] != "d":
      print("Stack overflow.")
    try:
      num.append(int(text_lis[i]))
      if len(operator) > 0 and operator[-1] != "-" and operator[-1] != "+":
        num[-2] = op[operator[-1]](num[-2], num[-1])
        operator.remove(operator[-1])
    except ValueError:
      if text_lis[i] == "#":
        if comment == True and text_lis[i-1] == " ":
          comment = False
        elif comment == False and text_lis[i+1] == " ":
          comment = True
        else:
          print('Unrecognised operator or operand "{}".'. format(text_lis[i]))
      elif comment == True:
        continue
      elif text_lis[i] == "r":
        if rnum == 23 or top+1+rnum >= 23:
          rnum += 1
          continue
        num.append(r_val[rnum])
        rnum += 1
      elif top == -1 and text_lis[i] not in op.keys() and len(num) == 0:
        if text_lis[i] == "=":
          print("Stack empty.")
        elif text_lis[i] == "d":
          print(MIN)
        else:
          print('Unrecognised operator or operand "{}".'. format(text_lis[i]))
      elif text_lis[i] in op.keys(): # index of operand as keys
        operator.append(text_lis[i])
      elif text_lis[i] == "=":
        if len(num) == 0:
          print(stack[-1])
        elif text_lis[i-1].isdigit():
          print(text_lis[i-1])
        elif text_lis[i-1] == " ":
          operator, result = extra_computation(num, operator)
          num = [result]
          print(num[0])
      elif text_lis[i] == "d":
        if text_lis[i-1] in op.keys():
          operator = operator[:-1]
        for i in range(top+1):
          print(stack[i])
        if len(operator) > 0:
          operator, result = extra_computation(num, operator)
          num = [result]
        for j in range(len(num)):
          print(num[j])
      elif text_lis[i] == " ":
        pass
      else:
        print('Unrecognised operator or operand "{}".'. format(text_lis[i]))
  if len(operator) > 0:
    operator, result = extra_computation(num, operator)
    num = [result]

  if len(num) > 0:
    stack.extend(num)
    top += len(num)


def extra_computation(num_lis, op_lis):
  result = 0
  add_count = op_lis.count("+")
  while add_count > 0:
    ind = op_lis.index("+")
    num_lis[ind] = op["+"](num_lis[ind], num_lis[ind+1])
    num_lis = num_lis[:ind+1] + num_lis[ind+2:]
    op_lis.remove("+")
    add_count -= 1
  sub_count = len(op_lis)
  if "-" in op_lis:
    for i in range(sub_count):
      result += op["-"](num_lis[i], num_lis[i+1])
      op_lis.remove("-")
  else:
    result = num_lis[0]
  if result > MAX:
    result = MAX
  elif result < MIN:
    result = MIN
  return op_lis, result



def text_processing(text):
  """parse the text"""
  str_lis = []
  temp = ""
  for j in range(len(text)):
    try:
      int(text[j])
      temp += text[j]
    except ValueError:
      if text[j-1].isdigit():
        str_lis.append(temp)
      str_lis.append(text[j])
      temp = ""
  return str_lis


if __name__ == "__main__":
  SRPN()
  