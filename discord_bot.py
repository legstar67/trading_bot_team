import discord
from discord.ext import commands, tasks
import os
import dotenv

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        

    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}')
        print('------')
    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.user:
            return
        #debug print to see if the bot is receiving messages
        print(f"Message reçu : {message}")
        print(f"Contenu : {message.content}")
        print(f"Auteur : {message.author}")
        print(f"Pièces jointes : {message.attachments}")
        print(f"Embeds : {message.embeds}")
        if message.content.startswith(self.command_prefix):
            print(f"Received command: {message.content}")
            command = message.content[len(self.command_prefix):].strip()
            if command == 'test':
                await message.channel.send(' test received!!')



if __name__ == "__main__":
    
    dotenv.load_dotenv()
    api_key = os.getenv("API_DISCORD_BOT")
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = MyBot(command_prefix='!', intents=intents)

    bot.run(api_key)
    print("Bot is running...")
    # bot.add_cog(MyBot(command_prefix='!', intents=intents))
    # print("Bot has started successfully.")
