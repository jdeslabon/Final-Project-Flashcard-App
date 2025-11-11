# data/user_and_theme.py
import json, os

class AppData:
    def __init__(self):
        self.theme = "light"
        self.username = None
        self.accounts = []
        self.profile_data = {}
        self.load_data()

    def load_data(self):
        """Load saved user data and profiles from disk."""
        if os.path.exists("user_profiles.json"):
            with open("user_profiles.json", "r") as f:
                data = json.load(f)
            self.profile_data = data
            self.accounts = list(data.keys())

    def save_profile(self, username, info):
        """Save or update a user profile."""
        self.profile_data[username] = info
        self.accounts = list(self.profile_data.keys())
        with open("user_profiles.json", "w") as f:
            json.dump(self.profile_data, f, indent=4)

    def get_profile(self, username):
        """Get a user's profile info."""
        return self.profile_data.get(username, {})

    def delete_account(self, username):
        """Remove a user account from saved data."""
        if username in self.profile_data:
            del self.profile_data[username]
            self.accounts = list(self.profile_data.keys())
            with open("user_profiles.json", "w") as f:
                json.dump(self.profile_data, f, indent=4)