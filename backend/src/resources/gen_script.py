import os
import random

from cad_services.bikeCad_renderer import RenderingService
from cad_services.bike_xml_handler import BikeXmlHandler
from cad_services.cad_builder import BikeCadFileBuilder
from mcd_demo.fit_optimization.optimization_constants import TEMP_SEED_BIKES_MAP
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
    for i in range(1, 14):
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


def generate_form_html(form_id, display, seed_bike_id_suffix, dimension_input_div, on_click_function):
    return f"""        <form id="{form_id}" style="display: {display}">
    {dimension_input_div}

          <div id="seed-bike-selection-container-{seed_bike_id_suffix}" class="m-3">
            <h3>Select Seed Bike</h3>
            <div id="bikes-container-{seed_bike_id_suffix}" class="m-3"></div>
            <div id="all-bikes-helper-div-{seed_bike_id_suffix}">
              <div class="row p-5">
                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike1.png"
                    alt="seed-bike-1"
                  />
                  <br />
                  <input
                    id="seed1-{seed_bike_id_suffix}"
                    value="1"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed1-{seed_bike_id_suffix}">Snow Camo</label>
                </div>

                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike2.png"
                    alt="seed-bike-2"
                  />
                  <br />
                  <input
                    id="seed2-{seed_bike_id_suffix}"
                    value="2"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed2-{seed_bike_id_suffix}">Childlike</label>
                </div>

                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike3.png"
                    alt="seed-bike-3"
                  />
                  <br />
                  <input
                    id="seed3-{seed_bike_id_suffix}"
                    value="3"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed3-{seed_bike_id_suffix}">Fiery</label>
                </div>
              </div>

              <div class="row p-5">
                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike11.png"
                    alt="seed-bike-11"
                  />
                  <br />
                  <input
                    id="seed11-{seed_bike_id_suffix}"
                    value="11"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed11-{seed_bike_id_suffix}">Pythonic</label>
                </div>

                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike5.png"
                    alt="seed-bike-5"
                  />
                  <br />
                  <input
                    id="seed5-{seed_bike_id_suffix}"
                    value="5"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed5-{seed_bike_id_suffix}">Inferno</label>
                </div>

                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike6.png"
                    alt="seed-bike-6"
                  />
                  <br />
                  <input
                    id="seed6-{seed_bike_id_suffix}"
                    value="6"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed6-{seed_bike_id_suffix}">Wintery</label>
                </div>
              </div>
              <div class="row p-5">
                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike7.png"
                    alt="seed-bike-7"
                  />
                  <br />
                  <input
                    id="seed7-{seed_bike_id_suffix}"
                    value="7"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed7-{seed_bike_id_suffix}">Pastel</label>
                </div>

                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike10.png"
                    alt="seed-bike-10"
                  />
                  <br />
                  <input
                    id="seed10-{seed_bike_id_suffix}"
                    value="10"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed10-{seed_bike_id_suffix}">Standard</label>
                </div>

                <div class="col seed-bike-div">
                  <img
                    class="seed-bike-img"
                    src="assets/bike12.png"
                    alt="seed-bike-12"
                  />
                  <br />
                  <input
                    id="seed12-{seed_bike_id_suffix}"
                    value="12"
                    name="seedBike"
                    type="radio"
                    class="form-check-input"
                    required
                  />
                  <label class="form-check-label" for="seed12-{seed_bike_id_suffix}">Sleek</label>
                </div>
              </div>
            </div>
          </div>
          <div class="p-3">
            <div class="row flex-cont text-center justify-content-center">
              <div class="dropdown">
                <button
                  class="btn btn-outline-danger btn-lg dropdown-toggle w-40"
                  type="button"
                  id="dropdownMenuButton1-{seed_bike_id_suffix}"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Generate!
                </button>
                <ul
                  class="dropdown-menu w-40"
                  aria-labelledby="dropdownMenuButton1"
                >
                  <li>
                    <button
                      type="button"
                      class="dropdown-item"
                      onclick="{on_click_function}('ergonomics')"
                    >
                      Ergonomic bikes!
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      class="dropdown-item"
                      onclick="{on_click_function}('aerodynamics')"
                    >
                      Aerodynamic bikes!
                    </button>
                  </li>
                  <li>
                    <button
                      type="button"
                      class="dropdown-item disabled"
                    >
                      Structurally-optimal bikes! [COMING SOON]
                    </button>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </form>
"""


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
    with open("rider-images/person2.jpg", "rb") as file:
        print(PoserAnalyzer().analyze_bytes_mm(
            70,
            file.read()
        ))

