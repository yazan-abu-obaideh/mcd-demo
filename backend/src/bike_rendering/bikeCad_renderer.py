import asyncio
import os
import platform
import queue
import threading
import uuid
from asyncio import subprocess
import logging
from app_config.rendering_parameters import RENDERER_TIMEOUT, RENDERER_TIMEOUT_GRANULARITY
from bike_rendering.bike_xml_handler import BikeXmlHandler

from exceptions import InternalError

LOGGER_NAME = "BikeCadLogger"

WINDOWS = "Windows"

DEFAULT_BIKE_PATH = os.path.join(os.path.dirname(__file__), "../resources/PlainRoadbikestandardized.txt")

OPTIMIZED_TO_CAD = {
    "ST Angle": "Seat angle",
    "HT Length": "Head tube length textfield",
    "HT Angle": "Head angle",
    "HT LX": "Head tube lower extension2",
    'Stack': 'Stack',
    "ST Length": "Seat tube length",
    "Seatpost LENGTH": "Seatpost LENGTH",
    "Saddle height": "Saddle height",
    "Stem length": "Stem length",
    "Crank length": "Crank length",
    "Headset spacers": "Headset spacers",
    "Stem angle": "Stem angle",
    "Handlebar style": "Handlebar style",
}


class RenderingService:
    def __init__(self, renderer_pool_size):
        self._renderer_pool = queue.Queue(maxsize=renderer_pool_size)
        for i in range(renderer_pool_size):
            self._renderer_pool.put(BikeCad())

    def render_object(self, bike_object):
        xml_handler = BikeXmlHandler()
        with open(DEFAULT_BIKE_PATH, "r") as file:
            xml_handler.set_xml(file.read())
        for response_key, cad_key in OPTIMIZED_TO_CAD.items():
            xml_handler.update_entry_value(xml_handler.find_entry_by_key(cad_key),
                                           str(bike_object[response_key]))
        return self.render(xml_handler.get_content_string())

    def render(self, bike_xml):
        renderer = self._get_renderer()
        result = renderer.render(bike_xml)
        self._renderer_pool.put(renderer)  # This will never block as is - no new elements
        # are ever added, so the pool will always have room for borrowed renderers.
        return result

    def _get_renderer(self):
        return self._renderer_pool.get(timeout=RENDERER_TIMEOUT / 2)


class BikeCad:
    def __init__(self):
        self._expected_success = self._get_expected_success()
        self._event_loop_lock = threading.Lock()
        with self._event_loop_lock:
            self._event_loop = asyncio.new_event_loop()
            self._instance = self._event_loop.run_until_complete(self._init_instance())
        self._log_info("Started BikeCAD process!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kill()

    def render(self, bike_xml):
        bike_path = self._generate_bike_path()
        self._write_to_file(bike_path, bike_xml)
        self._export_svg_from_list([bike_path])
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

    def _export_svgs(self, folder):
        self._run("svg<>" + folder + "\n")

    def _export_pngs(self, folder):
        self._run("png<>" + folder + "\n")

    def _export_svg_from_list(self, files):
        self._run("svglist<>" + "<>".join(files) + "\n")

    def _export_png_from_list(self, files):
        self._run("pnglist<>" + "<>".join(files) + "\n")

    async def _init_instance(self):
        command = f"java -Djava.awt.headless=false -jar  {os.path.dirname(__file__)}/console_BikeCAD_final.jar"
        process = await asyncio.create_subprocess_shell(bytes(command, 'utf-8'),
                                                        stdin=subprocess.PIPE,
                                                        stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE)
        self._log_info("BikeCAD instance running")
        return process

    def kill(self):
        self._instance.kill()

    def _run(self, command):
        self._log_info(f"Running command {command}...")
        self._instance.stdin.write(bytes(command, 'UTF-8'))
        self._await_termination()

    def _await_termination(self):

        async def get_latest_signal():
            return await self._instance.stdout.readline()

        async def get_error_signal():
            return await self._instance.stderr.readline()

        async def await_termination_timed():
            try:
                await asyncio.wait_for(await_termination(), RENDERER_TIMEOUT)
            except asyncio.exceptions.TimeoutError:
                self._log_error(f"Renderer timed out!")
                raise InternalError("Something went wrong: rendering took too long")

        async def await_termination():
            while True:
                self._log_info("Loop...")
                signal = await self._wait_or_pass(get_latest_signal())
                if signal == b"Done!\n":
                    return
                signal = await self._wait_or_pass(get_error_signal())
                if signal:
                    self._log_error(f"Renderer threw an exception! {signal}")
                    raise Exception(f"Something went wrong: {signal}")

        with self._event_loop_lock:
            self._event_loop.run_until_complete(await_termination_timed())

    def _get_expected_success(self):
        if platform.system() == WINDOWS:
            return b'Done!\r\n'
        else:
            return b'Done!\n'

    async def _wait_or_pass(self, future):
        try:
            signal = await asyncio.wait_for(future, RENDERER_TIMEOUT_GRANULARITY / 2)
            self._log_info(f"{signal}")
            return signal
        except asyncio.exceptions.TimeoutError:
            return None

    def _log_info(self, log_message):
        logging.getLogger(LOGGER_NAME).info(log_message)

    def _log_error(self, log_message):
        logging.getLogger(LOGGER_NAME).error(log_message)
