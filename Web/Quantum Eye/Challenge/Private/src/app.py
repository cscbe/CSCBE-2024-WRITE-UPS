import os
import random
from base64 import b64encode
from functools import wraps
from urllib.parse import urlparse

from playwright.async_api import async_playwright
from quart import Quart, abort, jsonify, redirect, render_template, request

app = Quart(__name__)
app.config["DEBUG"] = True
app.secret_key = "SBBi5wVj6ReUSLAioqB7"

allowed_hosts = ["cybersecuritychallenge.be", "127.0.0.1", "::1", "localhost"]


async def capture_screenshot(url: str) -> str:
    """
    Captures a screenshot of the given URL and returns the screenshot as a base64-encoded image.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        screenshot = await page.screenshot()

        return b64encode(screenshot).decode("utf-8")


async def extract_domain(url: str) -> str:
    """
    Extracts the domain from the given URL.
    """
    if url.startswith("view-source:"):
        url = url.replace("view-source:", "", 1)
    return urlparse(url).netloc


@app.get("/")
async def index():
    return await render_template("index.html")


@app.route("/quantum-eye", methods=["GET", "POST"])
async def quantum_eye():
    if request.method == "GET":
        return await render_template("quantum-eye.html")

    try:
        data = await request.get_json()
        assert data["url"] is not None
    except:
        abort(400)

    domain = await extract_domain(data["url"])

    if domain not in allowed_hosts:
        return jsonify({"error": "This URL is not allowed in the preview."})

    if domain != "cybersecuritychallenge.be" and data["url"].startswith("https"):
        data["url"] = data["url"].replace("https", "http")

    if domain != "cybersecuritychallenge.be" and data["url"].startswith(
        "viewsource:https"
    ):
        data["url"] = data["url"].replace("https", "http")

    try:
        b64_img = await capture_screenshot(data["url"])
        return jsonify({"image": b64_img})
    except:
        return jsonify({"error": "An error occurred while capturing the screenshot."})


@app.get("/admin")
async def admin():
    if not request.remote_addr == "127.0.0.1" and not request.remote_addr == "::1":
        abort(403)

    return await render_template("admin.html")


@app.get("/th3-fl4g-1s-her3")
async def flag():
    if not request.remote_addr == "127.0.0.1" and not request.remote_addr == "::1":
        abort(403)

    flag = os.getenv(
        "FLAG", "There was an error retrieving the flag, please contact the admins."
    )

    rotation = random.randint(0, 360)

    return await render_template("flag.html", flag=flag, rotation=rotation)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
