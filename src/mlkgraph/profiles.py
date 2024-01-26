import os
import yaml


# TODO: documentar


# ----------------------
#
# Read profiles from file.
#
# ----------------------
class Profiles:
    # ----------------------
    #
    # Initializator.
    #
    # ----------------------
    def __init__(self):
        """Initializes the profiles object."""
        self.profiles = {}

    # ----------------------
    #
    # Read the profile file.
    #
    # ----------------------
    def read_profiles(self):
        """Reads profiles from a file.

        Args:
            profiles_file (str): The path to the profiles file.

        Returns:
            dict[str, dict[str, Any]]: A dictionary with the profiles.
        """

        # Try to find the file in the home folder
        home_folder = os.path.expanduser("~")

        # Try to find the file in the current folder
        try:
            with open(os.path.join(home_folder, ".mlkgraphprofiles"), "r") as f:
                self.profiles = {**yaml.safe_load(f.read())}
        except Exception:
            pass

        # Try to find the file in the current folder (supersedes the home folder)
        current_folder: str = os.getcwd()

        try:
            with open(os.path.join(current_folder, ".mlkgraphprofiles"), "r") as f:
                self.profiles = {**self.profiles, **yaml.safe_load(f.read())}
        except Exception:
            pass

        # If profiles is empty, raise an exception
        if self.profiles == {}:
            raise Exception(
                "No profiles file .mlkgraphprofiles found in current or home folders."
            )
