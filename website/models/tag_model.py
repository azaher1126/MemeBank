from dataclasses import dataclass
from ..database.tag_model import Tag

@dataclass
class TagType():
    id: int
    name: str

    def __init__(self, tag) -> None:
        self.id = tag.id
        self.name = tag.name

def convert_to_tagtype(tags: list[Tag]) -> list[TagType]:
    return [TagType(tag) for tag in tags]