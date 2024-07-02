from os.path import isfile
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


class Settings:
    """
    Class to handle the settings for reading the source.

    Attributes:
        doc_conf_file: The settings for reading the source are stored in this yaml file
        doc_conf_data: The deserialized settings for reading the sourcecode, also used as template at --init
        yaml: Object for loading and serializing yaml
    """
    def __init__(self):
        """
        Constructor of the class, defining class attributes.
        """
        self.doc_conf_file: str = "./md_gd4_docs.yml"
        self.doc_conf_data: [dict | CommentedMap] = {
            "doc_destination": "",
            "rebuild_src_path": True,
            "project_scan": True,
            "project_scan_options": {
                "src_path": "",
                "read_gd_project": True,
                "scene2src_links": True
            },
            "filelist_scan": False,
            "scan_list": [
                "./file1.gd",
                "./file2.gd"
            ]
        }
        self.yaml: YAML = YAML()
        print("Application settings initialized.")

    def init_settings(self) -> bool:
        """
        This method writes a configuration template for how to read the project / sourcecode, if it not already exists.

        Returns:
            Result of the operation, True if creating configuration file successfully
        """
        print("Initializing documentation settings ...")
        if isfile(self.doc_conf_file):
            print(f"Configuration file {self.doc_conf_file} already exists.")
            print("If you want start over again, you have to delete (after backup?) the file first")
            return False
        try:
            with open(self.doc_conf_file, "w") as file:
                self.yaml.dump(self.doc_conf_data, file)
                print(f"Documentation settings template {self.doc_conf_file} successfully created.")
                return True
        except Exception as e:
            print(f"Writing file {self.doc_conf_file} failed with Exception:")
            print(e)
            return False

    def load_settings(self) -> bool:
        """
        Loads the settings from the configuration file, if it exists, and serializes it into the doc_conf_data dict.

        Returns:
            True if loading and serializing is successful. Further checks of the correctness of the file are not done
                here, has to be done before reading the source at the build stage
        """
        print("Loading documentation settings ...")
        if not isfile(self.doc_conf_file):
            print(f"Configuration file {self.doc_conf_file} doesn't exist.")
            print("A settings template can be created with:")
            print("    md_gd4_docs --init")
            return False
        try:
            with open(self.doc_conf_file, "r") as file:
                self.doc_conf_data = self.yaml.load(file)
                if not self.doc_conf_data["doc_destination"].endswith("/"):
                    self.doc_conf_data["doc_destination"] = \
                        self.doc_conf_data["doc_destination"] + "/"
                if not self.doc_conf_data["project_scan_options"]["src_path"].endswith("/"):
                    self.doc_conf_data["project_scan_options"]["src_path"] = \
                        self.doc_conf_data["project_scan_options"]["src_path"] + "/"
                print(f"Documentation settings file {self.doc_conf_file} successfully loaded.")
                return True
        except Exception as e:
            print(f"Reading file {self.doc_conf_file} failed with Exception:")
            print(e)
            return False

    def get_settings(self) -> CommentedMap:
        """
        Get the settings dict.

        Returns:
            doc_conf_data: Deserialized settings object. Further checks of the correctness of this settings object is
                not done here, has to be done before reading the source at the build stage
        """
        return CommentedMap(self.doc_conf_data)
