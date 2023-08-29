from pymongo import MongoClient


# Includes database operations
class DB:

    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']

    # checks if an account with the username exists
    def is_account_exist(self, username):
        if self.db.accounts.find_one({'username': username}):
            return True
        else:
            return False

    # registers a user
    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)

    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]

    # checks if an account with the username online
    def is_account_online(self, username):
        if self.db.online_peers.find_one({"username": username}):
            return True
        else:
            return False

    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)

    # logs out the user
    def user_logout(self, username):
        acc = self.db["online_peers"].find_one({"username": username})
        self.db["online_peers"].delete_one(acc)

    # retrieves the ip address and the port number of the username
    # New functions for chat rooms
    def create_chat_room(self, room_id,participants):
        room = {
            "room_id": room_id,
            "participants": participants.split(',')
        }
        self.db.chat_rooms.insert_one(room)
        return room
    def room_exist(self,room_id):
       if self.db.chat_rooms.find_one({"room_id": room_id})!=None:
           return True
       else:
            return False
    def add_participant_to_room(self, room_id, username):
        self.db.chat_rooms.update_one({"room_id": room_id}, {"$push": {"participants": username}})

    def get_room_participants(self, room_id):
        room = self.db.chat_rooms.find_one({"room_id": room_id})
        if room:
            return room["participants"]
        else:
            return []

    def remove_participant_from_room(self, room_id, username):
        self.db.chat_rooms.update_one({"room_id": room_id}, {"$pull": {"participants": username}})

    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])


