import math

class heap:
    '''
    Implementing heap as a complete binary tree
    Internally we can use a array to represent a binary tree
    '''
    def __init__(self, cmp):
        self.data = []
        self.cmp = cmp

    def __leftChild(self , i):
        return ((2*i)+1)
    
    def __rightChild(self, i):
        return ((2*i)+2)
    
    def __parent(self,i):
        return (i-1)//2

    def __siftUp(self , index):
        parentIndex = self.__parent(index)
        while(index > 0 and self.cmp(self.data[index], self.data[parentIndex])): #min heap
            self.data[index] , self.data[parentIndex] = self.data[parentIndex] , self.data[index]
            index = parentIndex
            parentIndex = self.__parent(index)

    def __siftdown(self, index):
        size = len(self.data)
        while True:
            leftChildIndex = self.__leftChild(index)
            rightChildIndex = self.__rightChild(index)
            best = index  # Assume current index is smallest

            if leftChildIndex < size and self.cmp(self.data[leftChildIndex] , self.data[best]):
                best = leftChildIndex

            if rightChildIndex < size and self.cmp(self.data[rightChildIndex], self.data[best]):
                best = rightChildIndex

            if best == index:  # If no swap needed, break
                break

            self.data[index], self.data[best] = self.data[best], self.data[index]
            index = best  # Move down to the swapped child


    def makeHeap(self , l):
        for value in l:
            self.offer(value=value)
    
    def heapify(self, l):
        pass
        ''' Implement this -->
          heapify method builds the heap from bottom up
          Time complexity of heapify is O(n) compared to O(nlogn) for makeHeap'''

    def offer(self,value):
        #when an element is offered , append it to list and sift up until heap invariant is maintained
        self.data.append(value)
        self.__siftUp(len(self.data)-1)

    def poll(self):
        #when we poll a heap , swap the root with the last leaf node and pop it
        #then, sift down the root node to satisfly heap invariant
        if not self.data:
            return None  # Heap is empty

        self.data[0] , self.data[-1] = self.data[-1] , self.data[0]
        popped_value = self.data.pop()
        if self.data: #If heap is not empty , then sift down
            self.__siftdown(0)
        return popped_value

    def display(self):

        if self.data == []:
            print("Tree is empty")
        else:
            # print(*self.data)
            height = math.floor(math.log2(len(self.data))) + 1
            max_width = 2**(height - 1)
            index = 0
            for level in range(height):
                nodes_in_level = 2**level
                space = max_width // nodes_in_level
                row = []
                for _ in range(nodes_in_level):
                    if index < len(self.data):
                        row.append(f"{self.data[index]:^3}")  # Center align
                        index += 1
                    else:
                        break
                print(" " * (space // 2) + (" " * space).join(row))
            print("-"*20)
            print("\n")


# Comparator functions
min_heap_cmp = lambda child, parent: child < parent  # Min-Heap (default behavior)
max_heap_cmp = lambda child, parent: child > parent  # Max-Heap

heap = heap(max_heap_cmp)
heap.makeHeap([1,7,2,3,8,3])
heap.display()
heap.offer(3)
heap.offer(5)
heap.display()
heap.offer(1)
heap.offer(7)
heap.display()
print(heap.poll())
heap.display()