from src.model.enum_member_doc import EnumMemberDoc


class EnumDoc:
    """
    Model class for storing enum documentation (including enum members)
    """
    def __init__(self, name: str, description: str):
        """
        Constructor of the enum documentation model

        Args:
            name: Name of the enum
            description: Description of the enum
        """
        self.name: str = name
        self.description: str = description
        self.members: list[EnumMemberDoc] = []
