# Chatty

## Development

Runt the application using:

```bash
uvicorn app.main:app --reload
```

## Client Guide to the Chat WebSocket Endpoint

### Initiating a Conversation

After establishing the connection, clients can start a new conversation by sending the following JSON message:

```json
{
  "type": "start_conversation"
}
```

Upon successful initiation, the server will respond with a message indicating the ID of the new conversation.

### Resuming a Previous Conversation

If clients have a conversation ID from a previous session and want to resume that conversation, they can send the
following JSON message:

```json
{
  "type": "resume_conversation",
  "conversationId": "[Your_Previous_Conversation_ID]"
}
```

Replace [Your_Previous_Conversation_ID] with the actual ID of the conversation you want to resume.

The server will respond, confirming the conversation's resumption or notifying the client if no matching conversation is
found.

### Sending Messages

Once either a new conversation has been started or a previous one has been resumed, clients can send regular chat
messages in the following format:

```json
{
  "sender": "[Sender_Type]",
  "content": "[Your_Message_Content]"
}
```

Replace [Sender_Type] with the type of sender (e.g., user) and [Your_Message_Content] with the actual content of the
message.

### Receiving Messages

Clients should also be set up to receive messages from the server. This can include responses to their messages or
any other information the server wishes to convey.
