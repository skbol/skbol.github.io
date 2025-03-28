import time
class Solution:
    def __init__(self):
        self.memcache = {} #Create a hashmap to implement memoization
        
    def fib(self, n: int) -> int:
        #Base case
        if(n==0):
            return 0
        if(n==1):
            return 1
        
        #Reccurance
        if(n-1 in self.memcache):
            n1 = self.memcache[n-1]
        else:
            self.memcache[n-1] = self.fib(n-1)
            n1 = self.memcache[n-1]
        
        if(n-2 in self.memcache):
            n2 = self.memcache[n-2]
        else:
            self.memcache[n-2] = self.fib(n-2)
            n2 = self.memcache[n-2]
        
        return n1+n2
        # return self.fib(n-1)+ self.fib(n-2)
        
sol = Solution()
start = time.time()
n = int(input("Enter you input : "))
print(sol.fib(n))
end = time.time()
print(f"Ran in {(end-start) * 1000} ms")