import asyncio
import os.path

from flask import Flask, jsonify, request
from jinja2 import Environment, FileSystemLoader

from database import register_models

# Предполагается, что вы импортировали enums из database.data
from database.data import DurationEnum, LocationEnum, ThemeEnum
from database.methods import get_games_data
from misc import PathControl

env = Environment(
    loader=FileSystemLoader(PathControl.get(os.path.join("web_ui", "templates"))),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=True,
)

main_page_template = env.get_template("index.html")
app = Flask(__name__)


@app.route("/")
def index():
    return main_page_template.render(
        durations=[str(d) for d in DurationEnum],
        locations=[str(i) for i in LocationEnum],
        themes=[str(t) for t in ThemeEnum],
    )


@app.route("/get_games_data", methods=["POST"])
def handle_get_games_data():
    data = request.json
    duration = data.get("duration")
    location = data.get("location")
    theme = data.get("theme")
    games_data = asyncio.run(get_games_data(duration, location, theme))
    print(len(games_data))
    games_data = [
        {
            "title": g.title,
            "condition": g.condition,
            "duration": g.duration,
            "location": g.location,
            "theme": g.theme,
        }
        for g in games_data
    ]
    return jsonify(games_data)


if __name__ == "__main__":
    asyncio.run(register_models())
    app.run(debug=False)
