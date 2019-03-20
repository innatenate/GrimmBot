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

class roles:
	def __init__(self, client):
		self.client = client

	async def error_create(self, error, ctx):
		client = self.client
		embed = discord.Embed(title="ERROR", description=error, colour=discord.Colour.red())
		await client.send_message(ctx.message.channel, embed=embed)
		await client.add_reaction(ctx.message, emoji="⛔")

	async def message_create(self, msg, ctx, color, title=None):
		client = self.client
		if title:
			embed = discord.Embed(title=title, description=msg, colour=color)
		else:
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


	@commands.command(pass_context=True)
	async def addrole(self, ctx, member: discord.member, role: discord.role):
		client = self.client
		if not await roles.dm_check(self, ctx) and await roles.permission(self, ctx.message.author.roles, 2):
			try:
				role = get(ctx.message.server.roles, name=role)
				await client.add_roles(member, role)
			except Exception as e:
				print(repr(e))
				await roles.error_create(self, "There was an error with that command.", ctx)
		else:
			await roles.error_create(self, "You don't have permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def ranked(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Ranked")
			if not role:
				role = get(ctx.message.server.roles, name="Ranked")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you would like to do Ranked PvP.", ctx, color = discord.Colour.red(), title="Go get 'em boys")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the Ranked PvP signal from your roles.", ctx, color = discord.Color.light_grey(), title="I think I left my stove on")

	@commands.command(pass_context=True)
	async def pvp(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="PvP")
			if not role:
				role = get(ctx.message.server.roles, name="PvP")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you would like to do PvP.", ctx,
				                           color=discord.Colour.dark_red(), title="Go get 'em boys, but not as cool as Ranked PvP")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the PvP signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="Nevermind this is boring")

	@commands.command(pass_context=True)
	async def raid(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Raids")
			if not role:
				role = get(ctx.message.server.roles, name="Raids")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you would like to do Raids.", ctx,
				                           color=discord.Colour.red(), title="LEEEERROOOYYYY JEEENNKKIINNSSS")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the Raids signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="On second thought...")

	@commands.command(pass_context=True)
	async def ops(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Operations")
			if not role:
				role = get(ctx.message.server.roles, name="Operations")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you would like to do Operations.", ctx,
				                           color=discord.Colour.blue(), title="Rodger Rodger, 10-4")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the Operations signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="Too scary for me")

	@commands.command(pass_context=True)
	async def fp(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Flashpoints")
			if not role:
				role = get(ctx.message.server.roles, name="Flashpoints")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you would like to do Flashpoints.", ctx,
				                           color=discord.Colour.dark_blue(), title="Quick n' ez exp")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the Flashpoints signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="Nevermind, I'm stuck doing KotFE")

	@commands.command(pass_context=True)
	async def heal(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Healer")
			if not role:
				role = get(ctx.message.server.roles, name="Healer")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you are a healer.", ctx,
				                           color=discord.Colour.green(), title="I'll stay in the back while you guys run around")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the healer signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="Nevermind, I like slashy slashy more")


	@commands.command(pass_context=True)
	async def damage(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Damage")
			if not role:
				role = get(ctx.message.server.roles, name="Damage")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you are a DPS.", ctx,
				                           color=discord.Colour.red(), title="Let me just run into the room with the boss real quick...")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the DPS signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="My healers suck")	@commands.command(pass_context=True)

	@commands.command(pass_context=True)
	async def tank(self, ctx):
		client = self.client
		if not await roles.dm_check(self, ctx):
			role = get(ctx.message.author.roles, name="Tank")
			if not role:
				role = get(ctx.message.server.roles, name="Tank")
				await client.add_roles(ctx.message.author, role)
				await roles.message_create(self, "You have signaled that you are a tank.", ctx,
				                           color=discord.Colour.blue(), title="Healers are my slaves now")
			else:
				await client.remove_roles(ctx.message.author, role)
				await roles.message_create(self, "You have removed the tank signal from your roles.", ctx,
				                           color=discord.Color.light_grey(), title="My healers suck")

def setup(client):
	client.add_cog(roles(client))