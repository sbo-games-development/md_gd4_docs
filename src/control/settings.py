from ruamel.yaml import YAML
import sys


class Settings:
    """
    Class to handle the settings for reading the source.

    Attributes:
        doc_conf_file: The settings for reading the source are stored in this yaml file
        doc_conf_data: The deserialized settings for reading the source
        yaml: Object for loading and serializing yaml
        con_file_obj: object for opening and reading the doc_conf_file
    """
    def __init__(self):
        """
        Constructor of the class, defining class attributes.
        """
        self.doc_conf_file: str = "./md_gd4_docs.yml"
        self.doc_conf_data: dict = {}
        self.yaml: YAML = YAML()
        self.con_file_obj: _io.TextIOWrapper = None
        print("Settings initialized")
