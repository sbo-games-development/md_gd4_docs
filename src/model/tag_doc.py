

class TagDoc:
    """
    Model class for holding documentation for tags
    """
    def __init__(self, tag_type: str, tutorial_url: str = "", tutorial_name: str = ""):
        """
        Constructor of the tag documentation model.

        Args:
            tag_type: Possible values are @tutorial, @experimental or @deprecated
            tutorial_url: Only used for @tutorial tag
            tutorial_name: Only used for @tutorial tag
        """
        self.tag_type = tag_type
        self.tutorial_url = tutorial_url
        self.tutorial_name = tutorial_name
