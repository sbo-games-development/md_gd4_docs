from sys import exit
from os.path import isdir, isfile
from ruamel.yaml.comments import CommentedMap, CommentedSeq


class Build:
    """
    Reads the necessary data from the project and source files and generates the markdown documentation file(s) from it.

    Attributes:
        doc_conf_data: The deserialized settings for reading the sourcecode
        doc_conf_file: Path to the documentation config file
        gd_project: For information extracted from project.godot file
        script_files: A list with information for all script files in the project and/or in the filelist_scan scan_list
        scene_files: A list for all scene files of the project

    Returns:
        Application_exit_code (int): Applications exits directly from this class on error. if anything is successful,
            returns None to the calling Main class. This gives the possibility for working with addons there after the
            creation of the documentation files (for example creating a full site including menus with mkdocs)
    """
    def __init__(self, doc_conf_data: CommentedMap, doc_conf_file: str):
        """
        Constructor of the class. Anything from reading project to building documentation sites is directly done here.

        Args:
            doc_conf_data: The deserialized settings for reading the sourcecode
            doc_conf_file: Path to the documentation config file
        """
        self.doc_conf_data: CommentedMap = doc_conf_data
        self.doc_conf_file = doc_conf_file
        self.gd_project: dict = {
            "project_name": "",
            "godot_version": "",
            "main_scene": {
                "scene_path": "",
                "added_script": ""
            },
            "autoload": []
        }
        self.script_files: list = []
        self.scene_files: list = []
        self.check_doc_conf_data()
        print(f"Check of {self.doc_conf_file} configuration file finished, everything seems ok")
        if self.doc_conf_data["project_scan"]:
            self.collect_proj_files_info()
        #

    def check_doc_conf_data(self):
        """
        Checks if the configuration data are correct. Exits directly after printing error message if not.
        """
        # todo: point to according chapter/subsite in error msgs urls?
        print("Checking settings correctness before reading & building ...")
        # print(self.doc_conf_data)
        if "doc_destination" not in self.doc_conf_data or self.doc_conf_data["doc_destination"] == "" \
                or not isinstance(self.doc_conf_data["doc_destination"], str):
            print(f"doc_destination not set in {self.doc_conf_file}, empty or wrong type")
            print()
            print("For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/")
            exit(5)
        if "rebuild_src_path" not in self.doc_conf_data or not isinstance(self.doc_conf_data["rebuild_src_path"], bool):
            print(f"rebuild_src_path not set in {self.doc_conf_file} or wrong type")
            exit(5)
        if "project_scan" not in self.doc_conf_data or not isinstance(self.doc_conf_data["rebuild_src_path"], bool):
            print(f"project_scan not set in {self.doc_conf_file} or wrong type")
            print()
            print("For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/")
            exit(5)
        if self.doc_conf_data["project_scan"]:
            if "project_scan_options" not in self.doc_conf_data \
                    or not isinstance(self.doc_conf_data["project_scan_options"], CommentedMap):
                print(f"project_scan_options not set in {self.doc_conf_file}, wrong type or empty")
                print("project_scan_options are needed if project_scan is true")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(5)
            if "src_path" not in self.doc_conf_data["project_scan_options"] \
                    or self.doc_conf_data["project_scan_options"]["src_path"] == ""\
                    or not isinstance(self.doc_conf_data["project_scan_options"]["src_path"], str):
                print(f"src_path wrong type or not set in project_scan_option in {self.doc_conf_file}")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/")
                exit(5)
            if self.doc_conf_data["project_scan_options"]["src_path"] == self.doc_conf_data["doc_destination"]:
                print(f"Conflicting options: src_path in project_scan_options can't be the same as doc_destination in "
                      f"{self.doc_conf_file} settings file")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(5)
            if "read_gd_project" not in self.doc_conf_data["project_scan_options"] \
                    or not isinstance(self.doc_conf_data["project_scan_options"]["read_gd_project"], bool):
                print(f"read_gd_project wrong type or not set in project_scan_option in {self.doc_conf_file}")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(5)
            if "scene2src_links" not in self.doc_conf_data["project_scan_options"] \
                    or not isinstance(self.doc_conf_data["project_scan_options"]["scene2src_links"], bool):
                print(f"scene2src_links wrong type or not set in project_scan_option in {self.doc_conf_file}")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(5)
            if not isdir(self.doc_conf_data["project_scan_options"]["src_path"]):
                print(f"src_path in project_scan_options in {self.doc_conf_file} doesn't exist")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(2)
        if "filelist_scan" not in self.doc_conf_data or not isinstance(self.doc_conf_data["filelist_scan"], bool):
            print(f"filelist_scan not set in {self.doc_conf_file} or wrong type")
            print()
            print("For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/")
            exit(5)
        if not self.doc_conf_data["project_scan"] and not self.doc_conf_data["filelist_scan"]:
            print(f"At least one of the options project_scan or filelist_scan needs to be set true, otherwise theres "
                  f"nothing to scan")
            print()
            print("For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/")
            exit(5)
        if self.doc_conf_data["filelist_scan"]:
            if "scan_list" not in self.doc_conf_data \
                    or not isinstance(self.doc_conf_data["scan_list"], CommentedSeq):
                print(f"scan_list not set in {self.doc_conf_file}, wrong type or empty")
                print("scan_list is needed if filelist_scan is true")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(5)
            if len(self.doc_conf_data["scan_list"]) < 1:
                print(f"scan_list in {self.doc_conf_file} needs at least 1 file to scan, if file_list_scan is true")
                print()
                print(
                    "For a full user documentation, visit https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                )
                exit(5)
            for element in self.doc_conf_data["scan_list"]:
                if not isinstance(element, str) or not element.endswith(".gd"):
                    print(f"Element {str(element)} in scan_list in {self.doc_conf_file} can't be scanned, only .gd "
                          f"files are allowed")
                    print()
                    print(
                        "For a full user documentation, visit "
                        "https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                    )
                    exit(5)
                if not isfile(element):
                    print(f"Element {str(element)} in scan_list in {self.doc_conf_file} can't be scanned, file "
                          f"doesn't exist")
                    print()
                    print(
                        "For a full user documentation, visit "
                        "https://sbo-games-development.github.io/md_gd4_docs/userdoc/"
                    )
                    exit(2)

    def collect_proj_files_info(self):
        """
        Recursively gathering *.gd files from the project.

        Additionally, reads project.godot file if read_gd_project is true, and gathers *.scene files recursively if
        scene2src_links is true, to link them to the correspondant .gd script source files
        """
        print("Scanning godot project ...")
        if self.doc_conf_data["project_scan_options"]["read_gd_project"]:
            gd_proj_file = self.doc_conf_data["project_scan_options"]["src_path"] + "/project.godot"
            if not isfile(gd_proj_file):
                print(
                    f"Warning: File '{gd_proj_file}' not found, skipping project index"
                )
            else:
                try:
                    with open(gd_proj_file, "r") as file:
                        section = ""
                        for line in file:
                            line = line.strip()
                            if line.startswith(";"):
                                continue
                            if line.startswith("[") and line.endswith("]"):
                                section = line.strip("[").strip("]")
                            if "config/name=" in line:
                                project_name = line.replace("config/name=", "").strip('"')
                                self.gd_project["project_name"] = project_name
                                continue
                            if "run/main_scene=" in line:
                                main_scene = line.replace("run/main_scene=", "").strip('"')
                                main_scene = main_scene.replace("res://", "")
                                self.gd_project["main_scene"]["scene_path"] = main_scene
                                continue
                            if "config/features=PackedStringArray" in line:
                                godot_version = line.replace(
                                    "config/features=PackedStringArray", ""
                                ).strip("(").strip(")")
                                godot_version = godot_version.replace('"', "")
                                self.gd_project["godot_version"] = godot_version
                                continue
                            if section == "autoload":
                                if "=" in line:
                                    line = line.split("=", 1)
                                    scene_name = line[0]
                                    scene_path = line[1]
                                    scene_path = scene_path.replace("res://", "").strip('"')
                                    scene_autoload_enabled = True if scene_path.startswith("*") else False
                                    scene_path = scene_path.strip("*")
                                    self.gd_project["autoload"].append({
                                        "scene_path": scene_path,
                                        "scene_name": scene_name,
                                        "enabled": scene_autoload_enabled
                                    })
                except Exception as e:
                    print(f"Skipping project index, reading {gd_proj_file} failed with Exception:")
                    print(e)
                    self.gd_project: dict = {
                        "project_name": "",
                        "godot_version": "",
                        "main_scene": ""
                    }
                else:
                    print(self.gd_project)
        # find all *.gd script files in the project

        # find all *.scene script files in the project, if scene2src_links true
