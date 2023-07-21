import asyncio
from asyncio import subprocess


async def init_instance():
    process = await asyncio.create_subprocess_shell(b"java -jar console_BikeCAD_final.jar",
                                                    stdin=subprocess.PIPE,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
    return process


async def do_everything():
    instance_ = await init_instance()
    instance_.stdin.write(bytes("svg<>small\n", "utf-8"))

    # instance_.stdin.flush()

    async def get_latest_signal():
        return await instance_.stdout.readline()

    async def get_error_signal():
        return await instance_.stderr.readline()

    while True:
        print("Loop...")
        try:
            signal = await asyncio.wait_for(get_latest_signal(), 1)
            print(f"{signal=}")
            if signal in [b"Done!\n", b'Done!\r\n']:
                return
        except asyncio.exceptions.TimeoutError:
            pass
        try:
            signal = await asyncio.wait_for(get_error_signal(), 1)
            print(f"{signal=}")
            raise Exception(f"Something went wrong: {signal}")
        except asyncio.exceptions.TimeoutError:
            pass


result = asyncio.run(do_everything())
print(result)
