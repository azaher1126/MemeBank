from flask import Flask

from .template_functions import get_popular_tag_links

def initialize_templates(app: Flask):
    app.add_template_global(get_popular_tag_links)