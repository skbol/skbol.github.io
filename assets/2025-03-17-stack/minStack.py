class MinStack:
    def __init__(self):
        self.dataStack = []
        self.minStack = []

    def push(self, val: int) -> None:
        self.dataStack.append(val)
        if(not self.minStack or val <= self.minStack[-1]):
            self.minStack.append(val)

    def pop(self) -> None:
        if self.minStack[-1] == self.dataStack[-1]:
            self.minStack.pop()
        self.dataStack.pop()
        

    def top(self) -> int:
        return self.dataStack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()