# Discord-Bot
This is a discord bot for my channel which has a few features:
==============================================================
1. Weather Forecast at 7:30, 12:30 and 18:30 am Perth time to tell the weather and the status
2. Annouces new ongoing episode that is just released based on a website using a logger file
3. Gives roles based on a reaction on a message

TODO:
=======
1. Fix the role removal function as it doesn`t remove the role if the reaction is removed
2. Add a feature to add anime to the log file from discord messages
3. Add sunset and sunrise time
4. Fix weather forecast timing

Git commands:
============
1. **Loging:**\
heroku login
2. Add and Commits:
##git commit -am "message"##
3. Push after add:
##git push heroku master##
4. Scale worker after push:
heroku ps:scale worker=1
5. Check logs:
heroku logs -a sopher-bot
6. View files:
git show master:'file name'
7. Check differences:
git diff
if no differences it will be empty
8. Check status:
git status
9. Check latest version:
git log -1

### Certain files are kept hidden for privacy ###
