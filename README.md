# CPT-KSS-Directory

Website link: https://kssdirectory.vercel.app/

This is a code repository for my ICS4U final project (called CPT), which is a website for KSS Directory. KSS Directory is a student-run resource respository for my high school, and its main selling point is the frequent condensing and public availability of school announcements. However, the repository is currently hosted on a Discord server, which is highly problematic for students because Discord is blocked at school. I therefore decided to create a website for KSS Directory, so that its resources could be accessed on my school's WiFi network.

## Background
Currently, accessing my school’s daily announcements after they have already been played in the morning is difficult. They are posted to the [school website](https://kss.limestone.on.ca/news/daily_announcement___schedule), as can be seen below.

<img src="https://media.discordapp.net/attachments/793318391409541143/1132919330737225758/image.png">

This resource exhibits several issues.
1.	The website only displays announcements that were played in the past week. This is therefore an issue if a student wants to access an older announcement, as there is no official archive present on this website.
2.	The announcements are not condensed and thus contain a lot of information that may be unnecessary for most students. This is needed for in-person announcements so that everything is covered but makes it difficult to navigate after the fact.
3.	The website does not update the announcements page instantly, sometimes taking up to a few days for an announcement to be posted. This is not ideal, as many of the announcements are time sensitive, such as club meeting dates.
4.	The KSS website is somewhat difficult to navigate, as the interface is not very user friendly. As such, it may be difficult to find the announcements page.

To address these concerns, a few of my fellow students and I run a Discord server called KSS Directory, where condensed versions of the school announcements along with club/event-specific pings are sent. This is a great resource, as it allows students to easily find the information that is most important to them. Furthermore, older announcements are not deleted, and so it serves as a proper archive. Below is the same announcement shown above, after being condensed and formatted with pings.

<img src="https://media.discordapp.net/attachments/793318391409541143/1132918952822067281/image.png">

Since Discord is a messaging platform, it sends notifications to users with the messages that have the club-specific pings they want to see. This let's students be more up-to-date with the school activities that they care about.

Though using Discord is very convenient in many ways, it still presents many accessibility-related problems.
1.	Discord requires an account to use its servers, and so the KSS Directory is only accessible to those that have an account. This is problematic, since a significant proportion of the student body does not have or actively use Discord.
2.	Discord is blocked by the firewall of my school’s Wi-Fi network, and so it is virtually impossible to access the KSS Directory Discord Server on school property. There are a few work arounds, but they are not practical or legal for most people. For instance, the firewall can be bypassed using a VPN, but this goes against the code of conduct enforced by my school. Students could also use their own mobile data, but this is impractical because not every student has access to a mobile phone or a mobile data plan.
3.	Opening Discord and navigating the interface is relatively seamless but can still be a bit cumbersome for those who are unfamiliar. As such, the experience of finding past announcements may be a bit difficult.

I therefore decided to design and build a KSS Directory website for my CPT assignment. This addresses many of the aforementioned concerns, while still being a fun and engaging project with many complex parts. The core function is to make the condensed announcements of the Discord server available via an accessible and unblocked website, with more features (like a filter and search function) planned. 


## Project overview

My project is split into three main parts:
1. A Discord bot, which parses announcement data from the current KSS Directory Discord server and stores them as JSON files on a web server.
2. The web server, which accepts HTTP get requests and returns the JSON files requested.
3. The front-end, which renders the data in the JSON files it receives on the screen of the client.

## Discord bot

The Discord bot has a few main functions:
1. Read messages sent to a specified announcement channel, parsing them as announcements.
2. Update a list of roles and their assigned names/categories, based on what is sent to a specified role assignment channel.
3. Send debug messages to a specified debug channel.

More information on the format of the messages can be seen in the user guide [here](https://docs.google.com/document/d/14OjtjYtXnETj6deIOvWdZafpBh44FwMC01dnu9CI8js/edit?usp=sharing).


### Setting up the Discord bot

To get the Discord bot to run, you first need to install [Python](https://www.python.org/downloads/) and [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html#installing), if you have not done so already.

The main file for the Discord bot is called [KSSDr_bot.py](/Bot%20and%20Web%20Server/KSSDr_bot.py)

Unfortunately, the code for the Discord bot provided in this repository does not have the token that is required for the bot to function. It has been removed for security purposes. However, if you'd like to run the code yourself, you can follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) to get your own token. Replace ```token``` in the last line of KSSDr_bot.py with your token.

```python
client.run('token')
```

The bot also references a file in the same directory called [bot_configs.py](/Bot%20and%20Web%20Server/bot_configs.py), which stores a lot of the configuration information for the Discord server. The ones that are likely to be most useful to change are lines in lines 1-11. Change these channel IDs to the IDs of the server you wish to implement this in.
```python
# anceChnl is the channel ID of the announcements channel
# i.e., where the actual announcements are sent
anceChnl = 1131051934703435886

# rolesChnl is the channel ID of the roles assignment channel
# i.e., where the role names and categories are set.
rolesChnl = 1131052452280533112

# debugChnl is the channel ID of the debug channel
# i.e., where the bot sends debug messages, e.g., confirmation messages
debugChnl = 1131051854634164284
```

To start the bot, simply run [KSSDr_bot.py](/Bot%20and%20Web%20Server/KSSDr_bot.py).


## Web server

The web server mainly accepts various HTTP requests sent by the front-end, returning the JSON files requested. It sorts through the JSON files that are created by the [Discord bot](/Bot%20and%20Web%20Server/KSSDr_bot.py) in the [announcements](/Bot%20and%20Web%20Server/announcements) directory, and returns the JSON files that are requested by the front-end.

### Setting up the web server

To get the web server to run, you first need to install [Python](https://www.python.org/downloads/) and [FastAPI](https://fastapi.tiangolo.com/tutorial/#install-fastapi), if you have not done so already.

In the [Bot and Web Server](/Bot%20and%20Web%20Server) directory, run the following command in the terminal. This will start the server locally.
```python
uvicorn main:app --reload
```
More setup instructions can be found [here](https://fastapi.tiangolo.com/tutorial/#run-the-code).


## Front-end

The front-end is coded in NextJS. It parses through the JSON files returned by HTTP requests sent to the web server, and renders them in a specific format to the client.

### Setting up the front-end

To get the front-end to run locally, run the following command in the terminal in the [Front-end](Front-end) directory.

```javascript
npm run dev
```
Note that this will only work if there are already announcements in the [announcements](/Bot%20and%20Web%20Server/announcements) directory, and if the web server is online and functional.

## More information

The bot and web server that are currently in use for the [KSS Directory website](https://kssdirectory.vercel.app/) are hosted on Google Cloud, whereas the front-end itself is hosted by [Vercel](https://vercel.com).
This project was coded by Matthew Kong with zero prior experience in NextJS, React, Javascript, discord.py, and FastAPI.
