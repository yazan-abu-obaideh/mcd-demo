import asyncio
import os
import platform
import uuid
from asyncio import subprocess

WINDOWS = "Windows"

TIMEOUT_GRANULARITY = 0.5
TIMEOUT = 10


class BikeCAD:
    def __init__(self):
        self._expected_success = self._get_expected_success()
        self._event_loop = asyncio.new_event_loop()
        self._instance = self._event_loop.run_until_complete(self._init_instance())
        print("Started!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kill()

    def render(self, bike_xml):
        bike_path = self._generate_bike_path()
        self._write_to_file(bike_path, bike_xml)
        self.export_svg_from_list([bike_path])
        os.remove(bike_path)
        image_path = bike_path.replace("bcad", "svg")
        image_bytes = self._read_image(image_path)
        os.remove(image_path)
        return image_bytes

    def _read_image(self, image_path):
        with open(image_path, "rb") as file:
            image_bytes = file.read()
        return image_bytes

    def _write_to_file(self, bike_path, bike_xml):
        with open(bike_path, "w") as file:
            file.write(bike_xml)

    def _generate_bike_path(self):
        return f"{os.path.dirname(__file__)}/bikes/{str(uuid.uuid4())}.bcad"

    def export_svgs(self, folder):
        self._run("svg<>" + folder + "\n")

    def export_pngs(self, folder):
        self._run("png<>" + folder + "\n")

    def export_svg_from_list(self, files):
        self._run("svglist<>" + "<>".join(files) + "\n")

    def export_png_from_list(self, files):
        self._run("pnglist<>" + "<>".join(files) + "\n")

    async def _init_instance(self):
        command = f"java -jar {os.path.dirname(__file__)}/console_BikeCAD_final.jar"
        process = await asyncio.create_subprocess_shell(bytes(command, 'utf-8'),
                                                        stdin=subprocess.PIPE,
                                                        stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE)
        print("BikeCAD instance running")
        return process

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
            await asyncio.wait_for(await_termination(), TIMEOUT)

        async def await_termination():
            while True:
                print("Loop...")
                try:
                    signal = await asyncio.wait_for(get_latest_signal(), TIMEOUT_GRANULARITY)
                    print(f"{signal=}")
                    if signal == b"Done!\n":
                        return
                except asyncio.exceptions.TimeoutError:
                    pass
                try:
                    signal = await asyncio.wait_for(get_error_signal(), TIMEOUT_GRANULARITY)
                    print(f"{signal=}")
                    raise Exception(f"Something went wrong: {signal}")
                except asyncio.exceptions.TimeoutError:
                    pass

        self._event_loop.run_until_complete(await_termination_timed())

    def _get_expected_success(self):
        if platform.system() == WINDOWS:
            return b'Done!\r\n'
        else:
            return b'Done!\n'
