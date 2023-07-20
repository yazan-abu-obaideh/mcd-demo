import platform
import select
import subprocess
import time

TIMEOUT_GRANULARITY = 1

TIMEOUT_SECONDS = 5

DEFAULT_MAX_SIZE = 3


def _seconds_to_millis(seconds):
    return seconds * 1000


class BikeCAD:
    def __init__(self):
        if platform.system() == "Windows":
            self._expected_success = b'Done!\r\n'
        else:
            self._expected_success = b'Done!\n'

        self._instance = self._start_bike_cad_Instance()
        self._output_listener = select.poll()
        self._output_listener.register(self._instance.stdout, select.POLLIN)
        self._error_listener = select.poll()
        self._error_listener.register(self._instance.stderr, select.POLLIN)

    def _start_bike_cad_Instance(self):
        p = subprocess.Popen('java -jar console_BikeCAD_final.jar'.split(' '), stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdout.read(14)
        return p

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
        self._instance.stdin.flush()
        self._await_termination()

    def _await_termination(self):
        start_time = time.time()
        while (time.time() - start_time) < TIMEOUT_SECONDS:
            if self._received_output_event(timeout=TIMEOUT_GRANULARITY):
                if self._check_output_for_success():
                    return
            if self._received_error_event(timeout=TIMEOUT_GRANULARITY):
                raise Exception(f"An exception occurred: {self._instance.stderr.readline()}")
        self.kill()
        raise TimeoutError("Process timed out...")

    def _received_output_event(self, timeout):
        return self._output_listener.poll(_seconds_to_millis(timeout))

    def _received_error_event(self, timeout):
        return self._error_listener.poll(_seconds_to_millis(timeout))

    def _check_output_for_success(self):
        signal = self._instance.stdout.readline()
        print(signal)
        return signal == self._expected_success


if __name__ == "__main__":
    bikeCAD = BikeCAD()
    start = time.time()
    bikeCAD.export_pngs("small")
    print(f"{time.time() - start}")
    bikeCAD.kill()
