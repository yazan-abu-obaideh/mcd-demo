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


def build_target(target_dir,
                 bootstrap_css_link_element,
                 bootstrap_script_element,
                 read_more_href,
                 decode_href):
    os.makedirs(from_relative_path(f"{target_dir}"), exist_ok=True)
    with open(from_relative_path(f"{target_dir}/decode.html"), "w") as file:
        file.write(
            build_template(
                "decode-template.html",
                seed_bike_selection_upload=build_seed_bike_selection(id_suffix="upload-rider"),
                seed_bike_selection_specify_dimensions=build_seed_bike_selection(
                    id_suffix="specify-rider-dimensions"),
                seed_bike_selection_seeds=build_seed_bike_selection(id_suffix="specify"),
                bootstrap_css_link_element=bootstrap_css_link_element,
                bootstrap_script_element=bootstrap_script_element,
                read_more_href=read_more_href
            ))
    with open(from_relative_path(f"{target_dir}/read-more.html"), "w") as file:
        file.write(build_template("read-more-template.html", decode_href=decode_href))


def build_web_target():
    return build_target(
        "web-target",
        bootstrap_css_link_element=BOOT_STRAP_CSS_LINK,
        bootstrap_script_element=BOOT_STRAP_SCRIPT_ELEMENT,
        read_more_href="/read-more",
        decode_href="/"
    )


def build_gui_target():
    return build_target(
        "gui-target",
        bootstrap_css_link_element=BOOT_STRAP_CSS_LINK,
        bootstrap_script_element=BOOT_STRAP_SCRIPT_ELEMENT,
        read_more_href="/gui-target/read-more.html",
        decode_href="/gui-target/decode.html"
    )


if __name__ == '__main__':
    build_web_target()
    build_gui_target()
