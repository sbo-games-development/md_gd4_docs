from src.model.var_doc import VarDoc
from src.model.tag_doc import TagDoc


class FuncDoc:
    """
    Model class for holding documentation for functions
    """
    def __init__(self, name: str, description: str, args: list[VarDoc], tags: list[TagDoc] = None):
        """
        Constructor of the function documentation model.

        Args:
            name: Name of the function
            description: Description of the function
            args: Argument(s) list of the function
        """
        self.code: str = ""
        self.name = name
        if tags is None:
            self.tags: list[TagDoc] = []
        else:
            self.tags: list[TagDoc] = tags
        self.description = description
        self.args = args

    def append_code_line(self, line: str):
        """
        Appends a line of code to the func doc. No auto linebreak, so \n need to be in line (if needed)

        Args:
            line: The line of code to be added
        """
        self.code = self.code + line

    def set_code(self, code: str):
        """
        Sets the code of the function to the func doc

        Args:
            code: All Code lines of the function
        """
        self.code = code
