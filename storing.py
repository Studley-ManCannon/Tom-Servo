import discord
import time

from filedata import FileInteraction

class Storage():

    @classmethod
    async def check_message_author(self, serverID, message_author):
        """
        Checks a message to ensure it was not sent by a bot or an ignored user.

        message_author: User object for sent message.
        """
        if message_author.bot is True or message_author.id in FileInteraction.get_yaml_data("users_to_ignore", serverID):
            return False
        else:
            return True

    @classmethod
    async def get_bans(self, client, serverID):
        ban_list = await client.get_guild(serverID).bans()
        return [ban_entry.user.id for ban_entry in ban_list]

    @classmethod
    async def scrape_channel(self, client, channelID):

        """
        Cycles through a channel from most recent to least up to a set limit.
        Checks the message author.
        If the most recently written message is reached, the loop terminates.
        The messages are added to the user's file.

        channelID: int ID for current channel.
        """
        message_dict = dict()
        curr_channel = client.get_channel(channelID)
        if curr_channel.guild.me.permissions_in(curr_channel).read_messages == False or curr_channel.guild.me.permissions_in(curr_channel).read_message_history == False:
            print("Missing permissions to scrape messages from channel #" + curr_channel.name)
            return
        first_message = True
        last_messageID = dict(FileInteraction.get_yaml_data("channels", curr_channel.guild.id)[0])[channelID]
        i = 0
        print("starting")        
        messages = await curr_channel.history(limit=10000).flatten()
        print(channelID)
        print("finished grabbing")
        for message in messages:
            i += 1
            if i % 100 == 0:
                print("{} out of {} messages in channel #{} scraped".format(i, len(messages), curr_channel.name)) 
            if(await self.check_message_author(client, message.author)):   
                if(message.id != last_messageID):
                    message_dict.setdefault(message.author.id, []).append([message.id, channelID])
                    if(first_message): # Only triggers once, on the first loop.
                        #FileInteraction.write_latest_message(message.guild.id, channelID, message.id)
                        first_message = False
                else:
                    break
            else:
                continue
        print("done")
        return message_dict
