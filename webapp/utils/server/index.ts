import { Message } from '@/types/chat';
import {
  ParsedEvent,
  ReconnectInterval,
  createParser,
} from 'eventsource-parser';

export class ChatbotError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ChatbotError';
  }
}

export const ChatbotStream = async (
  userMessage: string,
  conversationId: string | null,
  messages: Message[],
) => {
  const url = 'http://localhost:8000/chat'; // Your chatbot endpoint
  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      'X-USER-ID': 'rs-dev-test'
    },
    method: 'POST',
    body: JSON.stringify({
      user_message: userMessage,
      conversation_id: conversationId,
    }),
  });

  if (res.status !== 200) {
    const result = await res.json();
    throw new ChatbotError(
      `Chatbot API returned an error: ${result.message || res.statusText}`,
    );
  }

  const result = await res.json();

  return result.response
};

