from flask import request, make_response, Flask

from app_config.rendering_parameters import RENDERER_POOL_SIZE
from cad_services.bikeCad_renderer import RenderingService
from optimization_app import build_app, register_health_endpoint

rendering_app = build_app()
rendering_service = RenderingService(RENDERER_POOL_SIZE)


def endpoint(suffix):
    return f"/api/v1/rendering/{suffix}"


def register_rendering_endpoint(_app: Flask):
    @_app.route(endpoint("render-bike-object"), methods=["POST"])
    def render_bike_object():
        response = make_response(rendering_service.render_object(request.json["bike"],
                                                                 request.json["seedImageId"]))
        response.headers["Content-Type"] = "image/svg+xml"
        return response


def register_all_rendering_endpoints(_app: Flask, register_shared=True):
    register_rendering_endpoint(_app)
    if register_shared:
        register_health_endpoint(_app)


register_all_rendering_endpoints(rendering_app)
