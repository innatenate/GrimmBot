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

class music:

	def __init__(self, client):
		self.client = client
	players = []
	urls = []
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

	@commands.command(pass_context=True)
	async def join(self, ctx):
		client = self.client
		if not await music.dm_check(self, ctx):
			try:
				channel = get(client.get_all_channels(), id="557428063038603285")
				await client.join_voice_channel(channel)
				await music.message_create(self, "Voice channel joined.", ctx, discord.Colour.blue())
			except Exception as e:
				if e == TimeoutError or "OpusNotLoaded()" in str(repr(e)):
					return
				else:
					await music.error_create(self, "There was an error with that. Report it using !bug if you'd like.", ctx)
		else:
			await music.error_create(self, "I can't do that in a direct message channel.", ctx)


	@commands.command(pass_context=True)
	async def leave(self, ctx):
		client = self.client
		if not await music.dm_check(self, ctx):
			server = ctx.message.server
			if not client.is_voice_connected(server):
				await music.error_create(self, "I'm not in a voice channel.", ctx)
			else:
				try:
					voice_client = client.voice_client_in(server)
					await voice_client.disconnect()
					await music.message_create(self, "Voice channel left.", ctx, discord.Colour.blue())
				except Exception as e:
					print(repr(e))
					await music.error_create(self, "There was an error with that. Report it using !bug if you'd like.", ctx)
		else:
			await music.error_create(self, "I can't do that in a direct message channel.", ctx)


	@commands.command(pass_context=True)
	async def play(self, ctx, url):
		client = self.client
		server = ctx.message.server
		if not await music.dm_check(self, ctx):
			if not client.is_voice_connected(server):
				await music.error_create(self, "I can't play music without joining a voice channel.", ctx)
			else:
				try:
					voice_client = client.voice_client_in(server)
					player = await voice_client.create_ytdl_player(url)
					music.players[server.id] = player
					await player.start()
					await music.message_create(self, f"Playing {url} for you now, {ctx.message.author.mention}.", ctx, discord.Colour.dark_blue())
				except Exception as e:
					if "URL" in str(repr(e)):
						await music.error_create(self, "There was an error with the provided URL.", ctx)
		else:
			await music.error_create(self, "I can't do that in a direct message channel.", ctx)


	@commands.command(pass_context=True)
	async def pause(self, ctx):
		client = self.client
		server = ctx.message.server
		if not await music.dm_check(self, ctx):
			if not client.is_voice_connected(server):
				await music.error_create(self, "I can't pause without joining a voice channel.", ctx)
			else:
				try:
					id = server.id
					music.players[id].pause()
					await music.message_create(self, "The music has been paused.", ctx, discord.Colour.orange())
				except:
					await music.error_create(self, "There was an error pausing the music.", ctx)
		else:
			await music.error_create(self, "I can't do that in a direct message channel.", ctx)


	@commands.command(pass_context=True)
	async def resume(self, ctx):
		client = self.client
		server = ctx.message.server
		if not await music.dm_check(self, ctx):
			if not client.is_voice_connected(server):
				await music.error_create(self, "I can't resume without joining a voice channel.", ctx)
			else:
				try:
					id = server.id
					music.players[id].resume()
					await music.message_create(self, "The music has been resumed.", ctx,
					                           discord.Colour.orange())
				except:
					await music.error_create(self, "There was an error resuming the music.", ctx)
		else:
			await music.error_create(self, "I can't do that in a direct message channel.", ctx)


	@commands.command(pass_context=True)
	async def stop(self, ctx):
		client = self.client
		server = ctx.message.server
		if not await music.dm_check(self, ctx):
			if not client.is_voice_connected(server):
				await music.error_create(self, "I can't stop without joining a voice channel.", ctx)
			else:
				try:
					id = server.id
					music.players[id].stop()
					await music.message_create(self, "The music has been stopped.", ctx, discord.Colour.orange())
				except:
					await music.error_create(self, "There was an error stopping the music.", ctx)
		else:
			await music.error_create(self, "I can't do that in a direct message channel.", ctx)

def setup(client):
	client.add_cog(music(client))