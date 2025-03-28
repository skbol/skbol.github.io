import time
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if(n > 0):
            return self.__pow(x,n)
        elif(n == 0):
            return 1
        else:
            return 1/(self.__pow(x,n*(-1)))
    def __pow(self , x , n):
        #Base case
        if(n == 0):
            return 1
        
        #Reccurance
        return x*self.__pow(x , n-1)
    
sol = Solution()
start = time.time()
x = float(input("Enter you number : "))
n = int(input("Enter you power : "))
print(sol.myPow(x,n))
end = time.time()
print(f"Ran in {(end-start) * 1000} ms")