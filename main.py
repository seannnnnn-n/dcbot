import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True) 


intents.message_content = True

client = commands.Bot(command_prefix=",",intents=intents)



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

#name
@client.tree.command(name="name" , description="change your name into a form")
async def name(interaction: discord.Interaction, name: str):
  author = interaction.user
  await author.edit(nick=name)
  await interaction.response.send_message("done")

#roles
@client.tree.command(name="join",description="join a role" )
async def join(interaction:discord.Interaction,role:discord.Role):
  roleList=interaction.user.roles
  if role not in roleList:
    roleList.append(role)
  await interaction.user.edit(roles=roleList)
  await interaction.response.send_message("done")

@client.tree.command(name="leave",description="leave a role")
async def leave(interaction:discord.Interaction,role:discord.Role):
  roleList=interaction.user.roles
  if role in roleList:
    roleList.remove(role)
  await interaction.user.edit(roles=roleList)
  await interaction.response.send_message("done")

#welcome
@client.tree.command(name="welcome",description="welcome new member")
async def welcome(interaction:discord.Interaction,truename:str,nickname: str, role:discord.Role):
  author = interaction.user
  roleList=interaction.user.roles
  if role not in roleList:
    roleList.append(role)
  name = "2nd - %s - %s" % (nickname,truename)
  await author.edit(nick=name)
  await author.edit(roles=roleList)
  await interaction.response.send_message("done")

#channels
@client.tree.command(name="create",description="create a channel")
async def create(interaction:discord.Interaction,name:str):
  guild = interaction.guild
  await guild.create_text_channel(name)
  await interaction.response.send_message("done")

@client.tree.command(name="delete",description="delete a channel")
async def delete(interaction:discord.Interaction,channel:discord.TextChannel):
  await channel.delete()
  await interaction.response.send_message("done")

client.run('') # bot
