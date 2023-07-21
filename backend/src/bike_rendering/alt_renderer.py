import asyncio
import platform
from asyncio import subprocess


class BikeCAD:
    def __init__(self):
        if platform.system() == "Windows":
            self._expected_success = b'Done!\r\n'
        else:
            self._expected_success = b'Done!\n'
        self._event_loop = asyncio.new_event_loop()
        self._instance = self._event_loop.run_until_complete(self._init_instance())
        print("Started!")

    async def _init_instance(self):
        process = await asyncio.create_subprocess_shell(b"java -jar console_BikeCAD_final.jar",
                                                        stdin=subprocess.PIPE,
                                                        stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE)
        print("Process built!")
        return process

    def export_svgs(self, folder):
        self._run("svg<>" + folder + "\n")

    def export_pngs(self, folder):
        self._run("png<>" + folder + "\n")

    def export_svg_from_list(self, files):
        self._run("svglist<>" + "<>".join(files) + "\n")

    def export_png_from_list(self, files):
        self._run("pnglist<>" + "<>".join(files) + "\n")

    def kill(self):
        self._instance.kill()

    def _run(self, command):
        print("Running...")
        self._instance.stdin.write(bytes(command, 'UTF-8'))
        self._await_termination()

    def _await_termination(self):

        async def get_latest_signal():
            return await self._instance.stdout.readline()

        async def get_error_signal():
            return await self._instance.stderr.readline()

        async def await_termination_timed():
            await asyncio.wait_for(await_termination(), 10)

        async def await_termination():
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

        self._event_loop.run_until_complete(await_termination_timed())


bikeCad = BikeCAD()
bikeCad.export_pngs("small")
