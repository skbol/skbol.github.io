class MyCircularQueue:

    def __init__(self, k: int):
        self.data = [None]*k
        self.size = k
        self.head = 0
        self.tail = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():return False
        self.data[self.tail % self.size] = value
        self.tail += 1
        return True
        
    def deQueue(self) -> bool:
        if self.isEmpty(): return False
        self.head += 1
        return True

    def Front(self) -> int:
        if self.isEmpty(): return -1
        return self.data[self.head % self.size]

    def Rear(self) -> int:
        if self.isEmpty(): return -1
        return self.data[(self.tail - 1) % self.size]

    def isEmpty(self) -> bool:
        return self.head == self.tail

    def isFull(self) -> bool:
        return self.tail == self.head+self.size


# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()