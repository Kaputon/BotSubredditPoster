@bot.event
async def reddit_grab():
    await bot.wait_until_ready()
    
    wait_time = 0 # Time inbetween posts.
    thumb = "whatever.png" # Cosmetic embed junk.
    first_post = False # First post?
    
    main_ID = None #Discord Channel ID for Posts
    check_ID = None # PERSISTENT DATA CHANNEL, Instead of dealing with persistent data on a bot, I simply store the links already posted in a separate Discord channel. 
    # Cringe? Yeah, but it works!
    
    check_channel = bot.get_channel(check_ID)
    previous_posts = [] # Subreddit URLs that have already been posted to Discord.
    
    async for message in check_channel.history(limit=None): # On bot startup, go through each link and add them to the list.
       previous_posts.append(str(message.content))
    await asyncio.sleep(3)


    while True:
        if first_post: # If the first post after the bot has been started is made, change the wait time to 12600 seconds (3.5 hours)
            wait_time = 12600
        await asyncio.sleep(wait_time)
        
        # Store all of the subreddit post data in this dictionary
        post_dict = {
            "Upvotes": [],
            "Post Title": [],
            "Content": [],
            "Url": [],
            "Author": [],
        }
        
        # PRAW API mumbo jumbo
        r = asyncpraw.Reddit(
            client_id="",
            client_secret="",
            user_agent="",
        )
        
        sub = await r.subreddit("truetf2")
        
        # Iterate through 25 'Hot' threads in truetf2
        async for post in sub.hot(limit=25):
            if not (str(post.url) in previous_posts) and not post.stickied and not (str(post.author) == "exaflamer"): # Nothing against exa, he just posts about tourneys.
                post_dict["Upvotes"].append(post.score)
                post_dict["Post Title"].append(post.title)
                post_dict["Content"].append(post.selftext)
                post_dict["Url"].append(post.url)
                post_dict["Author"].append(post.author)
                # Append all the relevant data into the dictionary.
        
        # Find the most upvoted thread and index it to be posted
     
        biggest = max(post_dict["Upvotes"]) # Index the most upvoted post
        chose_post = post_dict["Upvotes"].index(biggest)
        chose_url = post_dict["Url"][chose_post]
        # Send this thread's URL to the check channel and add it to the blacklist.
        previous_posts.append(chose_url)
        await check_channel.send(chose_url)
        
        # Configure the embed.
        nEmbed = discord.Embed(title=post_dict["Post Title"][chose_post],
                               description=str(post_dict["Content"][chose_post])[:509] + "...")
        nEmbed.add_field(name="URL", value=post_dict["Url"][chose_post], inline=False)
        nEmbed.set_thumbnail(url=thumb)
        nEmbed.set_footer(text="r/truetf2", icon_url=bot.user.avatar_url)
        nEmbed.set_author(name="u/" + str(post_dict["Author"][chose_post]), icon_url=thumb)
        channel = bot.get_channel(main_ID)
        await channel.send(embed=nEmbed)
        
        first_post = True

bot.loop.create_task(reddit_grab()) # Create the Discord bot loop.
