from src.model.signal_doc import SignalDoc
from src.model.enum_doc import EnumDoc
from src.model.var_doc import VarDoc
from src.model.func_doc import FuncDoc
from src.model.tag_doc import TagDoc


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

        Raises:
            Exception: If inner class True without or with invalid class_name
        """
        self.file_name: str = file_name
        self.class_name: str = class_name
        self.is_inner_class: bool = inner_class
        self.extends: str = ""
        self.tags: list[TagDoc] = []
        self.brief_description: str = ""
        self.detail_description: str = ""
        self.signal_docs: list[SignalDoc] = []
        self.enum_docs: list[EnumDoc] = []
        self.const_docs: list[VarDoc] = []
        self.var_docs: list[VarDoc] = []
        self.func_docs: list[FuncDoc] = []
        self.inner_class_docs: list[ClassDoc] = []
        if self.inner_class_docs and (self.class_name == "not exposed" or " " in self.class_name):
            raise Exception("Inner classes needs to be named, no spaces allowed")

    def set_class_name(self, class_name: str):
        self.class_name = class_name

    def set_is_inner_class(self, value: bool):
        self.is_inner_class = value

    def set_extends(self, extends: str):
        self.extends = extends

    def add_signal(self, name: str, description: str, tags: list[TagDoc] = None):
        """
        Adds a signal description item to the doc

        Args:
            name: Name of the signal
            description: Description of the signal
            tags: Tag(s) of the signal, if any
        """
        self.signal_docs.append(SignalDoc(name, description, tags))

    def add_enum(self):
        """
        todo!
        """

        pass

    def add_attribute(
            self,
            name: str,
            data_type: str,
            description: str,
            value=None,
            var_type: str = "var",
            tags: list[TagDoc] = None
    ):
        """
        Adds an attribute (var, const) item to the doc

        Args:
            name: Name of the Attribute
            data_type: Data type of the attribute
            description: Description of the Attribute
            value: Value of the attribute, if any. Type of the attribute should match data_type
            var_type: Could be "const", "export_var", "var" or "onready_var"
            tags: Tag(s) of the signal, if any
        """
        if var_type == "const":
            self.const_docs.append(VarDoc(name, data_type, description, value, var_type, tags))
        else:
            self.var_docs.append(VarDoc(name, data_type, description, value, var_type, tags))
