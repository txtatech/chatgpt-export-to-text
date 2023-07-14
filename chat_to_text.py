import json

# Load the data from the JSON file
with open("conversations.json", "r") as read_file:
    data = json.load(read_file)

# Find the user's name from the first message in the first conversation
user_name = next(
    (node_details['message']['author']['name']
     for conversation in data
     for node_details in conversation['mapping'].values()
     if node_details.get('message') and node_details['message'].get('author') and node_details['message']['author'].get('role') == 'user'),
    None
)

# Empty list to hold all conversations
all_conversations = []

# Loop through each conversation in the data
for conversation in data:
    conversation_text = []

    for current_node, node_details in conversation['mapping'].items():
        message = node_details.get('message')

        if message:
            author_role = message['author']['role']
            if 'parts' in message['content']:
                content_parts = message['content']['parts']

                # Create conversation text
                text_string = ""
                for part in content_parts:
                    text_string += part

                text_prefix = f"{user_name}: " if author_role == 'user' else "ChatGPT: "
                text_string = text_prefix + text_string

                conversation_text.append(text_string)

    # Add this conversation to the all_conversations
    if conversation_text:
        all_conversations.append("\n".join(conversation_text))

# Convert list of all conversations to single string
all_conversations_string = "\n\n------------------------------\n\n".join(all_conversations)

# Write all conversations to a text file
with open('all_conversations.txt', 'w') as outfile:
    outfile.write(all_conversations_string)

print("File processed successfully. The output was saved as all_conversations.txt")
