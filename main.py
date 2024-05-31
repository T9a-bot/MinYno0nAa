from asyncio import run as arun
import asyncio
import random
import requests
from collections import UserDict
from highrise import BaseBot , __main__
from highrise import *
from highrise.models import SessionMetadata, User
from highrise.models import SessionMetadata, User, CurrencyItem, Item, AnchorPosition, Reaction, ModerateRoomRequest, Position
from highrise import BaseBot, User, Position, SessionMetadata
from highrise import BaseBot, __main__ 
from highrise.models import (AnchorPosition, Item, Position, User,)
from highrise.models import *
import time
from asyncio import Task
from highrise.__main__ import *
from highrise.models import (AnchorPosition, CurrencyItem, Item, Position,SessionMetadata,User,)
from highrise.__main__ import BotDefinition
emote_list : list[tuple[str, str]] = [('0', 'idle-sleep'), ('2', 'idle-sad'), ('4', 'idle-loop-sitfloor'), ('5', 'idle-loop-shy'), ('6', 'idle-enthusiastic'), ('7', 'idle-dance-headbobbing'), ('8', 'emote-wave'), ('9', 'emote-tired'), ('10', 'emote-think'), ('11', 'emote-theatrical'), ('12', 'emote-snowangel'), ('13', 'emote-shy'), ('14', 'emote-sad'), ('15', 'emote-peace'), ('16', 'emote-model'), ('17', 'emote-lust'), ('18', 'emote-laughing2'), ('19', 'emote-laughing'), ('20', 'emote-kiss'), ('21 Kick', 'emote-kicking'), ('22', 'emote-jumpb'), ('23', 'emote-judochop'), ('24 Jetpack', 'emote-jetpack'), ('25', 'emote-hot'), ('26', 'emote-hello'), ('27', 'emote-happy'), ('28', 'emote-exasperatedb'), ('29', 'emote-exasperated'), ('30', 'emote-death2'), ('31', 'emote-death'), ('32', 'emote-dab'), ('33', 'emote-curtsy'), ('34', 'emote-confused'), ('35', 'emote-cold'), ('36', 'emote-charging'), ('37', 'emote-bunnyhop'), ('38', 'emote-bow'), ('39', 'emote-boo'), ('40', 'emote-baseball'), ('41', 'emote-apart'), ('42', 'emoji-thumbsup'), ('43', 'emoji-there'), ('44', 'emoji-sneeze'), ('45', 'emoji-smirking'), ('46', 'emoji-sick'), ('47', 'emoji-scared'), ('48', 'emoji-punch'), ('49', 'emoji-dizzy'), ('50', 'emoji-cursing'), ('51', 'emoji-crying'), ('52', 'emoji-clapping'), ('53', 'emoji-celebrate'), ('54', 'emoji-arrogance'), ('55', 'emoji-angry'), ('56', 'dance-voguehands'), ('57', 'dance-tiktok8'), ("58", 'dance-tiktok2'), ('59', 'dance-spiritual'), ("60", 'dance-shoppingcart'), ('61', 'dance-russian'), ('62', 'dance-macarena'), ('63','dance-blackpink'), ('64', 'idle-enthusiastic')]

class BotDefinition:
  def __init__(self, bot, room_id, api_token):
      self.bot = bot
      self.room_id = room_id
      self.api_token = api_token

class MyBot(BaseBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.following_user = None 
        self.banned_users = {} 
        self.following_username = None
        super().__init__()
        self.user_positions = {}
      
    async def loop(self: BaseBot, user: User, message: str) -> None:
      # Defining the loop_emote method locally so it cann't be accessed from the command handler.
      async def loop_emote(self: BaseBot, user: User, emote_name: str) -> None:
          emote_id = ""
          for emote in emote_list:
              if emote[0].lower() == emote_name.lower():
                  emote_id = emote[1]
                  break
          if emote_id == "":
              await self.highrise.chat("Invalid emote")
              return
          user_position = None
          user_in_room = False
          room_users = (await self.highrise.get_room_users()).content
          for room_user, position in room_users:
              if room_user.id == user.id:
                  user_position = position
                  start_position = position
                  user_in_room = True
                  break
          if user_position == None:
              await self.highrise.chat("User not found")
              return
          await self.highrise.chat(f"@{user.username} is looping {emote_name}")
          while start_position == user_position:
              try:
                  await self.highrise.send_emote(emote_id, user.id)
              except:
                  await self.highrise.chat(f"Sorry, @{user.username}, this emote isn't free or you don't own it.")
                  return
              await asyncio.sleep(10)
              room_users = (await self.highrise.get_room_users()).content
              user_in_room = False
              for room_user, position in room_users:
                  if room_user.id == user.id:
                      user_position = position
                      user_in_room = True
                      break
              if user_in_room == False:
                  break
      try:
          splited_message = message.split(" ")
          # The emote name is every string after the first one
          emote_name = " ".join(splited_message[1:])
      except:
          await self.highrise.chat("Invalid command format. Please use '/loop <emote name>.")
          return
      else:   
          taskgroup = self.highrise.tg
          task_list : list[Task] = list(taskgroup._tasks)
          for task in task_list:
              if task.get_name() == user.username:
                  # Removes the task from the task group
                  task.cancel()

          room_users = (await self.highrise.get_room_users()).content
          user_list  = []
          for room_user, pos in room_users:
              user_list.append(room_user.username)

          taskgroup.create_task(coro=loop_emote(self, user, emote_name))
          task_list : list[Task] = list(taskgroup._tasks)
          for task in task_list:
              if task.get_coro().__name__ == "loop_emote" and not (task.get_name() in user_list):
                  task.set_name(user.username)
    async def stop_loop(self: BaseBot, user: User, message: str) -> None:
          taskgroup = self.highrise.tg
          task_list : list[Task] = list(taskgroup._tasks)
          for task in task_list:
              print(task.get_name())
              if task.get_name() == user.username:
                  task.cancel()
                  await self.highrise.chat(f"Stopping your emote loop, {user.username}!")
                  return
          await self.highrise.chat(f"You're not looping any emotes, {user.username}")
          return

    async def on_user_join(self, user: User, position: Position | AnchorPosition):
       await self.highrise.chat(f" Welcome to CampHut, feel free to sit anywhere and make friends {user.username} ")
      

    async def run(self, room_id, token):
       definitions = [BotDefinition(self, room_id, token)]
       await __main__.main(definitions)


    async def on_chat(self, user: User, message: str):
      
          emote_mapping = {
            "all a": "emote-float",
            "all b": "dance-tiktok2",
            "all c": "emote-pose1",
            "all d": "dance-shoppingcart",
            "all e": "dance-russian",
            "all f": "idle_singing",
            "all g": "idle-enthusiastic",
            "all h": "idle-dance-casual",
            "all i": "idle-loop-sitfloor",
            "all j": "emote-lust",
            "all k": "emote-greedy",
            "all l": "emote-bow",
            "all m": "emote-curtsy",
            "all n": "emote-snowball",
            "all o": "emote-snowangel",
            "all p": "emote-confused",
            "all q": "emote-teleporting",
            "all r": "emote-swordfight",
            "all s": "emote-energyball",
            "all t": "dance-tiktok8",
            "all u": "dance-blackpink",
            "all v": "emote-model",
            "all w": "dance-pennywise",
            "all x": "dance-tiktok10",
            "all y": "emote-telekinesis",
            "all z": "emote-hot",
            "all 1": "dance-weird",
            "all 2": "emote-pose7",
            "all 3": "emote-pose8",
            "all 4": "emote-pose3",
            "all 5": "emote-pose5"
          }
          # تحقق من البداية وقم بإرسال الرقصة المناسبة لجميع المستخدمين في الغرفة
          for key, emote in emote_mapping.items():
            if message.startswith(key) and user.username in ["T9s", "MinYno0nAa"]:
                roomUsers = (await self.highrise.get_room_users()).content
                for roomUser, _ in roomUsers:
                    if isinstance(roomUser, User):
                        await self.highrise.send_emote(emote, roomUser.id)
                    else:
                        print("Ignoring non-User object in roomUsers")
                break

          if message.lower().startswith("/loop "):
            await self.loop(user, message)
          elif message.lower().startswith("/stoploop"):
            await self.stop_loop(user, message)
            
          if message.startswith("!come") and user.username in ["T9s" , "MinYno0nAa"]:
            response = await self.highrise.get_room_users()
            your_pos = None
            for content in response.content:
              if content[0].id == user.id:
                if isinstance(content[1], Position):
                    your_pos = content[1]
                    break
            if not your_pos:
              await self.highrise.send_whisper(user.id, f"احداثيات غير صالحه")
              return
            await self.highrise.chat("I,m coming ")
            await self.highrise.walk_to(your_pos)

          if message.startswith("Float"):
            await self.highrise.send_emote("emote-float", user.id)
          if message.startswith("Tiktok2"):
            await self.highrise.send_emote("dance-tiktok2", user.id)   
          if message.startswith("pose1"):
            await self.highrise.send_emote("emote-pose1", user.id)
          if message.startswith("Russian"):
            await self.highrise.send_emote("dance-russian", user.id)
          if message.startswith("Sing"):
            await self.highrise.send_emote("idle_singing", user.id)
          if message.startswith("Enth"):
            await self.highrise.send_emote("idle-enthusiastic", user.id)   
          if message.startswith("Casual"):
            await self.highrise.send_emote("idle-dance-casual", user.id)   
          if message.startswith("sit"):
            await self.highrise.send_emote("idle-loop-sitfloor", user.id)
          if message.startswith("Lust"):
            await self.highrise.send_emote("emote-lust", user.id)
          if message.startswith("Creedy"):
            await self.highrise.send_emote("emote-greedy", user.id)
          if message.startswith("Bow"):
            await self.highrise.send_emote("emote-bow", user.id)
          if message.startswith("Curtsy"):
            await self.highrise.send_emote("emote-curtsy", user.id)
          if message.startswith("Snow"):
            await self.highrise.send_emote("emote-snowball", user.id)
          if message.startswith("Angel"):
            await self.highrise.send_emote("emote-snowangel", user.id)
          if message.startswith("Confused"):
            await self.highrise.send_emote("emote-confused", user.id)
          if message.startswith("Teleport"):
            await self.highrise.send_emote("emote-teleporting", user.id)
          if message.startswith("Swordfight"):
            await self.highrise.send_emote("emote-swordfight", user.id)
          if message.startswith("Energy"):
            await self.highrise.send_emote("emote-energyball", user.id)
          if message.startswith("Tiktok8"):
            await self.highrise.send_emote("dance-tiktok8", user.id)
          if message.startswith("Blackpink"):
            await self.highrise.send_emote("dance-blackpink", user.id)
          if message.startswith("Model"):
            await self.highrise.send_emote("emote-model", user.id)
          if message.startswith("Penny"):
            await self.highrise.send_emote("dance-pennywise", user.id)
          if message.startswith("Tiktok10"):
            await self.highrise.send_emote("dance-tiktok10", user.id)
          if message.startswith("Telekinesis"):
            await self.highrise.send_emote("emote-telekinesis", user.id)
          if message.startswith("Hot"):
            await self.highrise.send_emote("emote-hot", user.id)
          if message.startswith("Weird"):
            await self.highrise.send_emote("dance-weird", user.id)
          if message.startswith("Pose7"):
            await self.highrise.send_emote("emote-pose7", user.id)
          if message.startswith("Pose8"):
            await self.highrise.send_emote("emote-pose8", user.id)
          if message.startswith("Pose3"):
            await self.highrise.send_emote("emote-pose3", user.id)
          if message.startswith("Pose5"):
            await self.highrise.send_emote("emote-pose5", user.id)
          if message.startswith("kiss"):
             await self.highrise.send_emote("emote-kiss", user.id)

          if message.startswith("Laughing"):
             await self.highrise.send_emote("emote-laughing", user.id)
          if message.startswith("cursing"):
             await self.highrise.send_emote("emoji-cursing", user.id)
          if message.startswith("flex"):
             await self.highrise.send_emote("emoji-flex", user.id)
          if message.startswith("gagging"):
             await self.highrise.send_emote("emoji-gagging", user.id)
          if message.startswith("celebrate"):
             await self.highrise.send_emote("emoji-celebrate", user.id)
          if message.startswith("macarena"):
             await self.highrise.send_emote("dance-macarena", user.id)
          if message.startswith("charging"):
             await self.highrise.send_emote("emote-charging", user.id)
          if message.startswith("shopp"):
             await self.highrise.send_emote("dance-shoppingcart", user.id)
          if message.startswith("maniac"):
             await self.highrise.send_emote("emote-maniac", user.id)
          if message.startswith("snake"):
             await self.highrise.send_emote("emote-snake", user.id)
          if message.startswith("frog"):
             await self.highrise.send_emote("emote-frog", user.id)
          if message.startswith("superpose"):
             await self.highrise.send_emote("emote-superpose", user.id)
          if message.startswith("cute"):
             await self.highrise.send_emote("emote-cute", user.id)
          if message.startswith("tiktok9"):
             await self.highrise.send_emote("dance-tiktok9", user.id)
          if message.startswith("weird"):
             await self.highrise.send_emote("dance-weird", user.id)
          if message.startswith("cutey"):
             await self.highrise.send_emote("emote-cutey", user.id)
          if message.startswith("punkguitar"):
             await self.highrise.send_emote("emote-punkguitar", user.id)
          if message.startswith("zombierun"):
             await self.highrise.send_emote("emote-zombierun", user.id)
          if message.startswith("fashi"):
             await self.highrise.send_emote("emote-fashionista", user.id) 
          if message.startswith("gravity"):
             await self.highrise.send_emote("emote-gravity", user.id)
          if message.startswith("icecream"):
             await self.highrise.send_emote("dance-icecream", user.id)
          if message.startswith("wrong"):
             await self.highrise.send_emote("dance-wrong", user.id)
          if message.startswith("uwu"):
             await self.highrise.send_emote("idle-uwu", user.id)
          if message.startswith("tiktok4"):
             await self.highrise.send_emote("idle-dance-tiktok4", user.id)
          if message.startswith("shy2"):
             await self.highrise.send_emote("emote-shy2", user.id)
          if message.startswith("anime"):
             await self.highrise.send_emote("dance-anime", user.id)



          if message.lower().startswith("!help"):
            dance_list = [
                "Float", "Tiktok2", "pose1", "Russian", "Sing", "Enth", "Casual", "sit",
                "Lust", "Creedy", "Bow", "Curtsy", "Snow", "Angel", "Confused", "Teleport",
                "Swordfight", "Energy",
            ]

            # Convert the list to a comma-separated string
            dance_list_str = ", ".join(dance_list)

            # Send the message
            await self.highrise.send_whisper(user.id, dance_list_str)


          if message.lower().startswith("!help"):
            await self.highrise.send_whisper(user.id, "Model , Penny , Tiktok10 , Telekinesis , Hot , Weird , Pose7 , Pose8 , Pose3 , Pose5 , kis , Laughing , cursing , flex , gagging , Blackpink , Tiktok8" )

          if message.lower().startswith("!help"):
            await self.highrise.send_whisper(user.id, " celebrate , macarena , charging , shopp , maniac , snake  , frog , superpose , cute , tiktok9 , weird , cutey ,  punkguitar , zombierun , fashi , gravity , icecream , wrong , uwu , tiktok4 , shy2 , anime" )


if __name__== "__main__":
  room_id = "665855b027ee5185e0daea83"
  token = "27a6340de50b01d90827df53d1957b05bdc88172feac10e3a94e131e9871becc"
  arun(MyBot().run(room_id, token))