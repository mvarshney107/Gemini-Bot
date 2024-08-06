import discord
from discord.ext import commands
import time

import google.generativeai as genai 

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

genai.configure(api_key="GEMINI API KEY")  # replace with relevant gemini api key
model = genai.GenerativeModel('gemini-1.5-flash')


def contextual_response(prompt, context):
    response = model.generate_content(f"Answer this following prompt in 1000 characters or less (this is a hard limit and cannot be exceeded under any circumstances): {prompt}. Here is the message history of this particular conversation for context (there may be none): {context}")
    return response.text


def length_check_DM(user_id):
    if len(DM_context[user_id]) > 6:
        DM_context[user_id].clear()
        return True
    else:
        return False


def length_check_server(user_id):
    if len(server_context[user_id]) > 6:
        server_context[user_id].clear()
        return True
    else:
        return False


@bot.event
async def on_ready():
    print(f"Online: {bot.user.name}")


DM_context = {}
server_context = {}


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):  # if user sends a direct message
        user_id = message.author.id  # takes note of which user it is
        if user_id not in DM_context:  # if this is a new user
            DM_context[user_id] = [message.content]
            await message.channel.send("Hello! This is your first time DMing me. Feel free to chat about (almost) anything. NOTE: to keep context, reply to messages. Context limit is 6 messages. Sending a message that isn't a reply will reset the context.")

        if message.reference:  # if the message from the user is a reply
            reference_message = await message.channel.fetch_message(message.reference.message_id)
            DM_context[user_id].append(reference_message.content)  # adds bot message to context
            DM_context[user_id].append(message.content)  # add user message to context

            if length_check_DM(user_id):  # checks for length of context for the user
                await message.reply("This conversation has exceeded the limit of 6 messages. Please start a new conversation!")
            else:  # if length is not exceeded
                prompt = message.content
                response = contextual_response(prompt, DM_context[user_id])
                await message.reply(response)
        
        else:
            DM_context[user_id].clear()  # reset context
            DM_context[user_id] = [message.content]
            prompt = message.content
            response = contextual_response(prompt, DM_context[user_id])
            await message.reply(response)

    elif bot.user in message.mentions:  # if the message is a ping or reply to the bot
        user_id = message.author.id
        if user_id not in server_context:  # if its a new user
            server_context[user_id] = [message.content]

        if message.reference:  # if the message is a reply
            reference_message = await message.channel.fetch_message(message.reference.message_id)  # fetches original message (that was quoted)
            server_context[user_id].append(reference_message.content)  # adds bot message to context
            server_context[user_id].append(message.content)  # add user message to context
            if length_check_server(user_id):  # checks for length of context for the user
                await message.reply("This conversation has exceeded the limit of 6 messages. Please start a new conversation!")
            else:  # if length is not exceeded
                prompt = message.content
                response = contextual_response(prompt, server_context[user_id])
                await message.reply(response)

        else:  # if the message is a ping
            server_context[user_id].clear()  # reset context
            server_context[user_id] = [message.content]
            prompt = message.content
            response = contextual_response(prompt, server_context[user_id])
            await message.reply(response)


bot.run("DISCORD API KEY")  # replace with relevant discord bot key
