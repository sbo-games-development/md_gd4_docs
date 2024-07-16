from src.model.tag_doc import TagDoc


class EnumMemberDoc:
    """
    Model class for storing enum members
    """
    def __init__(self, value_name: str, value_int: int, description: str, tags: list[TagDoc] = None):
        """
        Constructor of the enum member documentation model

        Args:
            value_name: Name of the enum member
            value_int: Value of the enum member
            description: Description of the enum member
        """

        self.value_name = value_name
        self.value_int = value_int
        if tags is None:
            self.tags: list[TagDoc] = []
        else:
            self.tags: list[TagDoc] = tags
        self.description = description
