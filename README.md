# VocaBee

This is the home repository of the website code of VocaBee. VocaBee is a Japanese language vocabulary tool, meant to
provide a modern solution to learning vocabulary for new students. See the website at
[vocabee.xyz](https://www.vocabee.xyz)!

# Technology stack

The application is written in Python (3.8+) with the Flask framework. Data is stored in a MySQL database 
(but should be database agnostic with some modifications). No front-end framework was used, scripting is done in 
pure JS (unless a dependency requires jquery). 

See the most noteable dependencies below:

## Backend

- Flask (web framework)
- Flask-security (user accounts)
- SQLAlchemy (database interaction)
- Genanki (anki deck creation)

## Frontend

- Jinja2 (templating)
- Datatables (extensive table package)
- Bootstrap (css toolkit)
- Crel (easy DOM creation)

# Data

Original vocabulary and example sentence data is sourced from [Tanos.co.uk](http://www.tanos.co.uk). While the site is
nearing antique at this point, its datasets are gigantic and solidly written. The data has been collected with a Python
webscrapere which you can find in [this repository](https://github.com/MichaelVerdegaal/tanos_scraper). Note that 
data from Tanos and data from VocaBee may not match exactly, as VocaBee can update the vocabulary quickly and 
dynamically.
