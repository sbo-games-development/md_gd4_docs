from src.model.tag_doc import TagDoc


class VarDoc:
    """
    Model class for holding documentation for a var or const.
    """

    def __init__(self, name: str, data_type: str, description: str, value, var_type: str = "var"):
        """
        Constructor of the const documentation model.

        Args:
            name: Name of the const
            data_type: Data type of the const
            description: Description of the const
            value: Should have data type as mentioned in data_type
            var_type: Could be "const", "export_var", "var" or "onready_var"
        """
        self.name: str = name
        self.tags: list[TagDoc] = []
        self.data_type: str = data_type
        self.description: str = description
        self.value = value
        self.var_type: str = var_type
