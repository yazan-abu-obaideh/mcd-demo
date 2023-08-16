import os
import random

from cad_services.bikeCad_renderer import RenderingService
from cad_services.bike_xml_handler import BikeXmlHandler

background_colors = {
    "BACKGROUND color BLUE": "255",
    "BACKGROUND color RED": "255",
    "BACKGROUND color GREEN": "255",
    "BACKGROUND color IMAGEaspectR": "true",
    "BACKGROUND color TILED": "false",
    "BACKGROUND color IMAGEYES": "false",
    "BACKGROUND color IMAGEFitHeight": "false",
    "BACKGROUND color sRGB": "-1",
    "BACKGROUND color IMAGENAME": "fade_to_black_at_top.png",
    "BACKGROUND color IMAGEFitWidth": "true"
}


def make_backgrounds_white():
    for i in range(1, 8):
        xml_handler = BikeXmlHandler()
        file_path = f"good-seeds/bike{i}.bcad"
        with open(file_path, "r") as file:
            xml_handler.set_xml(file.read())

        for entry_key, entry_value in background_colors.items():
            entry = xml_handler.find_entry_by_key(entry_key)
            if entry:
                xml_handler.update_entry_value(entry, entry_value)
            else:
                xml_handler.add_new_entry(entry_key, entry_value)
        with open(file_path, "w") as file:
            file.write(xml_handler.get_content_string())


def render_seeds():
    rendering_service = RenderingService(1)
    for i in range(1, 8):
        file_path = f"good-seeds/bike{i}.bcad"
        with open(file_path, "r") as file:
            rendered = rendering_service.render(file.read())
        with open(file_path.replace(".bcad", ".svg"), "wb") as img_file:
            img_file.write(rendered)


def render_random_sample():
    rendering_service = RenderingService(1)
    potential_bikes = os.listdir("potential-seeds")
    random.shuffle(potential_bikes)
    for bike_file_name in potential_bikes[:100]:
        bike_path = os.path.join("potential-seeds", bike_file_name)
        with open(bike_path, "r") as file:
            image = rendering_service.render(file.read())
        with open(os.path.join("potential-seeds", bike_file_name.replace(".bcad", ".svg")), "wb") as img_file:
            img_file.write(image)


if __name__ == "__main__":
    make_backgrounds_white()
    render_seeds()
