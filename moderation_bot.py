import discord
import spacy
from transformers import pipeline

# Load NLP models
print("Loading Spacy model...")
nlp = spacy.load("en_core_web_sm")
print("Spacy model loaded.")
toxicity_classifier = pipeline("text-classification", model="facebook/bart-large-mnli")
print("Toxicity classifier loaded.")

# Set up Discord bot
TOKEN = # Your bot's token goes here

# Enable intents
intents = discord.Intents.default()
intents.messages = True  # To read messages
intents.message_content = True  # To access message content

client = discord.Client(intents=intents)

# List of banned words
banned_words = ["stupid", "idiot", "dumb", "moron", "fool"]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    print(f"Bot is ready and logged in!")

@client.event
async def on_message(message):
    print(f"--- Debugging on_message ---")
    
    # Check if the message is from the bot itself
    if message.author == client.user:
        print("Ignoring bot's own message.")
        return  # Ignore bot messages

    # Print message content and author for debugging
    print(f"Received message from {message.author}: {message.content}")

    # Ensure message content is not empty
    if not message.content:
        print("Warning: Message content is empty.")
    
    text = message.content.lower()

    # Debugging banned word check
    print(f"Checking for banned words in the message: {text}")
    # Check for banned words
    if any(word in text for word in banned_words):
        print(f"Detected banned word in message: {text}")
        await message.delete()
        await message.channel.send(f"🚨 That's a naughty word! {message.author.mention}!")
        return  # Prevent toxicity classifier from running after banning


    # Debugging NLP Toxicity Classification
    print("Running toxicity classification...")
    toxicity_score = toxicity_classifier(text)[0]
    print(f"Toxicity score: {toxicity_score['score']}, Label: {toxicity_score['label']}")

    if toxicity_score["label"] == "toxic" and toxicity_score["score"] > 0.85:
        print(f"Message flagged as toxic with score: {toxicity_score['score']}")
        await message.delete()
        await message.channel.send(f"🚨 Message flagged for toxicity, {message.author.mention}!")
        return

# Run the bot
print("Starting the bot...")
client.run(TOKEN)
