from swiper.error import ParseError


class Message:
    """Wrapper for a Slack API Message"""


    def __init__(self, message):
        for key in message.keys():
            self.__setattr__(key, message[key])


class Parser:
    """Parses a Slack API message"""


    def __init__(self, message):
        self.message = message
        self.command = None
        self.tokens = None
        self.user = None
        self.channel = None


    def parse(self):
        """Constructs a parse tree consisting of a message's
        parts, tokens, and command"""

        text = self.message.content
        parts = [part.strip() for part in text.split('@swiper')]

        # determine whether the message originated from
        # a channel or direct message
        # TODO support for direct messages
        channel = self.message.subtitle
        channel = channel.replace('#', '')
        dm = None

        # get parts of the message - DMs have one part and
        # channel messages have two parts
        if len(parts) == 1:
            self.user = self.message.subtitle
        elif len(parts) == 2:
            self.user, text = parts
            self.user = self.user.rstrip(':')
            text = text.lstrip()
        else:
            raise ParseError('message has invalid structure')

        # get tokens of the message
        tokens = [token.strip() for token in text.split(' ')]

        # edge case - combine tokens such as 'big house' that
        # should be together for certain commands
        skip, tokens_mod = False, []
        for i in range(len(tokens) - 1):
            a, b = tokens[i], tokens[i + 1]
            if skip:
                skip = False
                continue
            if (a.startswith('\'') or a.startswith('‘') or \
                a.startswith('\"') or a.startswith('“')) and \
                (b.endswith('\'') or b.endswith('’') or \
                b.endswith('\"') or b.endswith('”')):
                tokens_mod.append('{} {}'.format(a, b))
                skip = True
            else:
                tokens_mod.append(a)
        if not skip:
            tokens_mod.append(tokens[-1])
        tokens = tokens_mod[:]

        if len(tokens):
            self.command = tokens[0]
            if not self.command.startswith('/'):
                self.command = None
            self.tokens = tokens[1:]
        else:
            raise ParseError('message has no tokens')

        # build parse tree
        tree = {
            'command': self.command,
            'tokens': self.tokens,
            'user': self.user,
            'channel': channel,
            'dm': dm
        }

        return tree
