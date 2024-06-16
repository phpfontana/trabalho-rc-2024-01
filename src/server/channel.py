from typing import List
from shared.utils import to_lowercase_bytes


class Channel:
    class Options:
        def __init__(self):
            self.max_channel_name = 63

    def __init__(self, channel_name:bytearray):
        self.name = channel_name
        self.normalized_name = to_lowercase_bytes(channel_name)
        self.user_list: List = []
        self.options = self.Options()

    def get_nickname_list(self):
        nickname_list = []
        for user in self.user_list:
            nickname_list.append(user.nickname)
        return nickname_list

    def is_user_in_channel(self, target_user) -> bool:
        for user in self.user_list:
            if target_user == user:
                return True
        return False

    def is_valid_channel_name(self, channel_name: bytearray) -> bool:
        try:
            channel_name_str = channel_name.decode()
        except UnicodeError:
            return False
        if channel_name_str[0] == "#":
            if len(channel_name_str) <= self.options.max_channel_name:
                if self.__is_only_alphanum_or_underline(channel_name_str[1:]):
                    return True
        return False

    def __is_only_alphanum_or_underline(
        self, channel_name_without_first_letter: str
    ) -> bool:
        for char in channel_name_without_first_letter:
            if not (char.isalnum() or char == "_"):
                return False
        return True


        
