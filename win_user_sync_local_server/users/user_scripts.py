import subprocess

from config.settings.base import BASE_DIR


def deserialize_users(serialized_users):
    return [User(user['username']) for user in serialized_users]

def run_powershell_command(command):
    """
    Executes a PowerShell command using subprocess.

    Args:
        command (list): The PowerShell command to execute.

    Returns:
        str: The stdout output from the command.
    """
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()


def skip_header(output, lines_to_skip=1):
    """
    Skips a specified number of lines at the beginning of the output.

    Args:
        output (str): The output string.
        lines_to_skip (int): The number of lines to skip.

    Returns:
        str: The output string with the specified number of lines skipped.
    """
    lines = output.split('\n')
    return '\n'.join(lines[lines_to_skip:])


class User:
    """
    Represents a user with a name.

    Attributes:
        username (str): The name of the user.
    """
    def __init__(self, username):
        self.username = username

    def serialize(self):
        """
        Serializes the user object to a dictionary.

        Returns:
            dict: A dictionary representation of the user.
        """
        return {'username': self.username}

    def __str__(self):
        """
        Returns a string representation of the user object.

        Returns:
            str: The string representation of the user.
        """
        return f"User(username={self.username})"


class UserEditor:
    """
    Manages user creation, password editing, enabling, disabling, and deletion.

    Attributes:
        powershell_path (str): The path to the PowerShell executable.
    """
    def __init__(self, powershell_path):
        self.powershell_path = powershell_path

    def add(self, username, password):
        """
        Adds a new user.

        Args:
            username (str): The username of the new user.
            password (str): The password for the new user.

        Returns:
            str: The output from the PowerShell command.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', f'{BASE_DIR}/scripts/create-user.ps1 "{username}" "{password}"'
        ]
        output = run_powershell_command(command)
        return skip_header(output, lines_to_skip=2).replace("True", "").strip()

    def edit_password(self, username, password):
        """
        Edits the password for an existing user.

        Args:
            username (str): The username of the user.
            password (str): The new password for the user.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', f'{BASE_DIR}/scripts/edit-user-password.ps1 "{username}" "{password}"'
        ]
        run_powershell_command(command)

    def disable(self, username):
        """
        Disables an existing user.

        Args:
            username (str): The username of the user to disable.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', f'Disable-LocalUser -Name "{username}"'
        ]
        run_powershell_command(command)

    def enable(self, username):
        """
        Enables an existing user.

        Args:
            username (str): The username of the user to enable.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', f'Enable-LocalUser -Name "{username}"'
        ]
        run_powershell_command(command)

    def delete(self, username):
        """
        Deletes an existing user.

        Args:
            username (str): The username of the user to delete.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', f'Remove-LocalUser -Name "{username}"'
        ]
        run_powershell_command(command)


class UserRetriever:
    """
    Retrieves user information.

    Attributes:
        powershell_path (str): The path to the PowerShell executable.
    """
    def __init__(self, powershell_path):
        self.powershell_path = powershell_path

    def get_all(self):
        """
        Retrieves all local users.

        Returns:
            list: A list of User objects representing all local users.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', 'Get-LocalUser | Format-Table -Property Name'
        ]
        output = run_powershell_command(command)
        usernames = self.extract_usernames(skip_header(output, lines_to_skip=2))
        return [User(username) for username in usernames]

    def get(self, username):
        """
        Retrieves a specific user by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: A User object representing the retrieved user.
        """
        command = [
            self.powershell_path,
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', f'Get-LocalUser -Name "{username}" | Format-Table -Property Name'
        ]
        output = run_powershell_command(command)
        username = self.extract_usernames(skip_header(output, lines_to_skip=2))[0].strip()
        return User(username)

    def extract_usernames(self, users_output):
        """
        Extracts usernames from the command output.

        Args:
            users_output (str): The output from the command containing user information.

        Returns:
            list: A list of usernames.
        """
        return [line.split()[0] for line in users_output.splitlines()]
