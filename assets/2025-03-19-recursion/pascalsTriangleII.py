import time

class Solution:
    def getRow(self, rowIndex):
        # we know that for a pascal's triangle , at row n(zero-indexed) , we will have n+1 columns
        if(rowIndex == 0):
            return [1]
        row = []
        
        # we know that the zeroth element is always 1
        row.append(1)
        
        for colIndex in range(1,rowIndex):
            x = self.valAtIndex(rowIndex , colIndex)
            row.append(x)
            
        # we know that the last element is always 1
        row.append(1)
            
        return row
        
    def valAtIndex(self , rowIndex , colIndex):
        
        #Base case
        if(colIndex == 0 or colIndex == rowIndex):
            return 1
        
        #Reccurance realtion
        # f(i,j) = f(i-1,j-1)+f(i-1,j)
        return self.valAtIndex(rowIndex-1,colIndex-1)+self.valAtIndex(rowIndex-1,colIndex)

sol= Solution()
start = time.time()
x = int(input())
res = sol.getRow(x)
end = time.time()

print(res)
print(f"Time taken : {(end-start) * 1000}")