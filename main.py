import os
import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents(messages = True, guilds = True, members = True) 


intents.message_content = True

client = commands.Bot(command_prefix=",",intents=intents)

memberShip = {
  "id" : "name"
}

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.tree.sync()

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == "info":
    await message.channel.send(message)

#new member
@client.event
async def on_member_join(member):
  guild = member.guild
  channel = guild.get_channel(1231584560853291028)
  view = View()
  res_button1 = Button(label = "我是社員", style = discord.ButtonStyle.green)
  res_button2 = Button(label = "我不是社員", style = discord.ButtonStyle.red)
  res_button1.callback = isMember
  res_button2.callback = notMember
  view.add_item(res_button1)
  view.add_item(res_button2)
  await channel.send(f"{member.mention} 加入了伺服器", view = view)

@client.event
async def on_member_remove(member):
  memberShip.pop(f"{member.id}")

async def isMember(interaction:discord.Integration):
  await interaction.response.edit_message(view = None)
  member = {
    f"{interaction.user.id}" : f"{interaction.user.name}"
  }
  memberShip.update(member)
  print(memberShip)

async def notMember(interaction:discord.Interaction):
  await interaction.response.edit_message(view = None)

#name
@client.tree.command(name = "name", description =" change your name into a form")
async def name(interaction: discord.Interaction, name: str):
  author = interaction.user
  await author.edit(nick=name)
  await interaction.response.send_message("done")

#roles
@client.tree.command(name = "join", description = "join a role" )
async def join(interaction:discord.Interaction, role:discord.Role):
  roleList = interaction.user.roles
  if role not in roleList:
    roleList.append(role)
  await interaction.user.edit(roles = roleList)
  await interaction.response.send_message("done")

@client.tree.command(name = "leave", description = "leave a role")
async def leave(interaction:discord.Interaction, role:discord.Role):
  roleList = interaction.user.roles
  if role in roleList:
    roleList.remove(role)
  await interaction.user.edit(roles = roleList)
  await interaction.response.send_message("done")

#channels
@client.tree.command(name = "create", description = "create a channel")
async def create(interaction:discord.Interaction, name:str):
  guild = interaction.guild
  await guild.create_text_channel(name)
  await interaction.response.send_message("done")

@client.tree.command(name = "delete", description = "delete a channel")
async def delete(interaction:discord.Interaction, channel:discord.TextChannel):
  await channel.delete()
  await interaction.response.send_message("done")

#stop bot
@client.tree.command(name = "killbot", description = "stop the bot")
async def killbot(interaction:discord.Interaction):
  await interaction.response.send_message("killed bot")
  await client.close()

client.run(os.getenv('TOKEN'))