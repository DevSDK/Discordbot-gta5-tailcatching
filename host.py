import discord
from discord.ext.commands import Bot
import random
import traceback

token_file = open("res/token.ign", "r")
TOKEN = token_file.read()


client = Bot(command_prefix='%')

color_table = []
player_count = 0
player_table = []

def getTarget(i):
    i = i - 1
    if i < 0:
        i = player_count - 1
    return i


@client.command(pass_context=True)
async def start(ctx, *members: discord.User):
    global player_count

    if (player_count > 0):
        await client.say("게임이 이미 진행중입니다")
        return

    with open('res/color.txt', mode='r', encoding='utf-8-sig') as f:
        lines = f.read().splitlines()
        print(lines)

    color_table.extend(lines)
    player_count = len(members)
    for user in members:
        player_table.append(user.name)

    if (len(members) > len(color_table)):
        await client.say("Not enough colors than user. Please add more color")
        return

    #Player Shufflei
    random.shuffle(player_table)

    await client.say("Game start")
    await client.say("Player number: " + str(player_count))
    await client.say("Color count: " + str(len(color_table)))
    del color_table[player_count : len(color_table)]

@client.command()
async def stop():
    color_table.clear()
    player_table.clear()
    global player_count
    player_count = 0

    await client.say("Game Stoped")


@client.command(pass_context=True)
async def myinfo(ctx):
    await client.say('{0} 의 꼬리 색깔은?'.format(ctx.message.author))
    try:
        index = player_table.index(ctx.message.author.name)
    except ValueError:
        await client.say("유저정보가 없습니다. 게임에 참여하고 있는지 확인해주세요")
        return
    await client.say(color_table[index])
    await client.say("잡아야 하는 색깔은?")
    await client.say(color_table[getTarget(index)])


@client.command(pass_context=True)
async def kill(ctx, user : discord.User):
    global player_count
    try:
        current_user_index = player_table.index(ctx.message.author.name)
    except ValueError:
        await client.say("유저정보가 없습니다. 게임에 참여하고 있는지 확인해주세요")
    
    target_user_index = getTarget(current_user_index) 
    if(player_table[target_user_index] == user.name):
        await client.say("축하합니다. 올바른 상대를 잡으셨습니다. 죽인 상대에게 연락을 취해 이 사실을 알리고, 부하로 삼으십시오")
        del player_table[target_user_index]
        del color_table[target_user_index]
        player_count = player_count - 1
    else:
        await client.say("안타깝지만 당신은 죽이지 말아야 할 상대를 죽였습니다. 당신을 쫒고 있는 유저는 \"" + str(player_table[getTarget(current_user_index)]) + "\" 입니다. 당신을 쫒고있는 유저에게 조용히 연락하여 부하가 되십시오. 들키지 않도록 조심하십시오.")
        del player_table[current_user_index]
        del color_table[current_user_index]
        player_count = player_count - 1
        


@client.event
async def on_command_error(error,ctx):
    print(error)
    print(ctx.command)
    await discord.ext.commands.bot._default_help_command(ctx, str(ctx.command))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
