from src.model.var_doc import VarDoc
from src.model.tag_doc import TagDoc


class FuncDoc:
    """
    Model class for holding documentation for functions
    """
    def __init__(self, name: str, description: str, args: list[VarDoc]):
        """
        Constructor of the function documentation model.

        Args:
            name: Name of the function
            description: Description of the function
            args: Argument(s) list of the function
        """
        self.name = name
        self.tags: list[TagDoc] = []
        self.description = description
        self.args = args
