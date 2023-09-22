from player import Player
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element,tostring
import player_pb2


class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        result = []
        for plr in players:
            result.append({
                "nickname": plr.nickname,
                "email": plr.email,
                "date_of_birth": datetime.strftime(plr.date_of_birth, "%Y-%m-%d"),
                "xp": plr.xp,
                "class": plr.cls
            })
        return result
        pass

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        result = []
        for d in list_of_dict:
            result.append(Player(d['nickname'], d['email'], d["date_of_birth"], d['xp'], d["class"]))
        return result
        pass

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        aux = []
        root = ET.fromstring(xml_string)
        for plr in root:
            temp = {}
            for atr in plr:
                if atr.tag == 'xp':
                    temp[atr.tag] = int(atr.text)
                else:
                    temp[atr.tag] = atr.text
            aux.append(temp)
        result = []

        for d in aux:
            result.append(Player(d['nickname'], d['email'], d["date_of_birth"], d['xp'], d["class"]))
        return result
        pass

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''

        temp = []
        for plr in list_of_players:
            temp.append({
                "nickname": plr.nickname,
                "email": plr.email,
                "date_of_birth": datetime.strftime(plr.date_of_birth, "%Y-%m-%d"),
                "xp": plr.xp,
                "class": plr.cls
            })

        root = Element('data')

        for p in temp:
            plr = Element('player')
            for key, val in p.items():
                child = Element(key)
                child.text = str(val)
                plr.append(child)
            root.append(plr)
        return tostring(root)
        pass

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        '''
        enum Class {
              Berserk = 0;
              Tank = 1;
              Paladin = 3;
              Mage = 4;
            }
        '''

        classes = {
            0: 'Berserk',
            1: 'Tank',
            3: 'Paladin',
            4: 'Mage'
        }

        result = []

        players = player_pb2.PlayersList()
        players.ParseFromString(binary)

        for plr in players.player:
            result.append(Player(plr.nickname, plr.email, plr.date_of_birth, plr.xp, classes[plr.cls]))

        return result
        pass

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects into a binary protobuf string.
        '''
        player_list = player_pb2.PlayersList()
        for plr in list_of_players:
            player = player_list.Player()
            player.nickname = plr.nickname
            player.email = plr.email
            player.date_of_birth = datetime.strftime(plr.date_of_birth, "%Y-%m-%d")
            player.xp = plr.xp
            player.cls = plr.cls
            player_list.player.append(player)

        return player_list.SerializeToString()
        pass

