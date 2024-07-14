from src.model.enum_doc import EnumDoc
from src.model.var_doc import VarDoc
from src.model.func_doc import FuncDoc


class ClassDoc:
    """
    Model class for storing class documentation.
    """
    def __init__(self, file_name: str, class_name: str = "not exposed", inner_class: bool = False):
        """
        Constructor of the class documentation model.

        Args:
            file_name: Filename of the script
            class_name: Class name, only needed to expose class for inheritance or for inner classes
            inner_class: Is it an inner class? class_name becomes mandatory if True.
        """
        self.file_name: str = file_name
        self.class_name: str = class_name
        self.is_inner_class: bool = inner_class
        self.extends: str = ""
        self.brief_description: str = ""
        self.detail_description: str = ""
        self.signal_doc: list = []
        self.enum_doc: list[EnumDoc] = []
        self.const_doc: list[VarDoc] = []
        self.func_doc: list[FuncDoc] = []
        self.inner_class_doc: list[ClassDoc] = []

    def set_class_name(self, class_name: str):
        self.class_name = class_name

    def set_is_inner_class(self, value: bool):
        self.is_inner_class = value

    def set_extends(self, extends: str):
        self.extends = extends
