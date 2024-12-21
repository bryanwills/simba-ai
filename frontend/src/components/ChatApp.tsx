import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "./ui/card"
import { Send, Bot, Trash2 } from 'lucide-react'

interface Message {
  id: number;
  text: string;
  isAi: boolean;
}

const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello! I'm MigiBot, your AI assistant. How can I help you today?",
      isAi: true,
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const newMessage: Message = {
      id: messages.length + 1,
      text: inputMessage,
      isAi: false,
    };
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Simulate AI response - Replace with actual API call
    setTimeout(() => {
      const aiResponse: Message = {
        id: messages.length + 2,
        text: "I'm a demo AI response. Connect me to your backend to make me functional!",
        isAi: true,
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1000);
  };

  const clearConversation = () => {
    setMessages([{
      id: 1,
      text: "Hello! I'm MigiBot, your AI assistant. How can I help you today?",
      isAi: true,
    }]);
  };

  return (
    <div className="flex h-screen bg-gray-100 items-center justify-center p-4">
      <Card className="w-full max-w-4xl h-[800px] flex flex-col shadow-xl">
        <CardHeader className="border-b px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Bot className="h-6 w-6 text-blue-500" />
              <CardTitle className="text-xl font-bold">MigiBot Assistant</CardTitle>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={clearConversation}
              className="text-gray-500 hover:text-red-500"
              title="Clear conversation"
            >
              <Trash2 className="h-5 w-5" />
            </Button>
          </div>
        </CardHeader>

        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
          <div className="space-y-6">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                isAi={message.isAi}
                message={message.text}
              />
            ))}
            {isLoading && (
              <div className="flex items-center space-x-2 text-sm text-gray-500">
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

        <CardFooter className="border-t p-4">
          <form onSubmit={handleSubmit} className="flex w-full space-x-2">
            <Input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              disabled={isLoading || !inputMessage.trim()}
              className="bg-blue-500 hover:bg-blue-600"
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