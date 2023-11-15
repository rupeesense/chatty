import { ChatbotError, ChatbotStream } from '@/utils/server';
import { ChatBody, Message } from '@/types/chat';


export const config = {
  runtime: 'edge',
};

const handler = async (req: Request): Promise<Response> => {
  try {
    const { messages, key } = (await req.json()) as ChatBody; // Assuming ChatBody is your request body type

    // Assuming the last message in the array is the user's message
    const userMessage = messages[messages.length - 1]?.content || "";
    const conversationId = key || null;

    // Call your chatbot service
    const chatbotResponse = await ChatbotStream(userMessage, conversationId, messages);

    // Construct the response
    return new Response(JSON.stringify(chatbotResponse), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error(error);
    if (error instanceof ChatbotError) {
      return new Response('Error', { status: 500, statusText: error.message });
    } 
    else {
      return new Response('Error', { status: 500 });
    }
  }
};

export default handler;
