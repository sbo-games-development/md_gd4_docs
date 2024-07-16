from src.model.tag_doc import TagDoc


class SignalDoc:
    """
    Model class for holding documentation for signals.
    """
    def __init__(self, name: str, description: str, tags: list[TagDoc] = None):
        """
        Constructor of the signal documentation model.

        Args:
            name: Name of the signal
            description: Description of the signal
            tags: Tag(s) of the signal, if any
        """
        self.name: str = name
        if tags is None:
            self.tags: list[TagDoc] = []
        else:
            self.tags: list[TagDoc] = tags
        self.description: str = description
