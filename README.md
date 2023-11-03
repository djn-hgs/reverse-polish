# Reverse Polish Notation and parsing arithmetic

## RPN calculator

The first program is a simple **RPN** calculator. The process runs as follows:
- Describe the form of numbers and operators using **regex**
- Tokenize the statement into numbers and operators using regex matching
- Describe a stack that will hold the RPN numbers and operators
- Work through the tokenized code and either push terms onto stack or evaluate

 ## Infix Arithmetic Calculator

 I'm not sure whether this one is finished, but it implements Dijkstra's classic **Shunting Yard Algorithm**, which requires two stacks in order to be able evaluate and to managae precedence or brackets.
