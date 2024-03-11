from mcd_demo.app import build_full_app

app = build_full_app()

if __name__ == "__main__":
    app.run(port=5000)
