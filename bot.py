import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', intents = intents, help_command=None)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

    print('------')
@client.event
async def on_member_join(member):
    print(f'{member.name} connected to the channel')

    with open('users.json') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@client.event
async def on_member_remove(member):
    print(f'{member.name} left channel')




@client.command()
async def help(context):
    await context.send("Welcom to test bot!")


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
        users[f'{user.id}']['level'] = 1


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


client.run('ODk0NjY2NzM1NTkwOTY5Mzc0.YVtVUw.0rBVi6t4v8jaF2zGeGevnUrwAlY')