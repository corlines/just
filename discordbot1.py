import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'봇이 로그인되었습니다: {bot.user.name}')

@bot.command()
async def embed(ctx, width: int, height: int):
    embed = discord.Embed(title='Multiply Embed', description=f'이것은 가로 {width}번, 세로 {height}번으로 이루어진 Embed입니다.', color=discord.Color.blue())

    field_value = ':yellow_square: ' * width
    fields = [(f'Line {i+1}', field_value, False) for i in range(height)]
    embed.add_fields(*fields)

    await ctx.send(embed=embed)

bot.run('MTA5MTUzMTU4MjM4NjQ3NTAzMg.GlUN53.8P5XHzZ8z4FDgLSoNOMjndxS8K_lph6xnvxbVI')
