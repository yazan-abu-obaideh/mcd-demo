import platform
import subprocess
import time


class BikeCAD:
    def __init__(self):
        if platform.system() == "Windows":
            self._expected_success = b'Done!\r\n'
        else:
            self._expected_success = b'Done!\n'

        self._instance = self._start_bike_cad_Instance()

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
        self._instance.stdin.write(bytes(command, 'UTF-8'))
        self._instance.stdin.flush()
        self._await_termination()

    def _await_termination(self):
        print("awaiting...")
        _process_signal = self._instance.communicate()
        print(_process_signal)
        # while self._no_success_signal() and self._no_error_signal():
        #     print("Done...")
        #     time.sleep(0.01)

    def _no_success_signal(self):
        return self._instance.stdout.readline() != self._expected_success

    def _no_error_signal(self):
        error_signal = self._instance.stderr.readline()
        has_error = error_signal is not None
        if has_error:
            print(error_signal)
        return has_error


if __name__ == "__main__":
    inst = BikeCAD()
    start = time.time()
    inst.export_pngs("small")
    print(f"{time.time() - start}")
    inst.kill()
