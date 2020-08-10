from vocabee import create_app
import os

app = create_app()


@app.context_processor
def inject_env():
    return dict(GA_TRACKING_ID=os.getenv("GA_TRACKING_ID"))
