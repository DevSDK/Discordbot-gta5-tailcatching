import discord
from discord.ext.commands import Bot
import random

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
        player_table.append(user.id)

    if (len(members) > len(color_table)):
        await client.say("Not enough colors than user. Please add more color")
        return

    # Player Shuffle
    random.shuffle(player_table)

    await client.say("Game start")
    await client.say("Player number: " + str(player_count))
    await client.say("Color count: " + str(len(color_table)))


@client.command()
async def stop():
    color_table.clear()
    player_table.clear()
    global player_count
    player_count = 0

    await client.say("Game Stoped")


@client.command(pass_context=True)
async def myinfo(ctx):
    # TODO: Implementation Tale Color
    await client.say('{0} 의 꼬리 색깔은?'.format(ctx.message.author))
    try:
        index = player_table.index(ctx.message.author.id)
    except ValueError:
        await client.say("유저정보가 없습니다. 게임에 참여하고 있는지 확인해주세요")
        return
    await client.say(color_table[index])
    await client.say("잡아야 하는 색깔은?")
    await client.say(color_table[getTarget(index)])


@client.command(pass_context=True)
async def kill(*message):
    # TODO: Implementation Kill
    if len(message) is 0:
        await client.say("죽일 사람을 선택해주세요!!!")
        await client.say("ex)%kill 죽일사람")
        return

    await client.say(message[0])
    await client.say("Need To Implementation!!!!")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
