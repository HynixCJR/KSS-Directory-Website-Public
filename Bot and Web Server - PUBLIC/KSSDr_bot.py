# This is the main Discord bot file!
# If you want to run the Discord bot, run this file.

# All code written by Matthew Kong.
# Sunday, June 23rd, 2023

# you need discord.py installed to run this
# You can run the following command in command prompt or terminal (if you're on Windows) to install, excluding the '#'
# py -3 -m pip install -U discord.py
import discord

# Importing the bot configs Python file
# I have it set like this because I wanted this file to be basically untouched, so that the server wouldn't break when switching config options
import bot_configs as bc

import json

# Opening the pings.json file
pingsFile = open("pings.json", "r+")
pings = json.loads(pingsFile.read())

# Stuff that initializes the Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# global variables
formattedDate = ""
"""The final date in ISO 8601 format for better file organization"""
anceNum = 1
"""The number of announcements sent so far, excluding the date identifier."""

def iterateSect(msg, mod, iter, iterEnd, endSymb):
    """Iterates through a specified message until it reaches a specific character, returning the full word up to the specified character and the final iterate value."""

    while True:
        if msg[iter] != endSymb:
            mod += msg[iter]
            iter += 1
        else:
            iter += iterEnd
            break

    return mod, iter

async def difChannel(channel, msgTitle, msgDescription, embedColour):
    """Sends an embed message to the specified channel. This function must be called with an "await" in front of it."""

    embed = discord.Embed(colour = embedColour, title = msgTitle, description = msgDescription)
    sendChannel = client.get_channel(channel)
    #await client.wait_until_ready()
    await sendChannel.send(embed = embed)



@client.event
async def on_ready():
    """This function activates when the bot first starts up."""
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """This function activates if a new message is sent."""

    global formattedDate, anceNum
    if message.author == client.user:
        return

    if message.channel.id == bc.anceChnl:
        # Checks if a message was sent the announcements channel
        previousDate = formattedDate

        if message.content.startswith('**'):
            # Trigger for start of new announcement, which starts with a ** to signify the day of the week being bold.

            anceNum = 1
            iterate = 2
            
            # Getting the day of the week
            day = ""
            day, iterate = iterateSect(message.content, day, iterate, 6, "*")

            # Getting the month
            month = ""
            month, iterate = iterateSect(message.content, month, iterate, 1, " ")
            month = bc.months[month.lower()]
            
            # Getting the date
            date = ""

            # Note that I don't use the iterateSect function here because the if statement is different
            while True:
                if ord(str(message.content[iterate])) in range(48,58):
                    date += str(message.content[iterate])
                    iterate += 1
                else:
                    while True:
                        if ord(message.content[iterate]) in range(97,123) or message.content[iterate] == "," or message.content[iterate] == " ":
                            iterate += 1
                        else:
                            break
                    break

            # For the sake of organization, I am making it so that all dates are a length of 2
            if len(date) == 1:
                date = "0" + date

            # Getting the year
            # It's easier to not use the iterateSect function here
            year = ""
            for i in range(iterate, len(message.content)-2):
                year += message.content[i]
            
            # Making the date info into a dictionary
            dateInfo = {
                0: [day, year, month, date]
            }
            
            # Formatting the year, month and date into ISO format, which is better for file organization
            formattedDate = year + month + date

            try:
                # Checking if the announcement file for the specified date exists
                anceData = open("announcements//" + formattedDate + ".json", "r+")
                ance = anceData.read()

                # If there is no error, this sends an error message to the debug channel.
                await difChannel(bc.debugChnl, "**Error!**", "There was an error with the message you sent!\n```" + message.content + "```\nThis date already exists in the database, and so the message you sent has been deleted.", bc.negColour)
                # Deleting the message and resetting the formattedDate to the previousDate.
                await message.delete()
                formattedDate = previousDate

            except:
                # If there are no issues, then proceed.

                # This is just for debugging, which I am keeping because it is useful to see in the console
                print("New JSON file created at announcements/" + formattedDate + ".json")

                # Sending a success message to the Debug Channel, along with the processed data for debugging purposes.
                await difChannel(bc.debugChnl, "**New *Date Identifier* announcement creation successful!**", "The most recent *Date Identifier* announcement was processed successfully. ```" + message.content + "```\nAny club/event announcements you send will henceforth be attached to this Date Identifier (as long as it is formatted it properly), and will be updated as such on the website.\n\nFor debugging purposes, here is what the processed data looks like:\n```" + "Day: " + day + "\n\nYear: " + year + "\nMonth: " + month + "\nDate: " + date + "\n\nJson file name: " + formattedDate + ".JSON```", bc.posColour)

                # Creating a new .json file with the formatted date as its name
                with open("announcements/" + formattedDate + ".json", "w") as json_file:
                    # Writing the date information (the dictionary) to the newly created file
                    json.dump(dateInfo, json_file)

        elif message.content.startswith('<@&'):
            # Mentions are read by the bot as <@&...>, and so this checks if the message starts with a ping.

            if formattedDate != "":
                iterate = 0

                # Getting the role that was pinged
                role_id = ""
                role_id, iterate = iterateSect(message.content, role_id, iterate, 3, " ")
                
                try:
                    # setting the role name and category of the announcement
                    role_name = pings[role_id][0]
                    role_cat = pings[role_id][1]
                except:
                    # warning message
                    await difChannel(bc.debugChnl, "**Role does not have assigned category!**", '**The role you mentioned, ' + role_id + ', does not have an assigned tag. It has been assigned a "miscellaneous" tag for the time being. You can change it in ' + str(bc.rolesChnl), bc.midColour)
                    role_id = role_id.replace("<@&", "")
                    role_id = role_id.replace(">", "")
                    role_name = discord.utils.get(message.guild.roles, id = int(role_id)).name
                    role_cat = "miscellaneous"

                anceBrief = ""
                while True:
                    if message.content[iterate] != "*":
                        anceBrief += message.content[iterate]
                        iterate += 1
                    else:
                        iterate += 6
                        break
                
                anceDtls = ""
                for i in range(iterate, len(message.content)-1):
                    anceDtls += message.content[i]
                
                anceFile = open("announcements/" + formattedDate + ".json", "r+")
                ance = json.loads(anceFile.read())
                
                ance.update({anceNum: [role_cat, role_name, anceBrief, anceDtls]})

                anceNum += 1

                # removes all stuff in json from 0th position
                anceFile.truncate(0)

                # moves cursor back to 0th position
                anceFile.seek(0)

                # json.dumps changes pings to str
                anceFile.write(json.dumps(ance))
                anceFile.flush()
                print(ance)
                
                # Sends confirmation message to debug channel
                await difChannel(bc.debugChnl, "**New *Club/event/info* announcement creation successful!**", "The most recent *Club/event/info* announcement was processed successfully. ```" + message.content + "```\nFor debugging purposes, here is what the processed data looks like:\n```" + "Club/event/info name: " + role_name + "\nClub/event/info category: " + role_cat + "\n\n Brief announcement: " + anceBrief + "\nAnnouncement details: " + anceDtls + "```", bc.posColour)

            else:
                # If there is no prior Date Identifier announcement to refer to

                # Sends error message to debug channel
                await difChannel(bc.debugChnl, "**Error!", "There was an error with the message you sent!\n```" + message.content + "```\nThere is no date associated with your announcement. Please send a properly formatted date first, then send an announcement. Thanks!", bc.negColour)
                await message.delete()

    elif message.channel.id == bc.rolesChnl:
        # Check if message is in the roles channel

        newRoleID = ""
        newRoleName = ""
        newRoleSect = ""

        if message.content.startswith('<@&'):
            # adding or updating the roles

            
            if len(message.content) < 100 and "," in message.content and "<@&" in message.content:
                # Basic error checking (seeing if length is too long, and if there is a comma)

                iterate = 0
                while True:
                    if message.content[iterate] != " ":
                        newRoleID += message.content[iterate]
                        iterate += 1
                    else:
                        iterate += 1
                        break
                while True:
                    if message.content[iterate] != ",":
                        newRoleName += message.content[iterate]
                        iterate += 1
                    else:
                        iterate += 2
                        break
                for i in range(iterate, len(message.content)):
                    newRoleSect += message.content[i]

                pings.update({newRoleID: [newRoleName, newRoleSect]})

                # removes all stuff in json from 0th position
                pingsFile.truncate(0)

                # moves cursor back to 0th position
                pingsFile.seek(0)

                # json.dumps changes pings to str
                pingsFile.write(json.dumps(pings))
                pingsFile.flush()
                print(pings)

            # error messages
            elif len(message.content) > 100:
                await message.channel.send("Sry, I think there was an error. Ur message is too long!")
            elif "," not in message.content:
                await message.channel.send("Sry, I think there was an error. Ur message does not have a comma!")
            elif "<@&" not in message.content:
                await message.channel.send("Sry, I think there was an error. You didn't add a ping!")
        
        elif message.content.startswith('.roles'):
            # Debugging cmd for the admins of the KSS Directory server
            await message.channel.send("Okay, here are the roles!")
            await message.channel.send(pings)
    elif message.channel.id == bc.debugChnl:
        if message.content == ".help":
            await message.channel.send("**Hello there! Thank you for using the KSS Directory bot.\nIt is important that you abide by the standard so that the bot and website can actually work. Here is how to send properly formatted announcements:**\n...")
            await message.channel.send("Full announcements are comprised of two parts: a **Date Identifier**, and the actual **club/event** announcements.\nThe date identifier tells users of the Discord server, as well as this bot, what date your announcement is.\n\nIt must follow this format:\n```\n**{day of the week}**\n\n**{month} {date} {year}**\n```\n\nFor example, here is a properly formatted Date Identifier.\n```\n**SUNDAY**\n\n**July 23rd 2023**```\n\nWhich produces the following:\n\n**SUNDAY**\n\n**July 23rd 2023**\n\n*Note that you MUST include the 'rd', 'st', or 'th' after the date.\nMake sure to not include any spaces or characters other than those that are needed!")
            await message.channel.send("...\nClub/event announcements are the actual announcements for KSS clubs and events.\nTo send one of them, you must first initialize the announcements for the day with a Date Identifier. The announcements that follow will then be linked to that date.\n\nThese announcements follow this specific format:\n```\n@{ping} **{announcement brief}**\n*{announcement details}*``` \n Note that this will not work without each of the parts enclosed in {}.\n\nFor example, here is a properly formatted club/event announcement:\n\n```\n@graphic design **Graphic Design Club meeting today at lunch in room 228**\n> *KSDC winners announced, raffle.*\n```\n\nWhich produces the following:\n\n<@&1038542186284859452> **Graphic Design Club meeting today at lunch in room 228**\n> *KSDC winners announced, raffle.*\n\nFor the bot to recognize the message you sent, please make sure that you only have one space after the ping, and one after the >. Also, please make sure you bold/italicize the announcements as shown!")
            await message.channel.send("...\nThe website also assigns new names and categories for each role. You can assign these roles in #temp-roles. Assigning them follows this format:\n\n```\n@{role} {role name}, {role category}\n```\n\nFor example...\n\n```@graphic design Graphic Design Club, Clubs```\n\nproduces the following message:\n\n<@&1038542186284859452> Graphic Design Club, Clubs\n\nThis assigns the name of Graphic Design Club to <@&1038542186284859452>, and puts it in the Clubs category. If you don't do this, the announcements you send will be grouped under the miscellaneous category, and the club/event name will just be the name of the ping.")
# This is the client ID of the Discord bot
# This is supposed to be confidential, so I've removed it from the code here.
client.run('Put your client ID here')