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
import bot

# Secondary Imports
from discord.ext import commands
from discord.utils import get
from modules.universal import variables
from modules.settings import settings

class raffle:

	def __init__(self, client):
		self.client = client

	async def error_create(self, error, ctx):
		client = self.client
		embed = discord.Embed(title="ERROR", description=error, colour=discord.Colour.red())
		await client.send_message(ctx.message.channel, embed=embed)
		await client.add_reaction(ctx.message, emoji="⛔")

	async def message_create(self, msg, ctx, color):
		client = self.client
		embed = discord.Embed(title="Grimmy", description=msg, colour=color)
		await client.send_message(ctx.message.channel, embed=embed)
		await client.add_reaction(ctx.message, emoji="💚")

	async def permission(self, roles, perm):
		client = self.client
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
			if settings.roles[0] not in roles and settings.roles[1] not in roles and settings.roles[
				2] not in roles and settings.roles[3] not in roles:
				return True
			else:
				return False

	async def dm_check(self, ctx):
		client = self.client
		if ctx.message.channel.is_private:
			return True
		else:
			return False

	async def raffleCheck(self):
		client = self.client
		while 1:
			if variables.raffle_ongoing:
				if variables.raffle_time > 0:
					variables.raffle_time -= 1
					await client.change_presence(game=discord.Game(f"Raffle Ongoing. {variables.raffle_time} hours left: {variables.raffle_reason}"))
					await asyncio.sleep(1)
				else:
					winner = variables.raffle_users[random.randrange(len(variables.raffle_users) - 1)]
					await client.send_message(client.get_channel("554478385691099269"),
					                          f"{winner} has won the raffle for {variables.raffle_reason}.")
					await client.change_presence(game=discord.Game("The raffle has been completed."))
					variables.raffle_time = 0
					variables.raffle_reason = ""
					variables.raffle_users = ["None"]
					variables.raffle_ongoing = False
			await asyncio.sleep(1)


	@commands.command(pass_context=True)
	async def newraffle(self, ctx, time=24, *args):
		client = self.client
		if not args:
			args = "No reason/prize specified."
		if not settings.raffle:
			await raffle.error_create(self, "Raffles are not currently allowed in this server.", ctx)
			return
		if not await raffle.dm_check(self, ctx) and await raffle.permission(self, ctx.message.author.roles, 3):
			if variables.raffle_ongoing:
				await raffle.error_create(self, "There is already an ongoing raffle.", ctx)
				return
			variables.raffleUsers = [ctx.message.author.name]
			variables.raffle_ongoing = True
			variables.raffle_time = time * 60 * 60
			variables.raffle_reason = " ".join(args)
			await raffle.message_create(self, f"Your raffle has been activated. It will continue for {str(time)} hours and the "
			                         f"prize/reason is {variables.raffle_reason}", ctx, discord.Colour.green())
		else:
			await raffle.error_create(self, "You don't have permission to do that.", ctx)

	@commands.command(pass_context=True)
	async def raffle(self, ctx):
		client = self.client
		if not settings.raffle:
			await raffle.error_create(self, "Raffles are not currently allowed in this server.", ctx)
			return
		if variables.raffle_ongoing:
			await raffle.message_create(self, f"There is currently a raffle going on. The remaining time is {str(round(variables.raffle_time/60/60))} "
			                         f"hours remaining and the prize/reason is {variables.raffle_reason}.", ctx, discord.Colour.green())
		else:
			await raffle.message_create(self, "There is currently no raffle going on.", ctx, discord.Colour.light_grey())


	@commands.command(pass_context=True)
	async def joinraffle(self, ctx):
		client = self.client
		if not await raffle.dm_check(self, ctx) and await raffle.permission(self, ctx.message.author.roles, settings.rafflePerm):
			if not settings.raffle:
				await raffle.error_create(self, "Raffles are not currently allowed in this server.", ctx)
				return
			if not variables.raffle_ongoing:
				await raffle.error_create(self, "There is no ongoing raffle.", ctx)
			else:
				if ctx.message.author.name in variables.raffle_users:
					await raffle.error_create(self, "You have already used your raffle ticket.", ctx)
				else:
					variables.raffle_users.append(ctx.message.author.name)
					await raffle.message_create(self, f"{ctx.message.author.mention} has been entered into the raffle."
					                         f" The remaining time is {str(round(variables.raffle_time / 60 / 60))} "
					                         f"hours remaining and the prize/reason is {variables.raffle_reason}.",
					                         ctx, discord.Colour.green())
		else:
			await raffle.error_create(self, "You don't have permission to do that.", ctx)

	@commands.command(pass_context=True)
	async def raffleperm(self, ctx, num:None):
		client = self.client
		if not await raffle.dm_check(self, ctx) and await raffle.permission(self, ctx.message.author.roles, 3):
			if not num:
				await raffle.error_create(self, "You'll need to specify a number. 0 means anyone can join. The highest permission is 5.", ctx)
			elif num > 5:
				await raffle.error_create(self, "That number is too high. 0 means anyone can join. The highest permission is 5.", ctx)
			else:
				settings.rafflePerm = num
				await raffle.message_create(self, "The permission value for raffles has now been modified.", ctx, discord.Colour.green())
		else:
			await raffle.error_create(self, "You don't have permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def cancelraffle(self, ctx):
		client = self.client
		if not await raffle.dm_check(self, ctx) and await raffle.permission(self, ctx.message.author.roles, 3):
			await raffle.message_create(self, "Are you sure you want to end the raffle?", ctx, discord.Colour.red())
			response = await client.wait_for_message(timeout=5, author=ctx.message.author)
			if not response:
				await raffle.message_create(self, "The raffle has not been canceled.", ctx, discord.Colour.green())
			elif str.lower(response.content) == "yes" or str.lower(response.content) == "y":
				variables.raffle_time = 0
				variables.raffle_reason = ""
				variables.raffle_users = ["None"]
				await raffle.message_create(self, "The raffle has been canceled.", ctx, discord.Colour.red())
			elif str.lower(response.content) == "no" or str.lower(response.content) == "n":
				await raffle.message_create(self, "The raffle has not been canceled.", ctx, discord.Colour.green())
			else:
				await raffle.message_create(self, "The raffle has not been canceled.", ctx, discord.Colour.green())
		else:
			await raffle.error_create(self, "You don't have permission to do that.", ctx)

	async def on_error(self, ctx, error):
		client = self.client
		now = datetime.datetime.now()
		returnDay = now.strftime("%A, %B %d")
		now = datetime.datetime.now()
		returnTime = now.strftime("%H:%M")
		await client.send_message(get(client.get_all_members(), id="203726041456443393"),
		f"bug report autocreated: **{ctx.message.author.name}**, {returnDay}, {returnTime}: *{ctx.message.content}*, {repr(error)}")
		print(repr(error))

def setup(client):
	client.add_cog(raffle(client))