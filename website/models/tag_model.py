from ..database.tag_model import Tag

class TagType():
    def __init__(self, tag) -> None:
        self.id = tag.id
        self.name = tag.name

def convert_to_tagtype(tags: list[Tag]) -> list[TagType]:
    tagT = []
    for tag in tags:
        tagT.append(TagType(tag))
    return tagT