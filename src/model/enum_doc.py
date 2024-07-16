from src.model.enum_member_doc import EnumMemberDoc
from src.model.tag_doc import TagDoc


class EnumDoc:
    """
    Model class for storing enum documentation (including enum members)
    """
    def __init__(self, name: str, description: str, tags: list[TagDoc] = None):
        """
        Constructor of the enum documentation model

        Args:
            name: Name of the enum
            description: Description of the enum
        """
        self.name: str = name
        self.description: str = description
        if tags is None:
            self.tags: list[TagDoc] = []
        else:
            self.tags: list[TagDoc] = tags
        self.members: list[EnumMemberDoc] = []
