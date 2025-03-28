class Solution:
    def __init__(self):
        self.stack = []
        
    def evalRPN(self, tokens) -> int:
        # Intuition:
        # Push numbers on stack ;
        # When operator is encountered , pop twice , eval and push back result
        # Continue till end , pop finally to get result
        
        for token in tokens:
            if(token.lstrip("-").isdigit()):
                self.stack.append(int(token))
            else:
                n2 = self.stack.pop()
                n1 = self.stack.pop()
                if(token == "+"):
                    self.stack.append(n1+n2)
                if(token == "-"):
                    self.stack.append(n1-n2)
                if(token == "*"):
                    self.stack.append(n1*n2)
                if(token == "/"):
                    self.stack.append(int(n1/n2)) #There's a reason why we use int() instead of floor division (//)
                                                    # This is because , int() truncates decimal part , while // always rounds DOWN.
        return int(float(self.stack.pop()))