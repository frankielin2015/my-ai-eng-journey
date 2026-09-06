import asyncio

from contextlib import contextmanager

# async def fetch_data(param):
#     print(f"Fetching data for {param}...")
#     await asyncio.sleep(param)  # Simulate an I/O operation
#     print(f"Data for {param} fetched.")
#     return f"Data for {param}"

# async def main():
#     task2 = asyncio.create_task(fetch_data(2))
#     task1 = asyncio.create_task(fetch_data(1))
#     result2 = await task2  # Wait for task2 to complete
#     print("Task 2 finished")
#     result1 = await task1  # Wait for task1 to complete
#     print("Task 1 finished")
#     return [result1, result2]

# results = asyncio.run(main())
# print("Results:", results)


@contextmanager
def foo():
    try:
        print("2. __enter__: setup runs (before yield)")
        yield "hello"
        print("4.a. __exit__: cleanup runs (after yield)")
    finally:
        print("5. __exit__: cleanup runs (after yield)")

print("---")
print("1. foo() called: creates the CM object (nothing prints yet)")
result = foo()  # just creates, doesn't execute the generator yet
print("   ^ see? nothing from foo() above")
print("---")
with result as f:
    
    print(f"3. f = {f!r} (the yielded value)")
    raise Exception("oops")  # raise an exception to see how __exit__ handles it
    print("4. with BODY runs (generator frozen at yield)")

