import os
import yaml
import random

class FileInteraction:
    global file_path
    file_path = "D:\Tom Servo\Servers\\"

    @classmethod
    def get_file_path(self):
        return file_path

    @classmethod
    def check_existence(self, serverID):
        """
        Checks if given server has a directory.

        serverID: int ID for a server.
        """
        if(os.path.isdir(file_path + str(serverID))):
            return True
        else:
            return False

    @classmethod
    def add_list_to_user(self, userID, user_list, serverID):
        """
        """
        with open(file_path + str(serverID) + "\\" + str(userID) + ".txt", 'w') as f:
            for item in user_list:
                f.write(str(item[0]) + "," + str(item[1]) + "\n")

    @classmethod
    def add_message_to_user(self, userID, messageID, channelID, serverID):
        """
        Appends given message to user's file.

        userID: int ID for user.
        messageID: int ID for user's message.
        channelID: int ID for message's channel.
        serverID: int ID for a server.
        """
        f = open(file_path + str(serverID) + "\\" + str(userID) + ".txt", "a")
        f.write(str(messageID) + "," + str(channelID) + "\n")
        f.close()

    @classmethod
    def sort_all_files(self, serverID):
        """
        Cycles through each txt file in a server directory.
        Reads file and sorts message IDs in desc order.
        Writes back to file.

        serverID: int ID for a server.
        """
        for filename in os.listdir(file_path + str(serverID)):
            if filename.endswith(".txt"):
                f = open(file_path + str(serverID) + "\\" + filename, "r")
                lines = f.readlines()
                f.close()
                lines.sort(reverse=True) # Latest message = highest number. 
                f = open(file_path + str(serverID) + "\\" + filename, "w")
                for line in lines:
                    f.write(str(line))
                f.close()
            else:
                continue

    @classmethod
    def get_yaml_data(self, key, serverID):
        """
        For the given key and serverID, retrieve any section of the .yaml file.

        key: String with .yaml key name.
        serverID: int ID for a server.
        """
        f = open(file_path + str(serverID) + "\\" + str(serverID) + ".yaml", "r")
        yaml_doc = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

        try:
            return yaml_doc[key]
        except Exception as e:
            print(e)
            return None

    @classmethod
    def edit_yaml_data(self, key, serverID, dict_to_write):
        """
        For the given key and serverID, retrieve any section of the .yaml file.
        Then, overwrite the specific section of the file variable with the new dict information.
        Write the whole yaml_doc variable to the file.
        
        key: String with .yaml key name.
        serverID: int ID for a server.
        dict_to_write: dict of new information.
        """
        f = open(file_path + str(serverID) + "\\" + str(serverID) + ".yaml", "r")
        yaml_doc = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

        yaml_doc[key][0] = dict_to_write

        f = open(file_path + str(serverID) + "\\" + str(serverID) + ".yaml", "w")
        yaml.dump(yaml_doc, f, default_flow_style=False)
        f.close()

    @classmethod 
    def write_latest_message(self, serverID, curr_channel, messageID):
        """
        Writes the most recent message to the yaml file of a server under the correct channel.

        serverID: int ID for a server.
        curr_channel: int ID for current channel.
        messageID: int ID for latest message.
        """
        new_dict = dict(self.get_yaml_data("channels", serverID)[0])
        new_dict[curr_channel] = messageID
        self.edit_yaml_data("channels", serverID, new_dict)

    @classmethod 
    def read_random_file(self, serverID):
        random_file = random.choice(os.listdir(file_path + str(serverID)))
        while random_file[-4:] != ".txt" or os.path.getsize(file_path + str(serverID) + "\\" + random_file) < 5120:
            random_file = random.choice(os.listdir(file_path + str(serverID)))

        f = open(file_path + str(serverID) + "\\" + random_file, "r")
        lines = f.readlines()
        f.close()
        stripped = [line.strip().split(",") for line in lines]
        int_stripped = [[int(value) for value in stripped_line] for stripped_line in stripped]
        
        if len(int_stripped) <= 500:
            return int_stripped, int(random_file.strip(".txt"))
        else:
            return random.sample(int_stripped, 500), int(random_file.strip(".txt"))

    @classmethod 
    def create_gen_file(self, serverID, user_file):
        with open(file_path + str(serverID) + "\\" + "temporary_generation_file.txt", 'w', encoding='utf-8') as f:
            for line in user_file:
                f.write(line + "\n")    

    @classmethod 
    def delete_gen_file(self, serverID):
        os.remove(file_path + str(serverID) + "\\" + "temporary_generation_file.txt")
