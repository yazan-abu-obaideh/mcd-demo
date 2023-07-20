import asyncio
import platform
from asyncio import subprocess


class BikeCAD:
    def __init__(self):
        if platform.system() == "Windows":
            self._expected_success = b'Done!\r\n'
        else:
            self._expected_success = b'Done!\n'
        event_loop = asyncio.get_event_loop()
        self._executor = asyncio.run_coroutine_threadsafe(init_instance(), event_loop).result()

    def export_svgs(self, folder):
        self._run("svg<>" + folder + "\n")

    def export_pngs(self, folder):
        self._run("png<>" + folder + "\n")

    def export_svg_from_list(self, files):
        self._run("svglist<>" + "<>".join(files) + "\n")

    def export_png_from_list(self, files):
        self._run("pnglist<>" + "<>".join(files) + "\n")

    def kill(self):
        self._executor.kill()

    def _run(self, command):
        print("Running...")
        self._executor.stdin.write(bytes(command, 'UTF-8'))
        self._await_termination()


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
            if signal == b"Done!\n":
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
