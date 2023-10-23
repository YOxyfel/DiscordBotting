import asyncio
import json
import os
import re
import time
import sqlite3

import discord
from discord import app_commands
from discord import ui
from discord import Embed
from discord.ext import command
from discord.ext import buttons
import requests
#from tictactoe import start_game
#
# look on discord

#---------------------------0-------DataBase-------0-------------------------------------
con = sqlite3.connect('dbs/1.db')
c = con.cursor()

#c.execute("""CREATE TABLE users (
#    discord_id INT,
#    discord_username TEXT,
#    win_or_lose TEXT);""")

# in the meanwhile i will look for any database extesntion
con.commit()
con.close()

#----------------------------1-------Client------1--------------------------------------


class MyClient(commands.Bot):

  def __init__(self, *, intents: discord.Intents):
    super().__init__(command_prefix="!", intents=intents)
    intents.message_content = True

  async def setup_hook(self):
    self.tree.copy_global_to(guild=discord.Object(id=1145239923033653280))
    await self.tree.sync(guild=discord.Object(id=1145239923033653280))
    print('Main bot synced!')


bot = MyClient(intents=discord.Intents.all())


@bot.command(aliases=['p'])
async def heya(ctx):
  await ctx.send('hi')


#--------------------------------On Ready event-----------------------------------------


@bot.event
async def on_ready():
  print(f"Logged on as {bot.user}")


#--------------------------------------------------------------------------------------

#-------------------------- Hello Command (Prefix) -------------------------------------------


@bot.tree.command(name="sayhello", description="Makes the bot say hi back!")
async def hi(ctx):
  await ctx.send("hi")


#-------------------------------------------------------------------------------------------

#--------------------------------Ban Command------------------------------------------------


@bot.tree.command(name="ban", description="Bans someone!")
@app_commands.checks.has_permissions(ban_members=True)
async def Ban(interaction: discord.Interaction, user: discord.User):
  guild = interaction.guild
  await interaction.response.send_message(f"Banned {user}.")
  await guild.ban(user)


#-------------------------------------------------------------------------------------------

#--------------------------------Unban Command----------------------------------------------


@bot.tree.command(name="unban")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user: discord.User):

  banlist = []
  guild = interaction.guild

  #putting guild bans into a list
  for i in guild.bans():
    banlist.append(i)

  #looking for the banned user in the list
  for o in banlist:

    if user in o:

      await guild.unban(user)
      await interaction.response.send_message(f"Unbanned {user}.")

    else:
      await interaction.response.send_message(f'{user} is not in the ban list.'
                                              )


#---------------------------------------------------------------------------------------

#------------------------------Modal/Ticket----------------------------------------------------


class Questionnaire(ui.Modal, title='Questionnaire Response'):

  name = ui.TextInput(label='Name')
  answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

  async def on_submit(self, interaction: discord.Interaction):
    username = discord.Member.display_name
    await interaction.response.send_message(
      f'Thanks for submitting a ticket, {username}!')


@bot.tree.command(name='ticket',
                  description='Gives information about that user')
async def whois2(interaction: discord.Interaction):
  await interaction.response.send_modal(Questionnaire())


#----------------------------------------------------------------------------------------

#-----------------------------WhoIs Command---------------------------------------------


@bot.tree.command(name='whois',
                  description='Gives information about that user')
async def whois(interaction: discord.Interaction, member: discord.User):

  name = member.display_name
  joindate = member.joined_at
  creationdate = member.created_at
  fjoindate = discord.utils.format_dt(joindate, style="F")
  fcreatedate = discord.utils.format_dt(creationdate, style="F")
  embedo=discord.Embed(title=f"{member}", description=f"{name} joined at {fjoindate} \nAccount created at {fcreatedate}", color=0xFF5733)
  embedo.set_footer(text="hi")
  await interaction.response.send_message(embed=embedo)


#---------------------------------------------------------------------------------------


#tableflip variant 1
@bot.tree.command(name="tableflip1",
                  description="Makes the bot flip the table 1!")
async def tableFlip1(interaction: discord.Interaction):
  await interaction.response.send_message(f"(╯°□°)╯︵ ┻━┻")


#Survival Timer
@bot.tree.context_menu(name='Survival time!')
async def survival(interaction: discord.Interaction, member: discord.Member):
  joined_time = member.joined_at
  current_time = discord.utils.utcnow()
  time_duration = current_time - joined_time

  days = time_duration.days
  hours, remainder = divmod(time_duration.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)

  formatted_duration = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
  await interaction.response.send_message(
    f'{member} has survived {formatted_duration}')


#-----------------------------------------------------------------------------------------
last_reply_times = {}


@bot.command(name='hello')
async def hello(ctx):
  await ctx.send('Hello, I am a bot!')


# def get_quote():
#   response = requests.get("https://zenquotes.io/api/random")
#   json_data = json.loads(response.text)

#   quote = json_data[0]['q'] + " -" + json_data[0]['a']
#   return quote

# async def clear_last_10_messages(channel):
#   async for msg in channel.history(limit=11):
#     await msg.delete()
#     await asyncio.sleep(1)  # Add a delay of 1 second between deletions
#   await channel.send('Cleared the last 10 messages.')

# async def clear_entire_history(channel):
#   async for msg in channel.history():
#     await msg.delete()
#     await asyncio.sleep(1)  # Add a delay of 1 second between deletions
#   await channel.send('Cleared the entire message history.')

bot.run(os.environ['TOKEN'])
