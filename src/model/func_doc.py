from src.model.var_doc import VarDoc


class FuncDoc:
    """

    """
    def __init__(self, name: str, description: str, args: list[VarDoc]):
        """

        Args:
            name: Name of the function
            description: Description of the function
            args: Argument(s) list of the function
        """
        self.name = name
        self.description = description
        self.args = args
