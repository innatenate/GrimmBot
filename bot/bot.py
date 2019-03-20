# Main Imports
import discord
import tweepy
import youtube_dl
import extensions
import modules
import asyncio
import pyjokes
import datetime
import os
import json
import requests
import random


# Secondary Imports
from discord.ext import commands
from discord.utils import get
from modules.universal import variables
from modules.settings import settings


# Variables
token = variables.token
players = {}
uptime = 0
version = "1.0.0.0"
lasttweet = ""
patch_notes = f"""
PATCH NOTES:
version {version}
`[+] Did a rewrite. Version has been modified based off of rewrite's version.`
"""


client = commands.Bot(command_prefix=".")
client.remove_command('help')
extensions = ['raffle', 'basic', 'roles', 'music']


async def count_down():
	global uptime
	uptime = 0
	while 1:
		await asyncio.sleep(1)
		uptime += 1


async def error_create(error, ctx):
	embed = discord.Embed(title="ERROR", description=error, colour=discord.Colour.red())
	await client.send_message(ctx.message.channel, embed=embed)
	await client.add_reaction(ctx.message, emoji="⛔")


async def message_create(msg, ctx, color, title=None):
	if title:
		embed = discord.Embed(title=title, description=msg, colour=color)
	else:
		embed = discord.Embed(title="Grimmy", description=msg, colour=color)
	await client.send_message(ctx.message.channel, embed=embed)
	await client.add_reaction(ctx.message, emoji="💚")



async def permission(roles, perm):
	if perm == 1:
		return True
	elif perm == 2:
		if settings.roles[0] not in roles:
			return True
		else:
			return False
	elif perm == 3:
		if settings.roles[0] not in roles and settings.roles[1] not in roles:
			return True
		else:
			return False
	elif perm == 4:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles:
			return True
		else:
			return False
	elif perm == 5:
		if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[2] not in roles and settings.roles[3] not in roles:
			return True
		else:
			return False


async def dm_check(ctx):
	if ctx.message.channel.is_private:
		return True
	else:
		return False

async def get_tweet():
	await client.wait_until_ready()
	while not client.is_closed:
			await asyncio.sleep(2)
			global lasttweet
			if settings.swtorUpdates:
				try:
					auth = tweepy.OAuthHandler(variables.conkey, variables.consec)  # Consumer Key, Consumer Secret
					auth.set_access_token(variables.tokkey, variables.toksec)  # Token key, Token Secret
					api = tweepy.API(auth)  # logs into @Natebot01
					tweet = api.user_timeline("TORCalendar", count=1)
					tweet = tweet[0]  # Gets 50 tweets from user's timeline
					if tweet.text != lasttweet and "Event" in tweet.text:
						lasttweet = tweet.text
						tweet = tweet.text.split(" ")
						tweet.remove(tweet[-1])
						tweet.remove(tweet[0])
						tweet.remove(tweet[0])
						tweet.remove(tweet[0])
						tweet = " ".join(tweet)
						embed = discord.Embed(title = "Star Wars the Old Republic Update", description = tweet,colour = discord.Colour.blue())
						embed.set_author(name="Grimmy",	icon_url=variables.imgid)
						await client.send_message(client.get_channel(settings.swtorUpdateChannel), "A new SW:TOR Update!", embed=embed)
						print("Updating discord: " + tweet)
						await client.change_presence(game=discord.Game(name=tweet))
				except Exception as e:
					print(repr(e))
				await asyncio.sleep(10)

@client.event
async def on_ready():
	print("The bot is now running.")


@client.event
async def on_member_join(member):
	channel = client.get_channel("554246714253508638")
	await message_create(f"Welcome to the Grimm Descent server, {member.mention}.", channel, discord.Colour.teal())
	if settings.defaultRole:
		role = get(member.server.roles, name = settings.role)
		if role:
			await client.add_role(member, role)
		else:
			channel = client.get_channel("203726041456443393")
			await error_create(f"There was an error adding the default role to {member.name}", channel)
	if settings.changeUsernames:
		await message_create("Hey there, I'm Grimmy, a discord bot created for the Grimm Descent server." +
		                          "What's the name of your main character?", member, discord.Colour.light_grey())
		await message_create("Also don't be worried if you see nothing on the server. You have to activate "
		                                  "your account first. :)", member, discord.Colour.green)
		username = await client.wait_for_message(timeout=432000, author=member)
		role = get(member.server.roles, role="unverified")
		await client.add_role(member, role)
		if settings.usernamesAreRoles:
			await client.create_role(name=username.content, colour=discord.Colour(0xE49AB0))
			role = get(member.server.roles, role=username.content)
			if role:
				await client.add_role(member, role)
				await client.send_typing(member)
				role = get(member.server.roles, role="verified")
				await client.add_role(member, role)
				role = get(member.server.roles, role="unverified")
				await client.remove_role(member, role)
				await asyncio.sleep(2)
				await client.send_message(member, f"Your account has now been activated for the server. Welcome {username.content}.")
		else:
			await client.change_nickname(member, username.content) # else, edit the users name
			await client.send_typing(member)
			role = get(member.server.roles, role="verified")
			await client.add_role(member, role)
			role = get(member.server.roles, role="unverified")
			await client.remove_role(member, role)
			await asyncio.sleep(2)
			await message_create(f"Your account has now been activated for the server. Welcome {username.content}.", member, discord.Colour.green())





@commands.command(pass_context=True)
async def grimmy(ctx):
	await message_create(
		f"Thanks for asking about me {ctx.message.author.mention}! I was created by Nate for the Grimm "
		f"Descent guild and am currently running version {version} for {uptime} seconds.", ctx,
		discord.Colour.gold())

@commands.command(pass_context=True)
async def uptime(ctx):
	await message_create(f"I've been online for {uptime} and am on version {version}.")

@client.command(pass_context=True)
async def notes(ctx):
	await message_create("Thanks for asking. No one ever asks. Messaging them to you now.", ctx, discord.Colour.purple(), title="True Love? <3")
	await client.send_message(ctx.message.author, patch_notes)

@client.command(pass_context=True)
async def private(ctx):
	role = get(ctx.message.author.roles, name='private')
	if not await dm_check(ctx) and not role:
		role = get(ctx.message.server.roles, name="private")
		await client.add_roles(ctx.message.author, role)
		await message_create("Private channel established, " + ctx.message.author.mention, ctx, discord.Colour.light_grey())
	else:
		role = get(ctx.message.author.roles, name='private')
		if not role:
			await error_create("There has been an error with that. Use !bug to report a bug.", ctx)
		else:
			await client.remove_roles(ctx.message.author, role)
			await message_create("Private channel removed, " + ctx.message.author.mention, ctx, discord.Colour.light_grey())


@client.command(pass_context=True)
async def allow(ctx, item):
	if not await dm_check(ctx) and await permission(ctx.message.author.roles, 4):
		set = ", ".join(settings.editableSettings)
		if item == "changeUsernames":
			settings.changeUsernames = True
		elif item == "usernamesAreRoles":
			settings.usernamesAreRoles = True
		elif item == "allowCommands":
			settings.allowCommands = True
		elif item == "swtorUpdates":
			settings.swtorUpdates = True
		elif item == "levelSystem":
			settings.levelSystem = True
		elif item == "raffle":
			settings.raffle = True
		else:
			await error_create(f"{item} is not a valid settings.", ctx)
			await message_create(f"Here is a list of editable settings. {set}", ctx, discord.Colour.green(), title="Editable Settings")
			return
		await message_create(f"{item} has been turned on.", ctx, discord.Colour.green())
	else:
		await error_create("You don't have permission to do that.", ctx)


@client.command(pass_context=True)
async def disallow(ctx, item):
	if not await dm_check(ctx) and await permission(ctx.message.author.roles, 4):
		set = ", ".join(settings.editableSettings)
		if item == "changeUsernames":
			settings.changeUsernames = False
		elif item == "usernamesAreRoles":
			settings.usernamesAreRoles = False
		elif item == "allowCommands":
			settings.allowCommands = False
		elif item == "swtorUpdates":
			settings.swtorUpdates = False
		elif item == "levelSystem":
			settings.levelSystem = False
		elif item == "raffle":
			settings.raffle = False
			variables.raffle_ongoing = False
			variables.raffle_time = 0
			variables.raffle_reason = ""
			variables.raffle_users = ["None"]
		else:
			await error_create(f"{item} is not a valid settings.", ctx)
			await message_create(f"Here is a list of editable settings. {set}", ctx, discord.Colour.green(), title="Editable Settings")
			return
		await message_create(f"{item} has been turned off.", ctx, discord.Colour.red())
	else:
		await error_create("You don't have permission to do that.", ctx)


if __name__ == "__main__":
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print(f"{extension} can not be loaded. {repr(error)}")

	client.loop.create_task(get_tweet())
	client.loop.create_task(count_down())
	client.run(token)