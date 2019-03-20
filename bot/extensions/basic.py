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

class basic:
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
	async def joke(self, ctx):
		client = self.client
		await basic.message_create(self, pyjokes.get_joke(language='en', category = 'neutral'), ctx,
		                           discord.Colour.blue(), title="Joke")

	@commands.command(pass_context=True)
	async def help(self, ctx):
		client = self.client
		await client.say(f"Sending you a message now, {ctx.message.author.mention}.")
		await client.send_message(ctx.message.author, f"Here is a list of commands, as well as descriptions. There "
		                                                    f"is also explanation over the commands and how they work. It"
		                                                    f" is updated very frequently with new commands and old "
		                                                    f"commands that have been deleted. {settings.cmds}")

	@commands.command(pass_context=True)
	async def ban(self, ctx, member: discord.Member):
		client = self.client
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 3):
			try:
				await basic.message_create(self, f"User `{member.display_name}` has been banned.", ctx, discord.Colour.red())
				await client.ban(member)
			except Exception as e:
				print(repr(e))
				await basic.error_create(self, "There was an error running that command.", ctx)
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)

	@commands.command(pass_context=True)
	async def kick(self, ctx, member: discord.Member):
		client = self.client
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 2):
			try:
				await basic.message_create(self, f"User `{member.display_name}` has been kicked.", ctx, discord.Colour.red())
				await client.kick(member)
			except Exception as e:
				print(repr(e))
				await basic.error_create(self, "There was an error running that command.", ctx)
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def unban(self, ctx, member: discord.Member):
		client = self.client
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 3):
			try:
				await basic.message_create(self, f"User `{member.display_name}` has been unbanned.", ctx, discord.Colour.blue())
				await client.unban(member)
			except Exception as e:
				print(repr(e))
				await basic.error_create(self, "There was an error running that command.", ctx)
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def bans(self, ctx):
		client = self.client
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 0):
			bans = await client.get_bans(ctx.message.server)
			bans = ", ".join(bans)
			await basic.message_create(self, bans, ctx, color=discord.Colour.red(), title="Bans")
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def prune(self, ctx, days:int=30):
		client = self.client
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 2):
			num = await client.estimate_pruned_member(ctx.message.server, days=days)
			await basic.message_create(self, f"Pruning members would prune {str(num)} members. Would you like to continue?", ctx, discord.Colour.red(), title="Are you sure?")
			reponse = await client.wait_for_message(timeout=10, author=ctx.message.author)
			if str.lower(reponse) == "yes" or str.lower(reponse) == "y":
				await basic.message_create(self, f"Pruning {str(num)} members from the server.", ctx, discord.Colour.light_grey(), title="Pruning.")
				await client.prune_members(ctx.message.server, days=days)
			else:
				await basic.message_create(self,"Pruning canceled.")
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)


	@commands.command(pass_context=True)
	async def invite(self, ctx):
		client = self.client
		if not await basic.dm_check(self, ctx):
			try:
				invite = await client.create_invite(ctx.message.channel, max_age=0)
				await basic.message_create(self, f"Here is your invite, {ctx.message.author.mention}: `{invite.url}`",
				                           ctx, discord.Colour.gold(), title="Invite")
			except Exception as e:
				print(repr(e))
				await basic.error_create(self, "There was an error running that command.", ctx)


	@commands.command(pass_context=True)
	async def bug(self, ctx):
		client = self.client
		now = datetime.datetime.now()
		returnDay = now.strftime("%A, %B %d")
		now = datetime.datetime.now()
		returnTime = now.strftime("%H:%M")
		try:
			await client.send_message(get(client.get_all_members(), id="203726041456443393"),
			f"bug report created by **{ctx.message.author.name}**, {returnDay}, {returnTime}: *{ctx.message.content}*")
			await basic.message_create(self, "Your bug report has been sent to Nate and will be investigated.", ctx,
			                           discord.Colour.lighter_grey(), title="Bug Report")
		except Exception as e:
			print(repr(e))
			await basic.error_create(self, "There was an error running that command.", ctx)


	@commands.command(pass_context=True)
	async def clear(self, ctx, amount=99):
		client = self.client
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 1):
			if amount > 99:
				await basic.error_create("You can only delete up to 99 messages.", ctx)
			else:
				await basic.message_create(self, f"Deleting the last {amount} messages.", ctx, discord.Colour.red())
				await asyncio.sleep(2)
				channel = ctx.message.channel
				async for message in client.logs_from(channel, limit=int(amount) + 1):
					await client.delete_message(message)
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)

	@commands.command(pass_context=True)
	async def perm(self, ctx, member:discord.Member=None):
		if not member:
			member = ctx.message.author
		for role in member.roles:
			for set_role in settings.roles:
				if role.name == set_role:
					await basic.message_create(self, f"The user {member.mention} has a permission level of {settings.roles.index(set_role)}.",
					                           ctx, discord.Colour.dark_red(), title="Permissions")

	async def namereset(self, member):
		client = self.client
		if settings.changeUsernames:
			role = get(member.server.roles, role="verified")
			if role:
				await client.remove_role(member, role)
			await client.send_message(member,
			                          "Hey there, I'm Grimmy, a discord bot created for the Grimm Descent server." +
			                          "What's the name of your main character?")
			await client.send_message(member,
			                          "Also don't be worried if you see nothing on the server. Your account is being reset.")
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
					await client.send_message(member,
					                          f"Your account has now been activated for the server. Welcome back, {username.content}.")
			else:
				await client.change_nickname(member, username.content)  # else, edit the users name
				await client.send_typing(member)
				role = get(member.server.roles, role="verified")
				await client.add_role(member, role)
				role = get(member.server.roles, role="unverified")
				await client.remove_role(member, role)
				await asyncio.sleep(2)
				await client.send_message(member,
				                          f"Your account has now been activated for the server. Welcome back, {username.content}.")

	@commands.command(pass_context=True)
	async def reset(self, ctx, member: discord.Member=None):
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 2):
			if not member:
				await basic.error_create(self, "You need to specify a member to reset.", ctx)
				return
			await basic.message_create(self, f"Username reset has been intitated to {member.display_name}.", ctx, discord.Colour.red(), title="Name Reset")
			await basic.namereset(member)
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)

	@commands.command(pass_context=True)
	async def editname(self, ctx, member:discord.Member=None, name=None):
		client = self.client
		if not name:
			await basic.error_create(self, "You have to specify the name I should change {member.mention} to.")
			return
		if not member:
			await basic.error_create(self, "You have to specify the member I should change the name of.")
			return
		if not await basic.dm_check(self, ctx) and await basic.permission(self, ctx.message.author.roles, 1):
			try:
				await client.change_nickname(member=member,nickname=name)
				await basic.message_create(self, f"{member.mention} has been updated.", ctx, discord.Colour.green(), title="Name Change")
			except:
				await basic.error_create(self, "There was an error with that command.", ctx)
		else:
			await basic.error_create(self, "You don't have permission to do that.", ctx)

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
	client.add_cog(basic(client))