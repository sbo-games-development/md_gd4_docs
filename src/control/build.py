from sys import exit
from os.path import isdir, isfile
from ruamel.yaml.comments import CommentedMap, CommentedSeq


class Build:
    """
    Reads the necessary data from the project and source files and generates the markdown documentation file(s) from it.

    Args:
        doc_conf_data: The deserialized settings for reading the sourcecode

    Returns:
        Application_exit_code (int): Applications exits directly from this class on error. if anything is successful,
            returns None to the calling Main class. This gives the possibility for working with addons there after the
            creation of the documentation files (for example creating a full site including menus with mkdocs)
    """
    def __init__(self, doc_conf_data: dict, doc_conf_file: str):
        self.doc_conf_data = doc_conf_data
        self.doc_conf_file = doc_conf_file
        self.check_doc_conf_data()

    def check_doc_conf_data(self):
        """
        Checks if the configuration data are correct. Exits directly after printing error message if not.
        """
        print("Checking settings correctness before reading & building ...")
        # print(self.doc_conf_data)
        if "doc_destination" not in self.doc_conf_data or self.doc_conf_data["doc_destination"] == "" \
                or not isinstance(self.doc_conf_data["doc_destination"], str):
            print(f"doc_destination not set in {self.doc_conf_file}, empty or wrong type")
            exit(5)
        if "rebuild_src_path" not in self.doc_conf_data or not isinstance(self.doc_conf_data["rebuild_src_path"], bool):
            print(f"rebuild_src_path not set in {self.doc_conf_file} or wrong type")
            exit(5)
        if "project_scan" not in self.doc_conf_data or not isinstance(self.doc_conf_data["rebuild_src_path"], bool):
            print(f"project_scan not set in {self.doc_conf_file} or wrong type")
            exit(5)
        if self.doc_conf_data["project_scan"]:
            if "project_scan_options" not in self.doc_conf_data \
                    or not isinstance(self.doc_conf_data["project_scan_options"], CommentedMap):
                print(f"project_scan_options not set in {self.doc_conf_file}, wrong type or empty")
                print("project_scan_options are needed if project_scan is true")
                exit(5)
            if "src_path" not in self.doc_conf_data["project_scan_options"] \
                    or self.doc_conf_data["project_scan_options"]["src_path"] == ""\
                    or not isinstance(self.doc_conf_data["project_scan_options"]["src_path"], str):
                print(f"src_path wrong type or not set in project_scan_option in {self.doc_conf_file}")
                exit(5)
            if "read_gd_project" not in self.doc_conf_data["project_scan_options"] \
                    or not isinstance(self.doc_conf_data["project_scan_options"]["read_gd_project"], bool):
                print(f"read_gd_project wrong type or not set in project_scan_option in {self.doc_conf_file}")
                exit(5)
            if "scene2src_links" not in self.doc_conf_data["project_scan_options"] \
                    or not isinstance(self.doc_conf_data["project_scan_options"]["scene2src_links"], bool):
                print(f"scene2src_links wrong type or not set in project_scan_option in {self.doc_conf_file}")
                exit(5)
            if not isdir(self.doc_conf_data["project_scan_options"]["src_path"]):
                print(f"src_path in project_scan_options in {self.doc_conf_file} doesn't exist")
                exit(2)
        if "filelist_scan" not in self.doc_conf_data or not isinstance(self.doc_conf_data["filelist_scan"], bool):
            print(f"filelist_scan not set in {self.doc_conf_file} or wrong type")
            exit(5)
        if not self.doc_conf_data["project_scan"] and not self.doc_conf_data["filelist_scan"]:
            print(f"At least one of the options project_scan or filelist_scan needs to be set true, otherwise theres "
                  f"nothing to scan")
            exit(5)
        if self.doc_conf_data["filelist_scan"]:
            if "scan_list" not in self.doc_conf_data \
                    or not isinstance(self.doc_conf_data["scan_list"], CommentedSeq):
                print(f"scan_list not set in {self.doc_conf_file}, wrong type or empty")
                print("scan_list is needed if filelist_scan is true")
                exit(5)
            if len(self.doc_conf_data["scan_list"]) < 1:
                print(f"scan_list in {self.doc_conf_file} needs at least 1 file to scan, if file_list_scan is true")
                exit(5)
            for element in self.doc_conf_data["scan_list"]:
                if not isinstance(element, str) or not element.endswith(".gd"):
                    print(f"Element {str(element)} in scan_list in {self.doc_conf_file} can't be scanned, only .gd "
                          f"files are allowed")
                    exit(5)
                if not isfile(element):
                    print(f"Element {str(element)} in scan_list in {self.doc_conf_file} can't be scanned, file "
                          f"doesn't exist")
                    exit(2)
