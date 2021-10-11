import discord
from discord.ext import commands
import json

"""
TASKS:

1. Events - tracking user connection to the channel ([user_name] connected to the channel / [user_name] left channel).
2. Commands - create a .help command to display the bot's greeting text.
3. Kick / Ban / Unban - add the kick feature using the .kick [user_name], ban .ban [user_name] and unban commands, respectively .unban [user_name]
4. Level system - create a level system for users (upgrade the user level every 20 messages).
"""



intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', intents = intents, help_command=None)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

    print('------')



#  TASK # 1

@client.event
async def on_member_join(member):
    channels = member.guild.text_channels
    await channels[0].send(f'{member.name} connected to the channel')

    with open('users.json') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.event
async def on_member_remove(member):
    print(f'{member.name} left channel')


# TASK #2

@client.command()
async def help(context):
    await context.send("Welcom to test bot!")



# TASK #3

@client.command()
async def ban( ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been buned')


@client.command()
async def unban( ctx, member):
    
    user_id = member[3:]
    user_id = user_id[:-1]
    member  = await client.fetch_user(user_id)
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

        if user == member:
            await ctx.guild.unban(user)
            await ctx.send(f'User {member} has been unbuned')
            return
    

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kick')



# TASK #4

@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 1)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await client.process_commands(message)



async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience/20)
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')


client.run('')