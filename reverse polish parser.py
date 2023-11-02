import re

# This is what I think a token needs to know

class Token:
  def __init__(self, regex, name):
    self.regex = regex
    self.name = name
  
  def get_regex(self):
    return self.regex

# Operands know what type they are

class Operand(Token):
  def __init__(self, regex, name, op_type):
    super().__init__(regex, name)
    self.op_type = op_type
  
  def recast(self, str_val):
    return self.op_type(str_val)

# Operators need to know what they can do

class Operator(Token):
  def __init__(self, regex, name, func):
    super().__init__(regex, name)
    self.func = func
  
  def do_func(self, args):
    return self.func(*args)

# So now let's define a few tokens

tokens = [
      Operand('^[0-9]+', 'int', int),
      Operator('^\*', '*', lambda x,y:x*y),
      Operator('^\+', '+', lambda x,y:x+y),
      Operator('^\-', '-', lambda x,y:x-y),
      Operator('^\/', '/', lambda x,y:x/y),
      Token('^\ +', 'space')
      ]

# This isn't very elegant

expression = input(f'Do you want to play a game? ')

print(expression)

# This should be a lexical analyser method on some expression class

token_list = []

scanning = True

while scanning and expression:
  token = None
  
  for t in tokens:
    check = re.search(t.get_regex(), expression)

    if check:
      value = check.group()
      start, finish = check.span()
      token = t
      break

  if check:
    token_list.append((token, value))
    expression = expression[finish: ]
  
    print(f'{type(token)}\t{token.name}\t-\t{value}')
  
  else:
    print(f'Not sure what to do with {expression}')
    scanning = False

# Now do the calculation - this should really be a syntax analysis to a parse tree
# And there should be a separate semantic analysis
# I guess the conclusion is that this isn't a compiler

calc_stack = []

for t, v in token_list:
  if t.name == 'space':
    continue
  if isinstance(t, Operand):
    print(f'Operand {t}')
    calc_stack.append(t.recast(v))
  if isinstance(t, Operator):
    print(f'Operator {t}')
    b = calc_stack.pop()
    a = calc_stack.pop()
    calc_stack.append(t.do_func((a,b)))
  print(calc_stack)
