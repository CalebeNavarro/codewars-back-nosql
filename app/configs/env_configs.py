from flask import Flask

def init_app(app: Flask):
    app.config["JSON_SORT_KEYS"] = False
