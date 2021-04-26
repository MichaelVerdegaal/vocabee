import os

from vocabee import create_app

app = create_app()

from flask import url_for


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return dict(links)
    # links is now a list of url, endpoint tuples


@app.context_processor
def inject_env():
    return dict(GA_TRACKING_ID=os.getenv("GA_TRACKING_ID"))
