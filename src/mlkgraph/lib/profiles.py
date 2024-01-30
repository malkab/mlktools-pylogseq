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
        self.profiles: dict = {}
        """The dictionary describing all the profiles found in .mlkgraphprofiles files.
        """

        self.root: str = ""
        """The root path to test the globs against."""

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
    def get_profile(self, profile_name: str) -> tuple[str, list[str], list[str]]:
        if profile_name in self.profiles:
            # Check if the profile has a root
            if "root" not in self.profiles[profile_name]:
                raise Exception(f"Profile {profile_name} does not have a root")

            return (
                # The root
                self.profiles[profile_name]["root"],
                # include if there is an include key and the key has list items
                self.profiles[profile_name]["include"]
                if "include" in self.profiles[profile_name]
                and self.profiles[profile_name]["include"] is not None
                else [],
                # exclude if there is an exclude key and the key has list items
                self.profiles[profile_name]["exclude"]
                if "exclude" in self.profiles[profile_name]
                and self.profiles[profile_name]["exclude"] is not None
                else [],
            )

        else:
            raise Exception(f"Profile {profile_name} not found")
