class IrcCodes():
    class Registration():
        RPL_WELCOME = b"001"

    class Nick():
        ERR_NICKNAMEINUSE = b"433"
        ERR_ERRONEUSNICKNAME = b"432"

    class Motd():
        RPL_MOTDSTART = b"375"
        RPL_MOTD = b"372"
        RPL_ENDOFMOTD = b"376"

    class Join():
        ERR_NOSUCHCHANNEL = b"403"

    class Names:
        RPL_NAMREPLY = b"353"
        RPL_ENDOFNAMES = b"366"

    class Part():
        ERR_NOTONCHANNEL = b"442"
