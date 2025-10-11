from ..database import db
from ..database.tag_model import Tag
from ..database.tag_entry import tag_entries
from sqlalchemy import func, desc
from urllib.parse import quote_plus

def get_popular_tag_links():
    popular_tags = (db.session.query(Tag, func.count(tag_entries.c.tag_id)
                                     .label("meme_count")).join(tag_entries)
                                     .group_by(Tag.id).order_by(desc("meme_count"))
                                     .limit(8).all())
    
    return [(f"#{x.t[0].name}", f"/search?search={quote_plus(x.t[0].name)}") for x in popular_tags]