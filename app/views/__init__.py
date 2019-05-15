from app.views import info, action_plans, load_sample, action_rules, generate_qid_batch


def setup_blueprints(app):
    app.register_blueprint(info.blueprint)
    app.register_blueprint(action_plans.blueprint)
    app.register_blueprint(load_sample.blueprint)
    app.register_blueprint(action_rules.blueprint)
    app.register_blueprint(generate_qid_batch.blueprint)
