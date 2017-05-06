import os
import time
import argparse

from slackclient import SlackClient
from imgurpython import ImgurClient
from swiper.settings import ProductionConfig, TestingConfig
from swiper.command import Help, Announcement, Poll, Roast, \
    Compliment, Meme
from swiper.parse import Message, Parser
from swiper.error import ParseError

parser = argparse.ArgumentParser(description='Swiper Bot server config')
parser.add_argument('-p', '--production', action='store_true', default='False',
                    help='start swiper on production stream')
parser.add_argument('-t', '--testing', action='store_true', default='False',
                    help='start swiper on testing stream')
parser.add_argument('-u', '--update', action='store_true', default='False',
                    help='update memes image db')
args = parser.parse_args()

if args.production == True:
    config = ProductionConfig()
if args.testing == True:
    config = TestingConfig()

def create_image_db():
    client = ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_CLIENT_SECRET)
    image_db = []
    try:
        items = client.memes_subgallery(sort='viral', page=0, window='week')
        for gallery in items:
            if gallery.is_album:
                album_id = gallery.id
                images = client.get_album_images(album_id)
                image_db.extend([image.link for image in images])
            else:
                image_db.append(gallery.link)
    except:
        return False
    if image_db:
        db_file = os.path.join(config.PARENT_DIR,
                                'data', 'memes.txt')
        f = open(db_file, 'w+')
        for link in image_db:
            f.write(link + '\n')
        f.close()
    return True

def parse_stream_message(output_list):
    if output_list and len(output_list):
        for output in output_list:
            if output and 'content' in output and \
                config.BOT_USERNAME in output['content']:
                return output
    return None

client = SlackClient(config.API_KEY)
if client.rtm_connect():
    print('Swiper connected and running')

    if args.update == True:
        create_image_db()
        print('Image DB updated')

    while True:
        output = parse_stream_message(client.rtm_read())
        if output:
            # write output to log file
            # log_file = os.path.join(config.PARENT_DIR, 'data', 'logs.txt')
            # f = open(log_file, 'a')
            # f.write(str(output['content']) + '\n')
            # f.close()

            if not config.SKIP_FIRST:
                # parse stream message
                try:
                    parser = Parser(Message(output))
                    tree = parser.parse()
                except ParseError:
                    response = 'Oops! There was an error in ' + \
                        'processing your request.'
                    client.api_call(
                        'chat.postMessage',
                        channel=channel_id,
                        text=response,
                        as_user=True
                    )
                    continue

                # get parsed information
                user = tree['user']
                command = tree['command']
                channel = tree['channel']

                if channel in config.CHANNELS.keys():
                    channel_id = config.CHANNELS[channel]
                else:
                    continue

                if command == '/help':
                    help = Help(client=client, config=config, tree=tree,
                                read=tree['channel'], write=tree['channel'])
                    help.execute()
                elif command == '/announce':
                    announce = Announcement(client=client, config=config,
                                            tree=tree, read=tree['channel'],
                                            write='announcements')
                    announce.execute()
                elif command == '/poll':
                    poll = Poll(client=client, config=config, tree=tree,
                                read=tree['channel'], write=tree['channel'])
                    poll.execute()
                elif command == '/roast':
                    roast = Roast(client=client, config=config, tree=tree,
                                read=tree['channel'], write=tree['channel'])
                    roast.execute()
                elif command == '/compliment':
                    compliment = Compliment(client=client, config=config,
                                            tree=tree, read=tree['channel'],
                                            write=tree['channel'])
                    compliment.execute()
                elif command == '/meme':
                    meme = Meme(client=client, config=config, tree=tree,
                                read=tree['channel'], write=tree['channel'])
                    meme.execute()
                else:
                    if command:
                        # invalid command
                        response = 'Sorry <@{}>, I don\'t understand '.format(
                            config.USERS[user]
                        ) + 'this command!'

                        client.api_call(
                            'chat.postMessage',
                            channel=channel_id,
                            text=response,
                            as_user=True
                        )
                    else:
                        # invalid message - doesn't include a backslash
                        # command to swiper
                        response = 'Hi <@{}>, type `@swiper /help` to see'.format(
                            config.USERS[user]
                        ) + ' what I can do!'

                        client.api_call(
                            'chat.postMessage',
                            channel=channel_id,
                            text=response,
                            as_user=True
                        )

            config.SKIP_FIRST = False
else:
    print('Connection failed')
    exit(1)
