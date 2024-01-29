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
        """The dictionary describing all the profiles found in .mlkgraphprofiles files.
        """

    # ----------------------
    #
    # Read the profile file.
    #
    # ----------------------
    def read_profiles(self):
        """Reads profiles from local folder and home folder .mlkgraphprofiles
        files and store them in self.profiles.

        Local folder file takes precedence over home folder file, overwriting
        any profile with the same name.
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

    # ----------------------
    #
    # Return a tuple with the include / exclude for a profile.
    # Raises an exception if the profile does no exists.
    #
    # ----------------------
    def get_profile(self, profile_name: str) -> tuple[list[str], list[str]]:
        if profile_name in self.profiles:
            return (
                self.profiles[profile_name]["include"],
                self.profiles[profile_name]["exclude"],
            )
        else:
            raise Exception(f"Profile {profile_name} not found")
