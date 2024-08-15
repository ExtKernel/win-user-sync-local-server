import subprocess
from concurrent.futures import ThreadPoolExecutor

from ..users.user_scripts import User, deserialize_users


def skip_header(output, lines_to_skip=1):
    """
    Skips a specified number of lines at the beginning of the output.

    Args:
        output (str): The output string.
        lines_to_skip (int): The number of lines to skip.

    Returns:
        str: The output string with the specified number of lines skipped.
    """
    return '\n'.join(output.split('\n')[lines_to_skip:])

class Usergroup:
    """
    Represents a user group with a name, description, and users.

    Attributes:
        name (str): The name of the user group.
        description (str): The description of the user group.
        users (list): A list of User objects representing users in the group.
    """
    def __init__(self, name, description=None, users=None):
        self.name = name
        self.description = description
        self.users = users or []

    def serialize(self):
        """
        Serializes the user group object to a dictionary.

        Returns:
            dict: A dictionary representation of the user group.
        """
        return {
            'name': self.name,
            'description': self.description,
            'users': [user.serialize() for user in self.users]
        }

    def __str__(self):
        """
        Returns a string representation of the user group object.

        Returns:
            str: The string representation of the user group.
        """
        return f"Usergroup(name={self.name}, description={self.description}, users={[str(user) for user in self.users]})"


class UsergroupEditor:
    """
    Manages user group creation, renaming, adding/removing users, and deletion.

    Attributes:
        powershell_path (str): The path to the PowerShell executable.
    """
    def __init__(self, powershell_path):
        self.powershell_path = powershell_path

    def _run_powershell_command(self, command):
        """
        Executes a PowerShell command using subprocess.

        Args:
            command (str): The PowerShell command to execute.

        Returns:
            str: The stdout output from the command.
        """
        result = subprocess.run(
            [self.powershell_path, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command],
            capture_output=True, text=True
        )
        return result.stdout.strip()

    def add(self, usergroup_name, description=None, users=None):
        """
        Creates a new user group.

        Args:
            usergroup_name (str): The name of the new user group.
            description (str, optional): The description of the new user group. Defaults to None.
            users (list, optional): A list of usernames to add to the new user group. Defaults to None.
        """
        command = f'New-LocalGroup -Name "{usergroup_name}"'
        if description:
            command += f' -Description "{description}"'
        self._run_powershell_command(command)
        if users:
            self.add_users(usergroup_name, users)

    def rename(self, old_usergroup_name, new_usergroup_name):
        """
        Renames an existing user group.

        Args:
            old_usergroup_name (str): The current name of the user group.
            new_usergroup_name (str): The new name for the user group.
        """
        self._run_powershell_command(
            f'Rename-LocalGroup -Name "{old_usergroup_name}" -NewName "{new_usergroup_name}"'
        )

    def remove_user(self, usergroup_name, username):
        """
        Removes users from an existing user group.

        Args:
            usergroup_name (str): The name of the user group.
            username (str): The username of the user to remove from the user group.
        """
        self._run_powershell_command(
            f'Remove-LocalGroupMember -Group "{usergroup_name}" -Member "{username}"'
        )

    def add_users(self, usergroup_name, users):
        """
        Adds users to an existing user group concurrently using ThreadPoolExecutor.

        Args:
            usergroup_name (str): The name of the user group.
            users (list): A list of usernames to add to the user group.
        """
        commands = [
            f'Add-LocalGroupMember -Group "{usergroup_name}" -Member "{user.username}"'
            for user in deserialize_users(users)
        ]
        with ThreadPoolExecutor() as executor:
            executor.map(self._run_powershell_command, commands)

    def delete(self, usergroup_name):
        """
        Deletes an existing user group.

        Args:
            usergroup_name (str): The name of the user group to delete.
        """
        self._run_powershell_command(f'Remove-LocalGroup -Name "{usergroup_name}"')


class UsergroupRetriever:
    """
    Retrieves user group information.

    Attributes:
        powershell_path (str): The path to the PowerShell executable.
    """
    def __init__(self, powershell_path):
        self.powershell_path = powershell_path

    def _run_powershell_command(self, command):
        """
        Executes a PowerShell command using subprocess.

        Args:
            command (str): The PowerShell command to execute.

        Returns:
            list: A list of output lines from the command.
        """
        result = subprocess.run(
            [self.powershell_path, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command],
            capture_output=True, text=True
        )
        return skip_header(result.stdout.strip(), lines_to_skip=2).split('\n')

    def get_all(self):
        """
        Retrieves all local user groups.

        Returns:
            list: A list of Usergroup objects representing all local user groups.
        """
        name_column = self.get_names()
        with ThreadPoolExecutor() as executor:
            return list(executor.map(self.get, (name.strip() for name in name_column)))

    def get(self, name):
        """
        Retrieves a specific user group by name.

        Args:
            name (str): The name of the user group to retrieve.

        Returns:
            Usergroup: A Usergroup object representing the retrieved user group.
        """
        name = self.get_names(name)[0].strip()
        descriptions = self.get_descriptions(name)
        description = descriptions[0] if descriptions else None
        users = self.get_users(name)
        return Usergroup(name, description, users)

    def get_names(self, name=None):
        """
        Retrieves names of all local user groups or a specific user group.

        Args:
            name (str, optional): The name of the user group to retrieve. Defaults to None (all user groups).

        Returns:
            list: A list of user group names.
        """
        command = f'Get-LocalGroup "{name}" | Format-Table -Property Name' if name else 'Get-LocalGroup | Format-Table -Property Name'
        return self._run_powershell_command(command)

    def get_descriptions(self, name=''):
        """
        Retrieves descriptions of all local user groups or a specific user group.

        Args:
            name (str, optional): The name of the user group to retrieve. Defaults to '' (all user groups).

        Returns:
            list: A list of user group descriptions.
        """
        command = f'Get-LocalGroup "{name}" | Format-Table -Property Description' if name else 'Get-LocalGroup | Format-Table -Property Description'
        return self._run_powershell_command(command)

    def get_users(self, name):
        """
        Retrieves users of a specific local user group.

        Args:
            name (str): The name of the user group to retrieve users from.

        Returns:
            list: A list of User objects representing users in the user group.
        """
        users = self._run_powershell_command(f'Get-LocalGroupMember -Name "{name}" | Format-Table -Property Name')
        return [User(user.strip().split('\\')[1]) for user in users if user]

    def get_included_users(self, group_name, users):
        """
        Retrieves users from a list that are included in a specific local user group.

        Args:
            group_name (str): The name of the user group to check against.
            users (list): A list of User objects representing users to check.

        Returns:
            list: A list of User objects that are included in the user group.
        """
        usergroup_users = self.get_users(group_name)
        user_names = {user.username for user in usergroup_users}
        return [user for user in deserialize_users(users) if user.username in user_names]
