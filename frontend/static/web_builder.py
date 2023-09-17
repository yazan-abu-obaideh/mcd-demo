import os.path

import jinja2

BOOT_STRAP_CSS_LINK = """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM"
      crossorigin="anonymous"/>"""
BOOT_STRAP_SCRIPT_ELEMENT = """    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz"
      crossorigin="anonymous"
    ></script>
"""


def from_relative_path(relative_path):
    absolute_path = os.path.join(os.path.dirname(__file__), relative_path)
    return absolute_path


def template_path(template_name):
    return from_relative_path(f"html-building-blocks/{template_name}")


def build_template(template_name, **kwargs):
    with open(template_path(template_name)) as file:
        return jinja2.Environment().from_string(file.read()).render(**kwargs)


def build_seed_bike_selection(id_suffix):
    return build_template("seed-bike-selection.html", id_suffix=id_suffix)


if __name__ == '__main__':
    os.makedirs(from_relative_path("web-target"), exist_ok=True)
    with open(from_relative_path("html-building-blocks/decode-template.html")) as _file:
        template = jinja2.Environment().from_string(_file.read())
    with open(from_relative_path("web-target/decode.html"), "w") as _file:
        _file.write(template.render(bootstrap_css_link_element=BOOT_STRAP_CSS_LINK,
                                    bootstrap_script_element=BOOT_STRAP_SCRIPT_ELEMENT,
                                    seed_bike_selection_upload=build_seed_bike_selection(id_suffix="upload-rider"),
                                    seed_bike_selection_specify_dimensions=build_seed_bike_selection(
                                        id_suffix="specify-rider-dimensions"),
                                    seed_bike_selection_seeds=build_seed_bike_selection(id_suffix="specify")))
