from optimization_app import build_app, register_all_optimization_endpoints
from rendering_app import register_all_rendering_endpoints

app = build_app()
register_all_optimization_endpoints(app)
register_all_rendering_endpoints(app, register_shared=False)

if __name__ == "__main__":
    app.run(port=5000)
