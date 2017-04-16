import os
import random
import urllib.request
from abc import ABC, abstractmethod


class Command(ABC):


    def __init__(self, client, config, tree, read, write):
        self.client = client
        self.config = config
        self.tree = tree
        self.read = read
        self.write = write


    def get_channel_id(self, channel):
        return self.config.CHANNELS[channel]


    def get_user_id(self, user):
        return self.config.USERS[user]


    @abstractmethod
    def sanitize(self):
        pass


    @abstractmethod
    def execute(self):
        pass


class Help(Command):


    def __init__(self, client, config, tree, read, write):
        super().__init__(client, config, tree, read, write)

        self.user_id = self.get_user_id(self.tree['user'])
        self.channel_id = self.get_channel_id(self.write)


    def sanitize(self):
        return True


    def post(self):
        # construct repsonse - @user_id: <msg>
        response = 'Hi <@{}>, here are my commands!\n'.format(
            self.user_id
        )

        # concatenate the list of swiper's commands to
        # the base response
        commands = [
            '/help`: Displays Swiper\'s commands',
            '/announce <message>`: Send an important message to <#{}>'.format(
                self.get_channel_id('announcements')
            ),
            '/poll <opt 1> <opt 2>`: Create a poll with up to 10 options',
            '/roast @<user>`: Roasts a user in this team',
            '/compliment @<user>`: Compliments a user in this team',
            '/meme`: Posts a meme from Imgur'
        ]
        for command in commands:
            response += '`@swiper ' + command + '\n'

        self.client.api_call(
            'chat.postMessage',
            channel=self.channel_id,
            text=response,
            as_user=True
        )


    def execute(self):
        self.post()


class Announcement(Command):


    def __init__(self, client, config, tree, read, write):
        super().__init__(client, config, tree, read, write)

        self.user_id = self.get_user_id(self.tree['user'])
        self.read_channel_id = self.get_channel_id(self.read)
        self.write_channel_id = self.get_channel_id(self.write)


    def sanitize(self):
        if len(self.tree['tokens']) == 0:
            # can't make announcement if there are no
            # tokens in message, so post error
            response = 'Sorry <@{}>, you must include'.format(
                self.user_id
            ) + ' a message with your announcement!'

            self.client.api_call(
                'chat.postMessage',
                channel=self.read_channel_id,
                text=response,
                as_user=True
            )

            return False
        return True


    def post_announcement(self):
        text = ' '.join(self.tree['tokens'])

        # construct response - @user_id: <msg>
        # note: user_id is found by looking up the
        # Slack ID given to each user in the team
        response = '<@{}>: {}'.format(
            self.user_id,
            text
        )

        self.client.api_call(
            'chat.postMessage',
            channel=self.write_channel_id,
            text=response,
            as_user=True
        )


    def post_confirmation(self):
        # construct response - @channel @user_id: <msg>
        response = '<!channel> <@{}> made an announcement!'.format(
            self.user_id
        )

        self.client.api_call(
            'chat.postMessage',
            channel=self.read_channel_id,
            text=response,
            as_user=True
        )


    def execute(self):
        if self.sanitize():
            self.post_announcement()
            self.post_confirmation()


class Poll(Command):


    def __init__(self, client, config, tree, read, write):
        super().__init__(client, config, tree, read, write)

        self.user_id = self.get_user_id(self.tree['user'])
        self.channel_id = self.get_channel_id(self.read)


    def sanitize(self):
        if len(self.tree['tokens']) == 0:
            # can't make a poll if there are no
            # options in message, so post error
            response = 'Sorry <@{}>, you must include'.format(
                self.user_id
            ) + ' at least one option for your poll!'

            self.client.api_call(
                'chat.postMessage',
                channel=self.channel_id,
                text=response,
                as_user=True
            )

            return False
        return True


    def post(self):
        emojis = [':one:', ':two:', ':three:', ':four:', ':five:',
                    ':six:', ':seven:', ':eight:', ':nine:', ':ten:']
        tokens = self.tree['tokens']

        # construct response - poll with up to ten options,
        # which originates from the first ten tokens
        response = '<!channel> <@{}> created a poll:\n'.format(
            self.user_id
        )

        for i, e in enumerate(tokens):
            if i == 10:
                break
            e = e.strip('\'\"‘’“”')
            response += '{} - {}\n'.format(emojis[i], e)

        self.client.api_call(
            'chat.postMessage',
            channel=self.channel_id,
            text=response,
            as_user=True
        )


    def execute(self):
        if self.sanitize():
            self.post()


class Roast(Command):


    def __init__(self, client, config, tree, read, write):
        super().__init__(client, config, tree, read, write)

        self.user_id = self.get_user_id(self.tree['user'])
        self.channel_id = self.get_channel_id(self.read)


    def sanitize(self):
        response = None

        if len(self.tree['tokens']) > 1:
            # can't roast more than one person
            response = 'Sorry <@{}>, I can only '.format(
                self.user_id
            ) + 'roast one person at a time!'
        elif len(self.tree['tokens']) == 0:
            # can't roast if there is nobody mentioned
            response = 'Sorry <@{}>, you must mention'.format(
                self.user_id
            ) + ' a user I can roast!'
        else:
            person = self.tree['tokens'][0]
            users = self.config.USERS.keys()

            if person.strip('@') not in users:
                # user does not exist
                response = 'Sorry <@{}>, this user '.format(
                    self.user_id
                ) + 'does not exist!'

        if response is None:
            return True
        else:
            self.client.api_call(
                'chat.postMessage',
                channel=self.channel_id,
                text=response,
                as_user=True
            )
            return False


    def post(self):
        parent = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))
        )

        # get random roast from file
        roasts_file = os.path.join(parent, 'data', 'roasts.txt')
        f = open(roasts_file, 'r')
        roasts = [r.strip() for r in f.read().strip().split('\n')]
        roast = random.choice(roasts)
        f.close()

        # construct response - @user: <msg>
        roast_user = self.tree['tokens'][0].strip('@')
        roast_user_id = self.get_user_id(roast_user)
        response = '<@{}>, {}'.format(roast_user_id, roast)

        self.client.api_call(
            'chat.postMessage',
            channel=self.channel_id,
            text=response,
            as_user=True
        )


    def execute(self):
        if self.sanitize():
            self.post()


class Compliment(Command):


    def __init__(self, client, config, tree, read, write):
        super().__init__(client, config, tree, read, write)

        self.user_id = self.get_user_id(self.tree['user'])
        self.channel_id = self.get_channel_id(self.read)


    def sanitize(self):
        response = None

        if len(self.tree['tokens']) > 1:
            # can't roast more than one person
            response = 'Sorry <@{}>, I can only '.format(
                self.user_id
            ) + 'compliment one person at a time!'
        elif len(self.tree['tokens']) == 0:
            # can't roast if there is nobody mentioned
            response = 'Sorry <@{}>, you must mention'.format(
                self.user_id
            ) + ' a user I can compliment!'
        else:
            person = self.tree['tokens'][0]
            users = self.config.USERS.keys()

            if person.strip('@') not in users:
                # user does not exist
                response = 'Sorry <@{}>, this user '.format(
                    self.user_id
                ) + 'does not exist!'

        if response is None:
            return True
        else:
            self.client.api_call(
                'chat.postMessage',
                channel=self.channel_id,
                text=response,
                as_user=True
            )
            return False


    def post(self):
        parent = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))
        )

        # get random roast from file
        roasts_file = os.path.join(parent, 'data', 'compliments.txt')
        f = open(roasts_file, 'r')
        compliments = [c.strip() for c in f.read().strip().split('\n')]
        compliment = random.choice(compliments)
        f.close()

        # construct response - @user: <msg>
        comp_user = self.tree['tokens'][0].strip('@')
        comp_user_id = self.get_user_id(comp_user)
        response = '<@{}>, {}'.format(comp_user_id, compliment)

        self.client.api_call(
            'chat.postMessage',
            channel=self.channel_id,
            text=response,
            as_user=True
        )


    def execute(self):
        if self.sanitize():
            self.post()


class Meme(Command):


    def __init__(self, client, config, tree, read, write):
        super().__init__(client, config, tree, read, write)

        self.user_id = self.get_user_id(self.tree['user'])
        self.channel_id = self.get_channel_id(self.read)


    def sanitize(self):
        return True


    def post(self):
        path = os.path.join(self.config.PARENT_DIR,
                            'data', 'memes.txt')

        # get random meme from file
        f = open(path, 'r')
        img_link = random.choice([l.strip() \
            for l in f.read().strip().split('\n')])
        f.close()

        # prepare attachment
        attachments = [{'title': img_link, 'image_url': img_link}]

        # make call with image as attachment
        self.client.api_call(
            'chat.postMessage',
            channel=self.channel_id,
            attachments=attachments,
            as_user=True
        )


    def execute(self):
        self.post()
