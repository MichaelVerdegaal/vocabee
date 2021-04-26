import os

from vocabee import create_app

app = create_app()


@app.context_processor
def inject_env():
    return dict(GA_TRACKING_ID=os.getenv("GA_TRACKING_ID"))
