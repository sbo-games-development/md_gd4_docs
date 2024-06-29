from sys import exit


class Build:
    """
    Reads the necessary data from the project and source files and generates the markdown documentation file(s) from it.

    Args:
        doc_conf_data: The deserialized settings for reading the sourcecode
    """
    def __init__(self, doc_conf_data: dict):
        print("Checking settings correctness before reading & building ...")
        pass
