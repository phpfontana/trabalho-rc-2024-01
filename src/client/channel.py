from typing import List
from client.user import User
from client.errors import InvalidChannelNameError

class Channel:
    class Options:
        def __init__(self):
            self.max_channel_name = 63

    def __init__(self, channel_name:str):
        self.options = self.Options()
        self.name = self.set_channel_name(channel_name)
        self.users: List[User] = []

    def set_channel_name(self, channel_name:str):
        if self.__is_valid_channel_name(channel_name):
            self.name = channel_name
        else:
            raise InvalidChannelNameError(channel_name)

    def get_nickname_list(self):
        nickname_list = []
        for user in self.users:
            nickname_list.append(user.nickname)
        return nickname_list

    def is_user_in_channel(self, target_user:User) -> bool:
        for user in self.users:
            if target_user == user:
                return True
        return False

    def __is_valid_channel_name(self, channel_name: str) -> bool:
        if channel_name[0] == "#":
            if len(channel_name) <= self.options.max_channel_name:
                if self.__is_only_alphanum_or_underline(channel_name[1:]):
                    return True
        return False

    def __is_only_alphanum_or_underline(
        self, channel_name_without_first_letter: str
    ) -> bool:
        for char in channel_name_without_first_letter:
            if not (char.isalnum() or char == "_"):
                return False
        return True


        
