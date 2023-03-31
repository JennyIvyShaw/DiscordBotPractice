from datetime import datetime
import discord
import asyncio
import projectTimeConversion as ptc
from datetime import timedelta


#Jenny Shaw 



#Method the main class runs, makes a connection to the discord client and bot, passes data as arguements 
def run_discord_bot(data):
    reminders = data['reminders']

    #Creating a connection the the bot and the client
    #Note the token must be added 
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    

    #Method the takes the reminder, reminder message, and reminder id as arguements and waits to send message
    #After message has been sent to the client the message is deleted from the array
    async def send_reminder(reminder, message, reminderId):
        await message.channel.send(f"Reminder: {reminder}")
        del reminders[reminderId]


    #Method prints all reminders in a formatted string 
    def print_all_reminders():
        result = ''
        for id, reminder in reminders.items():
            result += 'ID: ' + str(id) + '\nMESSAGE: '+ reminder['message'] + "\nTIME: " + reminder['time'].strftime("%d/%m/%Y %H:%M:%S") + '\n----------------------------\n'
        return result

    #Prints message to the console when the Bot is successfully running 
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')


    #Main functionality of the Bot 
    @client.event
    async def on_message(message, data=data):
        if message.author == client.user:
            return
        
             
        #If user enter !list the print_all_reminders method is called 
        if message.content.startswith('!list'):
            await message.channel.send(f"YOUR ACTIVE REMINDERS:\n----------------------------\n{print_all_reminders()}")


        #If user enters !remindme the message is split and a reminder is created 
        if message.content.startswith('!remindme'):
            #Get the reminder time and message from the user's input
            _, time_str, reminder_msg = message.content.split(maxsplit=2)
            #Gettimg the time rate from the string
            time_rate = reminder_msg[:1]
            #Getting the contents of the reminder message    
            reminder_msg = reminder_msg[1:]
            
                        
            #Convert time into seconds by calling the get_conversion method 
            total_seconds = ptc.get_conversion(time_str, time_rate) 
            if total_seconds > 0: 
                #Create a reminder thread and then stores the reminder in array 
                loop = asyncio.get_event_loop()
                reminderThread = loop.call_later(total_seconds, asyncio.create_task, send_reminder(reminder_msg, message, data['currentReminderId']))
                reminders[data['currentReminderId']] = {
                    "thread": reminderThread, 
                    "message": reminder_msg, 
                    "name": client.user.name,
                    "time": datetime.now() + timedelta(seconds = total_seconds) 
                }
                data['currentReminderId'] += 1
                #Confirmation message is sent to the user after setting a reminder
                await message.channel.send("Your reminder has been set!")

            if total_seconds == 0:
                await message.channel.send("Sorry your reminder was not set, error with format, please try again.")
            
    
       #If the user enters !cancel with the number of the reminder it is then cancelled and will no longer send
        if message.content.startswith('!cancel'):
            _, id = message.content.split(maxsplit=2)
            intId = int(id)
            if (intId in reminders):
                    reminders[intId]['thread'].cancel()
                    del reminders[intId]
                    await message.channel.send("Your reminder has been cancelled")



        #If the user enters !help the bot will print out a description of what functions are avaliable to the user and how to use them 
        if message.content.startswith('!help'):
            await message.channel.send(f"Hi, I'm the Reminder Bot! Here are the available options\n"
                                       +"---------------------------------------------------------------------------------------------\n"
                                       +"1. !remindme\n\tTo set a new reminder, available in s-seconds, m-minutes, h-hours, or d-days!\n"
                                       +"\tfor example: !remindme 5 m Take the dog out for a walk!\n\n"
                                       +"2. !list\n\tTo list all your active reminders\n\n"
                                       +"3. !cancel\n\tTo cancel a reminder, enter the reminder number directly beside\n"
                                       +"---------------------------------------------------------------------------------------------")

    client.run(TOKEN)

