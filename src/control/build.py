from sys import exit
from os.path import isdir, isfile, join
from os import walk
from fnmatch import filter

from ruamel.yaml.comments import CommentedMap, CommentedSeq


class Build:
    """
    Reads the necessary data from the project and source files and generates the markdown documentation file(s) from it.

    Attributes:
        doc_conf_data: The deserialized settings for reading the sourcecode
        doc_conf_file: Path to the documentation config file
        gd_project: For information extracted from project.godot file
        script_files: A dictionary with information for all script files in the project and/or in the filelist_scan
            scan_list
        scene_files: A list for all scene files of the project

    Attributes: doc_conf_data attributes:
        doc_destination (str): Destination directory for the resulting documentation. Create if not exists
        rebuild_src_path (bool): Reproduces directories from src_path for doc_destination if True
        project_scan (bool): Scanning all files of a project if True
        project_scan_options (list[dict]): Mandatory if project_scan is True
        filelist_scan (bool): Scanning a manually created list if True, can be combined with project_scan to add more
            files to scan
        scan_list (list): List to be scanned if filelist_scan is True

    Attributes: doc_conf_data.project_scan_options attributes
        src_path (str): The base directory of the project to scan
        read_gd_project(bool): Creates a project documentation index if True
        scene2src_links (bool): Scans and documents if a script is linked to a scene

    Attributes: gd_project attributes:
        project_name (str): For the name of the godot project, as read from the project.godot file
        godot_version (str): For the godot version of the godot source code, as read from the project.godot file
        main_scene (str): For the data of the main (aka starting) scene, as read from the project.godot file
        autoload (list[dict]): Scenes that load at application start, if enabled

    Attributes: gd_project.main_scene attributes:
        scene_path (str): For the path to the main (aka starting) scene, as read from the project.godot file
        added_script (str): The script linked to the main scene, if any

    Attributes: gd_project.autoload list[dict] attributes:
        scene_path (str): For the path to the scene, as read from the project.godot file
        added_script (str): The script linked to the scene, if any
        enabled (bool): Is the autoload scene enabled?

    Attributes: script_files attributes:
        scene (str): Full path to the connected scene, if any
        docs (list): For elements from docstring reading

    Returns:
        Application_exit_code (int): Applications exits directly from this class on error. if anything is successful,
            returns None to the calling Main class. This gives the possibility for working with addons there after the
            creation of the documentation files (for example creating a full site including menus with mkdocs)
    """
    def __init__(self, doc_conf_data: CommentedMap, doc_conf_file: str):
        """
        Constructor of the class. Anything from reading project to building documentation sites is done from here.

        Args:
            doc_conf_data: The deserialized settings for reading the sourcecode
            doc_conf_file: Path to the documentation config file
        """
        self.doc_conf_data: CommentedMap = doc_conf_data
        self.doc_conf_file: str = doc_conf_file
        self.gd_project: dict = {
            "project_name": "",
            "godot_version": "",
            "main_scene": {
                "scene_path": "",
                "added_script": ""
            },
            "autoload": []
        }
        self.script_files: dict = {}
        self.scene_files: list = []
        self.check_doc_conf_data()
        print(f"Check of {self.doc_conf_file} configuration file finished, everything seems ok")
        if self.doc_conf_data["project_scan"]:
            self.collect_proj_files_info()
            if self.doc_conf_data["project_scan_options"]["scene2src_links"]:
                self.connect_scene_to_script()
            self.scan_project_scripts()
        print()
        print(self.script_files)
        print()
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
                    print("Godot project file analyzed")
        tmp_script_files = self.rec_find_files_with_ext(
            "gd",
            self.doc_conf_data["project_scan_options"]["src_path"]
        )
        tmp_script_files = [
            element.replace(self.doc_conf_data["project_scan_options"]["src_path"], "")
            for element in tmp_script_files
        ]
        for file in tmp_script_files:
            self.script_files[file] = {
                "scene": "",
                "docs": []
            }
        print("Project script files list created")
        if self.doc_conf_data["project_scan_options"]["scene2src_links"]:
            self.scene_files = self.rec_find_files_with_ext(
                "tscn",
                self.doc_conf_data["project_scan_options"]["src_path"]
            )
            self.scene_files = [
                element.replace(self.doc_conf_data["project_scan_options"]["src_path"], "")
                for element in self.scene_files
            ]
            print("Project scene files list created")

    @staticmethod
    def rec_find_files_with_ext(file_extension: str, search_directory: str) -> list:
        """
        Gathers a list of files with the given extension in the given directory

        Args:
            file_extension: The extension of the files to search for. Example: gd (and NOT *.gd)
            search_directory: The directory from which to scan for the files recursively

        Returns:
            List with the full path of the files found with the given extension, relative to the working directory
        """
        file_list: list = []
        for root, dir_names, filenames in walk(search_directory):
            for filename in filter(filenames, f"*.{file_extension}"):
                file_list.append(join(root, filename))
        return file_list

    def connect_scene_to_script(self):
        """
        Register scene connected to script where applicable
        """
        for scene in self.scene_files:
            fp_scene = self.doc_conf_data["project_scan_options"]["src_path"] + scene
            if isfile(fp_scene):
                try:
                    with open(fp_scene, "r") as file:
                        for line in file:
                            if 'ext_resource type="Script"' not in line:
                                continue
                            script_path = line.strip("[").strip("]")
                            script_path = script_path.replace(
                                'ext_resource type="Script" path="res://',
                                ""
                            )
                            script_path = script_path.split('"', 1)[0]
                            self.script_files[script_path]["scene"] = scene
                            break
                except Exception as e:
                    print(f"Skipping file {fp_scene}, reading failed with exception:")
                    print(e)

    def scan_project_scripts(self):
        """
        Initiates scans of docstrings for all scripts in the project
        """
        for script in self.script_files:
            self.script_scanner(script)

    def scan_filelist_scripts(self):
        """
        ToDo!
        """
        pass

    def script_scanner(self, script: str, from_project: bool = True):
        """
        Scans docstrings from script, registering docstring class, signal, enum, enum values, const, var, func, and
        inner class categories

        Members of inner classes are not scanned at this time. Eventually becomes a feature in a future version.

        Args:
            script: Path to the script to read from
            from_project: If True, the path of the script is relative to the project root (src_path)
        """
        scan_stage: str = ""
        class_doc: dict = {
            "class_name": "",
            "extends": "",
            "brief_description": "",
            "detail_description": "",
            "signal_doc": [],
            "enum_doc": [],  # todo: embed enum values docstrings into this list somehow
            "const_doc": [],
            "var_doc": [],
            "func_doc": [],
            "inner_class_doc": [],

        }
        if from_project:
            fp_script = self.doc_conf_data["project_scan_options"]["src_path"] + script
        else:
            fp_script = script
        try:
            with open(fp_script, "r") as file:
                for line in file:

                    pass
        except Exception as e:

            # todo: broader exception handling
            print(e)
            pass
