import re

# This is what I think a token needs to know

class Token:
  def __init__(self, regex, name):
    self.regex = regex
    self.name = name

  def __str__(self):
    return self.name

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
  def __init__(self, regex, name, func, precedence):
    super().__init__(regex, name)
    self.func = func
    self.precedence = precedence

  def __eq__(self, other):
    return self.precedence == other.precedence

  def __lt__(self, other):
    return self.precedence < other.precedence
  
  def __gt__(self, other):
    return self.precedence > other.precedence
  
  def do_func(self, args):
    return self.func(*args)
  
  def get_precedence(self):
    return self.precedence

# Brackets need to know what they match

class Bracket(Token):
  def __init__(self, regex, name):
    super().__init__(regex, name)
    self.match = None
  
  def set_match(self, match):
    self.match = match
  
  def matches(self, target):
    return target.name == self.match.name

class LeftBracket(Bracket):
  pass

class RightBracket(Bracket):
  pass

# Let's start with round brackets

round_left = LeftBracket('^\(', 'left bracket')
round_right = RightBracket('^\)', 'right bracket')      

round_right.set_match(round_left)
round_left.set_match(round_right)

# So now let's define a few tokens

tokens = [
      Operand('^[0-9]+', 'int', int),
      Operator('^\*', '*', lambda x,y:x*y, 2),
      Operator('^\+', '+', lambda x,y:x+y, 1),
      Operator('^\-', '-', lambda x,y:x-y, 1),
      Operator('^\/', '/', lambda x,y:x/y, 2),
      round_left,
      round_right,
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

# We need somewhere to park our operators

op_stack = []

# And somewhere to output the result

out_stack = []

# Work through our tokenized string

for t, v in token_list:

# Use whitespace only as a separator

  if t.name == 'space':
    continue

# Operands (numbers) are output as they arrive

  if type(t) is Operand:
    out_stack.append((t, v))

# Left brackets go onto the operator stack as a marker

  elif type(t) is LeftBracket:
    op_stack.append((t, v))

# When we see a right bracket we shunt everything
# upto the matching left bracket onto the output stack

  elif type(t) is RightBracket:

# Keep looking through the operator stack

    still_popping = True
    while still_popping:
      s, u = op_stack.pop()

# Until we find a matching left bracket

      if isinstance(s, LeftBracket) and s.matches(t):
        still_popping = False
      else:

# Pushing operators to the output stack as we go

        out_stack.append((s,u))

# Operators cause all operators on the operator stack
# to jump to the output stack

  elif isinstance(t, Operator):
    still_popping = True

# Only proceed when there is a stack to look at

    while still_popping and op_stack:

# What's on the top?

      s, u = op_stack[-1]

# If it's a higher precedence operator then over it goes

      if isinstance(s, Operator) and s > t:
          out_stack.append(op_stack.pop())
      else:
          still_popping = False

# And our new operator goes to the top of the stack

    op_stack.append((t, v))

# Once the tokens are finished we need to un-shunt the remaining tokens

while op_stack:
  out_stack.append(op_stack.pop())

# This needs to improve

[print(f'{t}\t-\t{v}') for t, v in out_stack]
