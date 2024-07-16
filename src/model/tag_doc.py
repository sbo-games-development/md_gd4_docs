

class TagDoc:
    """
    Model class for holding documentation for tags
    """
    def __init__(self, tag_type: str, tutorial_url: str = "", tutorial_name: str = ""):
        """
        Constructor of the tag documentation model.

        Args:
            tag_type: Possible values are "@tutorial", "@experimental" or "@deprecated"
            tutorial_url: Only used for @tutorial tag
            tutorial_name: Only used for @tutorial tag

        Raises:
            Exception: If tag_type invalid
        """
        self.tag_type = tag_type
        self.tutorial_url = tutorial_url
        self.tutorial_name = tutorial_name
        if self.tag_type != "@tutorial" \
                or self.tag_type != "@experimental" \
                or self.tag_type != "@deprecated":
            raise Exception('Only "@tutorial", "@experimental" or "@deprecated" are valid tag types')
