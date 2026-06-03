import os
import time
from pathlib import Path

import pandas as pd
import redis
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD"),
)
DATA_PATH = Path(__file__).parent / "data" / "titanic.csv"


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route("/")
def hello():
    count = get_hit_count()
    return render_template("hello.html", name="BIPM", count=count)


@app.route("/titanic")
def titanic():
    df = pd.read_csv(DATA_PATH)
    preview_html = df.head(5).to_html(
        classes="data-table",
        index=False,
        border=0,
    )
    survived_by_sex = (
        df[df["Survived"] == 1]
        .groupby("Sex")
        .size()
        .reindex(["female", "male"], fill_value=0)
    )
    max_survivors = max(int(survived_by_sex.max()), 1)
    chart_rows = [
        {
            "label": sex.title(),
            "value": int(value),
            "width": round((int(value) / max_survivors) * 100, 1),
        }
        for sex, value in survived_by_sex.items()
    ]
    return render_template(
        "titanic.html",
        preview_html=preview_html,
        chart_rows=chart_rows,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
