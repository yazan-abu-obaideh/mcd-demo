import os
import random

from cad_services.bikeCad_renderer import RenderingService
from cad_services.bike_xml_handler import BikeXmlHandler
from cad_services.cad_builder import BikeCadFileBuilder
from fit_optimization.optimization_constants import TEMP_SEED_BIKES_MAP
from pose_analysis.pose_image_processing import PoserAnalyzer

"""This just exists so I can retrace my steps and if necessary redo some of the work fast"""

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
        file_path = f"seed-bikes/bike{i}.bcad"
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
    for i in range(1, 14):
        file_path = f"seed-bikes/bike{i}.bcad"
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


def analyze_images():
    images = [f"person{i}.jpg" for i in range(1, 4)]
    heights_inches = [73.6, 68.5, 61]
    analyzer = PoserAnalyzer()
    for image, person_height in zip(images, heights_inches):
        image_path = os.path.join(os.path.dirname(__file__), "rider-images", image)
        with open(image_path, "rb") as file:
            file_bytes = file.read()
            print(analyzer.analyze_bytes_mm(person_height, file_bytes))


def generate_seed_bikes_html():
    def fill_template(i, label):
        return f"""
        <div class="col seed-bike-div">
            <img class="seed-bike-img" src="assets/bike{i}.png" alt="seed-bike-{i}"/>
            <br/>
            <input id="seed{i}" value="{i}" name="seedBike" type="radio" class="form-check-input" required />
            <label class="form-check-label" for="seed{i}">{label}</label>
      </div>
"""

    result = ""
    for bike_number, bike_label in zip(range(1, 10), ["BIKE" for _ in range(10)]):
        result += fill_template(bike_number, bike_label)
    return result


def modify_seeds():
    all_bikes = list(TEMP_SEED_BIKES_MAP.values())
    builder = BikeCadFileBuilder()
    for i in range(13):
        updated_cad = builder.build_cad_from_object(all_bikes[i], str(i + 1))
        with open(f"seed-bikes/bike{i + 1}.bcad", "w") as file:
            file.write(updated_cad)


# USE THIS APPENDED TO THE END OF BIKE-INTEGRATION.EVALUATION_REQUEST_PROCESSOR TO GENERATE MAP
# result = {}
# for i in range(1, 11):
#     with open(f"seed-bikes/bike{i}.bcad", "r") as file:
#         # noinspection PyTypeChecker
#         file_data = file.read()
#         mapped = EvaluationRequestProcessor(None,
#                                             DefaultMapperSettings()).map_to_validated_model_input(
#             file_data)
#         xml_handler = BikeXmlHandler()
#         xml_handler.set_xml(file_data)
#         original = xml_handler.get_entries_dict()
#         mapped = {
#             key: value for key, value in mapped.items() if key in ["HT Length",
#                                                                    "HT Angle",
#                                                                    "HT LX",
#                                                                    "ST Length",
#                                                                    "ST Angle",
#                                                                    ]
#         }
#
#         original = {key: value for key, value in original.items() if key in ["Stack",
#                                                                              "Seatpost LENGTH",
#                                                                              "Saddle height",
#                                                                              "Stem length",
#                                                                              "Stem angle",
#                                                                              "Headset spacers",
#                                                                              "Crank length",
#                                                                              "Handlebar style"]}
#
#         mapped.update(original)
#         mapped["DT Length"] = 500
#         if not ("Stack" in mapped.keys()):
#             mapped["Stack"] = 565.5
#         result[str(i)] = {key: float(value) for key, value in mapped.items()}
# print(result)

if __name__ == "__main__":
    modify_seeds()
    render_seeds()
