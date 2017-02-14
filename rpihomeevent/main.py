import asyncio
import time
import datetime



def hello_world(loop):
    print('Hello World ' + str(datetime.datetime.now().time()))
    loop.call_later(1, hello_world, loop)

def good_evening(loop):
    print('Good Evening ' + str(datetime.datetime.now().time()))
    loop.call_later(1, good_evening, loop)

@asyncio.coroutine
def hello_world_coroutine():
    while True:
        yield from asyncio.sleep(0.5)
        print('Hello World Coroutine ' + str(datetime.datetime.now().time()))

@asyncio.coroutine
def good_evening_coroutine():
    while True:
        yield from asyncio.sleep(0.5)
        print('Good Evening Coroutine ' + str(datetime.datetime.now().time()))


# Get main event loop
print('step: asyncio.get_event_loop()')
loop = asyncio.get_event_loop()

# Call functions from main loop
print('step: loop.call_soon(hello_world, loop)')
loop.call_soon(hello_world, loop)
print('step: loop.call_soon(good_evening, loop)')
loop.call_soon(good_evening, loop)
print('step: asyncio.async(hello_world_coroutine)')
asyncio.async(hello_world_coroutine())
print('step: asyncio.async(good_evening_coroutine)')
asyncio.async(good_evening_coroutine())

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print('step: loop.close()')
    loop.close()
