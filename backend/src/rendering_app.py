from flask import request, make_response
from optimization_app import build_app, endpoint
from app_config.rendering_parameters import RENDERER_POOL_SIZE
from bike_rendering.bikeCad_renderer import RenderingService

rendering_app = build_app()
rendering_service = RenderingService(RENDERER_POOL_SIZE)


@rendering_app.route(endpoint("/rendering/render-bike"), methods=["POST"])
def render_bike():
    return rendering_service.render(request.data.decode("utf-8"))


@rendering_app.route(endpoint("/rendering/render-bike-object"), methods=["POST"])
def render_bike_object():
    with open("../test/resources/bike.bcad", "r") as file:
        response = make_response(rendering_service.render(file.read()))
        response.headers["Content-Type"] = "image/svg+xml"
        return response


@rendering_app.route(endpoint("/health"))
def health():
    return make_response({"status": "UP"})
