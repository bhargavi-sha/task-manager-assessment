from flask import Flask
from config import Config
from models import db
from models.task import Task
from routes.task_routes import task_bp
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})



    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(task_bp)

    @app.route("/")
    def home():
        return {"message": "Task Manager API Running"}

    # ✅ Print registered routes
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

