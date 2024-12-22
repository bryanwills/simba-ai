import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, Trash2 } from 'lucide-react';
import ChatMessage from './ChatMessage';
import { config } from '@/config';
import { sendMessage } from '@/lib/api';

interface Message {
  id: string;
  text: string;
  isAi: boolean;
}

const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage.trim(),
      isAi: false,
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send message to API and get response
      const response = await sendMessage(userMessage.text);
      
      // Add AI response
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.message || 'Sorry, I could not process your request.',
        isAi: true,
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      // Handle error
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, something went wrong. Please try again.',
        isAi: true,
      };
      setMessages(prev => [...prev, errorMessage]);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const clearConversation = () => {
    setMessages([]);
  };

  return (
    <div className="flex min-h-screen w-full bg-gray-100 p-2 sm:p-4 md:p-6">
      <Card className="w-full max-w-5xl mx-auto h-[calc(100vh-2rem)] sm:h-[calc(100vh-3rem)] md:h-[calc(100vh-4rem)] flex flex-col shadow-xl">
        <CardHeader className="border-b px-3 sm:px-4 md:px-6 py-2 sm:py-3 md:py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Bot className="h-5 w-5 sm:h-6 sm:w-6 text-blue-500" />
              <CardTitle className="text-lg sm:text-xl font-bold">
                {config.appName}
              </CardTitle>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={clearConversation}
              className="text-gray-500 hover:text-red-500"
              title="Clear conversation"
            >
              <Trash2 className="h-4 w-4 sm:h-5 sm:w-5" />
            </Button>
          </div>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-3 sm:p-4 md:p-6 space-y-4">
          <div className="space-y-4 sm:space-y-6">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                isAi={message.isAi}
                message={message.text}
              />
            ))}
            {isLoading && (
              <div className="flex items-center space-x-2 text-xs sm:text-sm text-gray-500">
                <div className="flex space-x-1">
                  <div className="animate-bounce">.</div>
                  <div className="animate-bounce delay-100">.</div>
                  <div className="animate-bounce delay-200">.</div>
                </div>
                <span>MigiBot is typing</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </CardContent>

        <CardFooter className="border-t p-2 sm:p-3 md:p-4">
          <form onSubmit={handleSubmit} className="flex w-full space-x-2">
            <Input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 text-sm sm:text-base"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              disabled={isLoading || !inputMessage.trim()}
              className="bg-blue-500 hover:bg-blue-600"
              size="icon"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </CardFooter>
      </Card>
    </div>
  );
};

export default ChatApp; 