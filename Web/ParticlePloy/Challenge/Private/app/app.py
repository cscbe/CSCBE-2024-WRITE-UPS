import json

from flask import (
    render_template,
    request,
    g,
    redirect,
    Flask,
    Response,
    Blueprint,
)
from flask_talisman import Talisman
import werkzeug
import db
from wtforms import (
    Form,
    BooleanField,
    StringField,
    validators,
    IntegerField,
    FloatField,
)

# from html_sanitizer import Sanitizer, sanitizer

blueprint = Blueprint("default", __name__, url_prefix="/")


def create_app() -> Flask:
    app = Flask(__name__)
    import initialize_db

    Talisman(
        app,
        force_https=False,
        content_security_policy={"script-src": ["'strict-dynamic'"]},
        content_security_policy_nonce_in=["script-src"],
    )

    app.register_blueprint(blueprint)

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    return app


class ParticleConfigForm(Form):
    name = StringField("A cool name for your particles!")
    maxParticles = IntegerField(
        "Maximum Particles", [validators.NumberRange(min=0, max=1000)], default=100
    )
    sizeVariations = FloatField("Size Variations", default=3.0)
    speed = FloatField("Speed", default=0.5)
    color = StringField(
        "Color (hexadecimal representation)",
        validators=[validators.Regexp(regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")],
        default="#000000",
    )
    minDistance = FloatField("Min Distance for Connecting Lines (px)", default=120.0)
    connectParticles = BooleanField("Connect Particles", default=False)


@blueprint.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return "bad request!", 400


@blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ParticleConfigForm(request.form)
    if request.method == "POST" and form.validate():
        config = {
            "maxParticles": form.maxParticles.data,
            "sizeVariations": form.sizeVariations.data,
            "speed": form.speed.data,
            "color": form.color.data,
            "minDistance": form.minDistance.data,
            "connectParticles": form.connectParticles.data,
        }
        config = json.dumps(config)
        id = db.save_particle_config(form.name.data, config)
        return redirect(f"/particles/{id}")
    else:
        return render_template("index.html", form=form)


# DEFAULT_HTML_SANITIZER_SETTINGS = {
#     "tags": {
#         "a",
#         "h1",
#         "h2",
#         "h3",
#         "strong",
#         "em",
#         "p",
#         "ul",
#         "ol",
#         "li",
#         "br",
#         "sub",
#         "sup",
#         "hr",
#     },
#     "attributes": {"a": ("href", "name", "target", "title", "id", "rel")},
#     "empty": {"hr", "a", "br"},
#     "separate": {"a", "p", "li"},
#     "whitespace": {"br"},
#     "keep_typographic_whitespace": False,
#     "add_nofollow": False,
#     "autolink": False,
#     "sanitize_href": sanitizer.sanitize_href,
#     "element_preprocessors": [
#         # convert span elements into em/strong if a matching style rule
#         # has been found. strong has precedence, strong & em at the same
#         # time is not supported
#         sanitizer.bold_span_to_strong,
#         sanitizer.italic_span_to_em,
#         sanitizer.tag_replacer("b", "strong"),
#         sanitizer.tag_replacer("i", "em"),
#         sanitizer.tag_replacer("form", "p"),
#         sanitizer.target_blank_noopener,
#     ],
#     "element_postprocessors": [],
#     "is_mergeable": lambda e1, e2: True,
# }
# custom_sanitizer = Sanitizer(DEFAULT_HTML_SANITIZER_SETTINGS)


@blueprint.route("/particles/<uuid>", methods=["GET"])
def view_particles(uuid):
    pc = db.get_particle_config(uuid)
    # sanitized_name = custom_sanitizer.sanitize(pc["name"])
    return render_template(
        "view.html", name=pc["name"], config=pc["config"], uuid=pc["uuid"]
    )


@blueprint.route("/particles/<uuid>/custom_particle_config.js", methods=["GET"])
def custom_particle_js(uuid):
    pc = db.get_particle_config(uuid)
    particles_config = pc["config"]

    return Response(
        response=render_template("particles.js", particles_config=particles_config),
        status=200,
        mimetype="application/javascript",
    )


@blueprint.route("/admin")
def admin():
    return db.get_all_particles()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
