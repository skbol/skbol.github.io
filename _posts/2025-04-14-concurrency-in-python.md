---
layout: post
title: "Concurrency in Python"
subtitle: How concurrency can be achieved in Python | A deep dive
tags: [Python, Concurrency]
---

[Difference between difference concurrency related modules](https://stackoverflow.com/questions/61351844/difference-between-multiprocessing-asyncio-threading-and-concurrency-futures-i)        

Let's go through the major concurrency-related modules provided by the standard library:

- threading: interface to OS-level threads. Note that CPU-bound work is mostly serialized by the GIL, so don't expect threading to speed up calculations. Use it when you need to invoke blocking APIs in parallel, and when you require precise control over thread creation. Avoid creating too many threads (e.g. thousands), as they are not free. If possible, don't create threads yourself, use concurrent.futures instead.

- multiprocessing: interface to spawning python processes with an API intentionally mimicking that of threading. Processes work in parallel unaffected by the GIL, so you can use multiprocessing to utilize multiple cores and speed up calculations. The disadvantage is that you can't share in-memory data structures without using multiprocessing-specific tools.

- concurrent.futures: A modern interface to threading and multiprocessing, which provides convenient thread/process pools it calls executors. The pool's main entry point is the submit method which returns a handle that you can test for completion or wait for its result. Getting the result gives you the return value of the submitted function and correctly propagates raised exceptions (if any), which would be tedious to do with threading. concurrent.futures should be the tool of choice when considering thread or process based parallelism.

- asyncio: While the previous options are "async" in the sense that they provide non-blocking APIs (this is what methods like apply_async refer to), they are still relying on thread/process pools to do their magic, and cannot really do more things in parallel than they have workers in the pool. Asyncio is different: it uses a single thread of execution and async system calls across the board. It has no blocking calls at all, the only blocking part being the asyncio.run() entry point. Asyncio code is typically written using coroutines, which use await to suspend until something interesting happens. (Suspending is different than blocking in that it allows the event loop thread to continue to other things while you're waiting.) It has many advantages compared to thread-based solutions, such as being able to spawn thousands of cheap "tasks" without bogging down the system, and being able to cancel tasks or easily wait for multiple things at once. Asyncio should be the tool of choice for servers and for clients connecting to multiple servers.

> When choosing between asyncio and multithreading/multiprocessing, consider the adage that "threading is for working in parallel, and async is for waiting in parallel".

> Also note that asyncio can await functions executed in thread or process pools provided by concurrent.futures, so it can serve as glue between all those different models. This is part of the reason why asyncio is often used to build new library infrastructure.      


[Learn about GIL](https://youtu.be/XVcRQ6T9RHo?si=Wp17FsVonCO5jwec)         
[Threading vs MultiProcessing](https://youtu.be/AZnGRKFUU0c?si=NHJFu86sxDnbj8zf)
[Threading in Python](https://www.youtube.com/watch?v=IEEhzQoKtQU)
[MultiProcessing in Python](https://youtu.be/fKl2JW_qrso?si=if8OBdO1tv_yYzx6)


# If Python's GIL doesnot let more than 1 thread to access the interpreter , why does Threading module work ??

# GIL and Threading in Python

**User:** Srikanth Bolla (skhbolla@gmail.com)  
**Created:** 4/14/2025 23:24  
**Updated:** 4/14/2025 23:37  
**Exported:** 4/14/2025 23:54  

## Prompt:
Hey , in python the GIL doesnot let more than 1 thread at a time to access the interpreter right ? then how does the threading module work ?

## Response:
Hey! You're absolutely right — the GIL (Global Interpreter Lock) in CPython does restrict only **one thread at a time** from executing Python **bytecode**. So the natural question is, _how does the `threading` module even help then?_ Great question. Let’s break it down:

* * *

### 🧠 What the GIL Does

*   CPython (the standard Python interpreter) has a **GIL**, which ensures that only one thread executes **Python bytecode** at a time.
    
*   It’s there to protect memory management and internal state of Python objects from race conditions.
    

* * *

### 🤔 Then Why Use `threading`?

The `threading` module **still has real OS-level threads**, but their **Python-level execution is serialized** due to the GIL. Still, threading **can** be useful in certain scenarios:

#### ✅ When threading _is_ useful:

1.  **I/O-bound tasks** – like:
    
    *   Waiting for file reads/writes
        
    *   Downloading from the internet
        
    *   Talking to a database or socket
        
    
    ➤ While one thread is waiting on I/O, the GIL is released and **another thread can run**.
    

#### ❌ When threading _is not_ useful:

2.  **CPU-bound tasks** – like:
    
    *   Image processing
        
    *   Mathematical computations
        
    *   Data crunching
        
    
    ➤ Here, threads fight over the GIL and only one runs at a time → **no true parallelism**.
    

* * *

### 🛠️ How does `threading` module work under the hood?

*   The threads are **native threads** (like `pthread` on Unix or Win32 threads).
    
*   Python **releases the GIL** when doing I/O or using certain C extensions that manage their own threading.
    
*   The interpreter periodically **switches between threads** (~every 5ms) to simulate concurrency.
    

* * *

### 🧪 Example: Threading good for I/O

```python
import threading
import time

def download_file():
    print("Start download")
    time.sleep(2)  # Simulates I/O
    print("Finished download")

threads = []

for _ in range(5):
    t = threading.Thread(target=download_file)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

Even with the GIL, this runs **concurrently**, because `time.sleep()` releases the GIL.

* * *

### 🧠 TL;DR

*   **GIL blocks true multi-core execution for Python code**.
    
*   **`threading` is useful for I/O-bound tasks**, not CPU-bound.
    
*   For CPU-bound tasks, prefer:
    
    *   `multiprocessing` (spawns separate Python processes)
        
    *   Or alternative interpreters (e.g., **Jython**, **IronPython**, or **PyPy STM**)
        

* * *
## Prompt:
how does python know when an IO operation is in progress ? and after it releases GIL , how does it know when the IO is done?

## Response:
That's a **brilliant question**, and you're digging into the core of how Python works under the hood. Let’s break this down in a way that connects everything step-by-step:

* * *

🔍 Part 1: **How does Python know when an I/O operation is in progress?**
-------------------------------------------------------------------------

Let’s look at a simple example:

```python
import time
time.sleep(5)
```

Even though you're not writing "this is an I/O operation", Python knows that `time.sleep()` doesn't need the CPU and it will release the GIL. Why?

### ✅ Because I/O functions in Python are written in **C**, and they explicitly tell Python:

> “Hey, I’m going to block for a while. You can release the GIL now.”

This is done using special C macros like:

```c
Py_BEGIN_ALLOW_THREADS
    // Do blocking operation (like sleep, file read, network)
Py_END_ALLOW_THREADS
```

So in the **C source code** of these functions, Python is told:

*   “I’m about to block on I/O.”
    
*   “You may let other threads use the GIL.”
    
*   “I’ll grab the GIL again when I’m done.”
    

That’s how Python knows it can safely pause this thread and let others run.

* * *

🔁 Part 2: **How does Python know when the I/O is done and it's time to reacquire the GIL?**
--------------------------------------------------------------------------------------------

Python uses the **OS's I/O mechanisms** to wait — like `select`, `poll`, or `epoll` (on Linux) or `IOCP` on Windows.

Let’s continue the story:

1.  Python thread calls a C function (like reading from a file or socket).
    
2.  That function does something blocking like:
    

```c
read(file_descriptor, buffer, length)
```

3.  It tells Python: “I’m waiting for this to finish, let go of the GIL.”
    
4.  Python releases the GIL, and lets other threads run.
    
5.  When the OS says “hey, I/O is done!” (file read completed or socket got data), the thread wakes up.
    
6.  Then the C function says: “Okay, I’m back. I’ll take the GIL again now.”
    

And it continues the Python code after that.

* * *

📦 Example: `requests.get()` — Network I/O
------------------------------------------

This function internally uses a C library (`urllib3`, `socket`, etc.), which makes system calls to the OS. These functions also:

*   Tell Python they're doing a blocking call.
    
*   Python releases the GIL.
    
*   Other threads are allowed to run.
    
*   Once data is received or a timeout occurs, the GIL is reacquired and execution resumes.
    

* * *

⚙️ So, to summarize:
--------------------

| Step | What Happens |
| --- | --- |
| 1 | Python thread enters a function like `read()` or `sleep()` |
| 2 | That function is written in C and uses `Py_BEGIN_ALLOW_THREADS` |
| 3 | Python releases the GIL so other threads can run |
| 4 | The OS blocks that thread until I/O completes |
| 5 | When done, Python reacquires the GIL and continues execution in that thread |

* * *

💡 Bonus: Can you write your own I/O function that releases the GIL?
--------------------------------------------------------------------

Not directly in Python — you'd need to write a **C extension** to Python, or use **Cython**, where you can manually control GIL behavior.

* * *

Would you like to see how this works in the C code of something like `time.sleep()` or `socket.recv()`? I can show that too!

## Prompt:
When the OS says “hey, I/O is done!” (file read completed or socket got data), the thread wakes up.

Then the C function says: “Okay, I’m back. I’ll take the GIL again now.”


How is this done ?

## Response:
Awesome follow-up — now you're getting into the **deep internals of Python + OS interaction**. So let's walk through **how the OS tells the thread "I'm done!"**, and how Python **knows to reacquire the GIL** after that.

* * *

🧠 First, let's simplify the question:
--------------------------------------

### ❓How does the blocked thread (doing I/O) wake up and get back the GIL?

It happens in 2 parts:

1.  **The thread is blocked in a system call (like `read`, `recv`, etc.).**
    
2.  **When the system call finishes, the thread wakes up and resumes.**
    
3.  **It then reacquires the GIL before returning control to Python code.**
    

* * *

🏗️ What does this look like under the hood?
--------------------------------------------

Let's say you're doing:

```python
response = requests.get("https://example.com")
```

Internally, here's what really happens:

### 1\. Python calls into a C function (from the `socket` library or OpenSSL)

### 2\. Inside the C function:

It wraps the blocking I/O code like this:

```c
Py_BEGIN_ALLOW_THREADS
    result = read(fd, buf, count);  // This blocks at the OS level
Py_END_ALLOW_THREADS
```

These macros expand to something like:

```c
PyThreadState *_save;
_save = PyEval_SaveThread();  // Releases the GIL

/* do blocking call here, like read() */
result = read(fd, buf, count);

PyEval_RestoreThread(_save); // Reacquires the GIL
```

* * *

💡 What’s happening here exactly?
---------------------------------

### 🔸 `PyEval_SaveThread()`:

*   Tells Python: "I'm done running Python bytecode for now."
    
*   Releases the GIL.
    
*   Stores the thread's state in `_save`.
    

### 🔸 Then, the thread **enters a system call** like `read()`, `recv()`, or `select()`:

*   This is a **kernel syscall** that blocks.
    
*   The OS **puts this thread to sleep**.
    
*   The thread **does not consume CPU** while sleeping.
    

### 🔸 When I/O completes:

*   The **OS wakes up the thread**.
    
    *   For sockets: The TCP stack says “we received the data!”
        
    *   For files: The disk driver says “read complete!”
        

### 🔸 `PyEval_RestoreThread(_save)`:

*   The thread **reacquires the GIL**.
    
*   Restores Python’s internal state.
    
*   Returns back to Python code.
    

* * *

🖼️ Visual Flow:
----------------

```
Thread: calls blocking I/O function
        ↓
GIL: released (via PyEval_SaveThread)
        ↓
OS: blocks thread in read()
        ↓
I/O completes (e.g., network packet arrives)
        ↓
OS: wakes up thread
        ↓
Thread: reacquires GIL (via PyEval_RestoreThread)
        ↓
Returns to Python land
```

* * *

🛠️ What role does the OS play?
-------------------------------

*   The OS uses **syscalls** like `read`, `recv`, `select`, etc., which block the thread until data is ready.
    
*   It uses kernel-level event queues, like:
    
    *   `select()` or `poll()` (classic)
        
    *   `epoll` (Linux), `kqueue` (BSD), IOCP (Windows)
        

Python doesn’t need to manage that itself — it relies on the OS.

* * *

✅ Summary
---------

*   Python's I/O functions are written in C.
    
*   These functions manually release the GIL before blocking.
    
*   When the OS says “I/O is done,” it wakes up the thread.
    
*   The thread then reacquires the GIL before continuing Python execution.
    

* * *

If you want, I can show the actual C code for `time.sleep` or `socket.recv` from CPython’s GitHub, or even build a tiny extension in C or Cython that demonstrates this behavior. Would that help make it more real?



---


