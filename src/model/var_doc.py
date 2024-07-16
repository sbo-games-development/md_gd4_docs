from src.model.tag_doc import TagDoc


class VarDoc:
    """
    Model class for holding documentation for a var or const.
    """

    def __init__(
            self,
            name: str,
            data_type: str,
            description: str,
            value=None,
            var_type: str = "var",
            tags: list[TagDoc] = None
    ):
        """
        Constructor of the const documentation model.

        Args:
            name: Name of the const
            data_type: Data type of the const
            description: Description of the const
            value: Should have data type as mentioned in data_type
            var_type: Could be "const", "export_var", "var" or "onready_var"
            tags: Tag(s) of the signal, if any
        """
        self.name: str = name
        self.data_type: str = data_type
        if tags is None:
            self.tags: list[TagDoc] = []
        else:
            self.tags: list[TagDoc] = tags
        self.description: str = description
        self.value = value
        self.var_type: str = var_type
        if self.var_type != "const" \
                or self.var_type != "export_var" \
                or self.var_type != "var" \
                or self.var_type != "onready_var":
            raise Exception('Only "const", "export_var", "var" or "onready_var" are valid var types')
