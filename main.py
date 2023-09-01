import asyncio
import json
import os
import re
import time
import sqlite3

import discord
from discord.ext import commands
import requests
#from tictactoe import start_game

# look on discord

#---------------------------0-------DataBase-------0-------------------------------------
con = sqlite3.connect('dbs/1.db')
c = con.cursor()

c.execute("""CREATE TABLE users (
    discord_id INT,
    discord_username TEXT,
    win_or_lose TEXT);""")

# in the meanwhile i will look for any database extesntion
con.commit()
con.close()


#----------------------------1-------Client------1--------------------------------------
class MyClient(commands.Bot):

  def __init__(self, *, intents: discord.Intents):
    super().__init__(command_prefix="!", intents=intents)

  async def setup_hook(self):
    self.tree.copy_global_to(guild=discord.Object(id=1145239923033653280))
    await self.tree.sync(guild=discord.Object(id=1145239923033653280))
    print('Main bot synced!')


bot = MyClient(intents=discord.Intents.all())


#-------------------------- SLASH COMMANDS ----------------------------------------------
@bot.tree.command(name="sayhello", description="Makes the bot say hi back!")
async def hi(interaction: discord.Interaction):
  await interaction.response.send_message(f"Hello! {interaction.user.mention}")


@bot.tree.command(name="tictactoe", description="Play a TicTacToe game!")
async def tictactoe(interaction: discord.Interaction):
  await interaction.response.send_message(f"Hello2! {interaction.user.mention}"
                                          )


@bot.tree.context_menu(name='Survival time!')
async def gay(interaction: discord.Interaction, member: discord.Member):
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
options = [
  "To play a game of tic tac toe, command : $game1",
  "To get inspired, command : $inspire",
  "To clear chat history, command : $clear (clears last 10",
  "To clear chat history, command :$clear_all (clears whole history)"
]
greetings = ['hello', 'hi', 'yo', 'wassup', 'hey', 'hoi']


@bot.command(name='hello')
async def hello(ctx):
  await ctx.send('Hello, I am a bot!')


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)

  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):

  if message.author == bot.user:
    return

  content = message.content.lower()

  #  if content.message.startswith('$tictactoe'):
  #    await start_game(content)

  #Greeting with 10s cooldown
  if re.search(r'\b(?:' + '|'.join(greetings) + r')\b', content):
    user_id = message.author.id
    current_time = time.time()

    # Check if the user's last reply time is available and if the timeout has passed
    if user_id in last_reply_times and current_time - last_reply_times[
        user_id] < 60:
      return

    last_reply_times[user_id] = current_time
    await message.channel.send(f"Hello, {message.author.mention}!")

  #Write a random quote
  if content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  #Clear last 10 messages or all messages
  if content.startswith('$clear'):
    if message.channel.permissions_for(message.author).manage_messages:
      if content == '$clear':
        await clear_last_10_messages(message.channel)
      elif content == '$clear_all':
        await clear_entire_history(message.channel)
    else:
      await message.channel.send(
        "You don't have permission to use this command.")


async def clear_last_10_messages(channel):
  async for msg in channel.history(limit=11):
    await msg.delete()
    await asyncio.sleep(1)  # Add a delay of 1 second between deletions
  await channel.send('Cleared the last 10 messages.')


async def clear_entire_history(channel):
  async for msg in channel.history():
    await msg.delete()
    await asyncio.sleep(1)  # Add a delay of 1 second between deletions
  await channel.send('Cleared the entire message history.')


bot.run(os.environ['TOKEN'])
