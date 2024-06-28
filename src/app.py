from control.settings import Settings


class Main:
    """
    Main entry point of the application
    """
    def __init__(self):
        """
        Constructor of the application
        """
        print("APP Started")
        self.settings = Settings()
        pass


if __name__ == '__main__':
    """
    Init program and starting class.
    """
    Main()
