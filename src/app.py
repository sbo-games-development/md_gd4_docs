import argparse
from sys import exit

from control.settings import Settings
from control.build import Build


class Main:
    """
    Main entry point of the application

    Attributes:
        version: Version of the application, also shown in the help

    Returns:
        Application_exit_code (int): 0 = success | 2 = argument parsing error | 5 = input/output error | and more?
    """
    def __init__(self):
        """
        Constructor of the applications Main class.

        Either initializes the settings or build markdown files as configured in settings.

        Attributes:
            settings (Settings): Local class instance to handle the settings for reading the source
            args (argparse.Namespace): Local parsed command line arguments, either args.init or args.build is True after
                the parsing was successful
            result (bool): Local var, set to False if any error occurs
            doc_settings (dict): Local var, deserialized settings for reading the sourcecode
        """
        self.version: str = "0.1.0"
        args: argparse.Namespace = self.arg_parse_init()
        settings: Settings = Settings()
        result: bool = True
        doc_settings: dict = {}
        if args.init:
            result = settings.init_settings()
        elif args.build:
            result = settings.load_settings()
            if result:
                doc_settings = settings.get_settings()
                if doc_settings:
                    Build(doc_settings)
        else:
            print("Something went very wrong ...")
            result = False
        if result:
            exit(0)
        else:
            exit(5)

    def arg_parse_init(self):
        """
        Parses and returns the command line arguments.

        Sets init (-i/--init) or build (-b/--build) to True, shows the help (-h/--help) or the version (-v/--version).
        If none of the former applies, an error message wil be displayed.
        """
        parser = argparse.ArgumentParser(
            prog="md_gd4_docs",
            description="Create Markdown documentation files automatically from Godot 4 projects/docstrings",
            epilog="For a full user documentation, visit https://..."  # todo: insert address for user manual
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-i", "--init", action="store_true",
            help="Creates a settings template (./md_gd4_docs.yml)"
        )
        group.add_argument(
            "-b", "--build", action="store_true",
            help="Creates the documentation files following the settings file ./md_gd4_docs.yml"
        )
        group.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {self.version}",
            help="Shows the version of the application"
        )
        return parser.parse_args()


if __name__ == '__main__':
    """
    Init program and starting class.
    """
    Main()
