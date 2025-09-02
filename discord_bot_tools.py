import discord




async def send_message(bot, channelId, title, color: discord.Color,  paragraphs : list = None):
    """Send a message to a Discord channel.

    Args:
        bot: The Discord bot instance.
        channelId: The ID of the channel to send the message to.
        title: The title of the embed message.
        paragraphs: A list of tuples, each containing a paragraph title and content.
        color: The color of the embed message.    
    """
    embed = discord.Embed(title=title, description=paragraphs, color=color)
    for p in paragraphs:
        embed.add_field(name=p[0], value=p[1], inline=False)
    channel = bot.get_channel(channelId)
    if (channel == None):
         print("ERROR : something weird happens while bot was sending the message...")
    else:
        await channel.send(embed=embed)



class ColorMsg(Enum):
    BLEU = discord.Color.blue()