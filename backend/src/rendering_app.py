from flask import request, make_response
from optimization_app import build_app
from app_config.rendering_parameters import RENDERER_POOL_SIZE
from bike_rendering.bikeCad_renderer import RenderingService

rendering_app = build_app()
rendering_service = RenderingService(RENDERER_POOL_SIZE)


def endpoint(suffix):
    return f"/api/v1/rendering/{suffix}"


@rendering_app.route(endpoint("render-bike"), methods=["POST"])
def render_bike():
    return rendering_service.render(request.data.decode("utf-8"))


@rendering_app.route(endpoint("render-bike-object"), methods=["POST"])
def render_bike_object():
    print(f"{request.json=}")
    return rendering_service.render_object(request.json)


@rendering_app.route(endpoint("health"))
def health():
    return make_response({"status": "UP"})
