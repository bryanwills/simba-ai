import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, Trash2 } from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import { config } from '@/config';
import { sendMessage } from '@/lib/api';

interface Message {
  id: string;
  text: string;
  isAi: boolean;
  streaming?: boolean;
  followUpQuestions?: string[];
}

interface StreamMarker {
  status: "start" | "end";
  node: string;
  details: string;
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

    const timestamp = Date.now();
    
    // Add user message
    const userMessage: Message = {
      id: `user-${timestamp}`,
      text: inputMessage.trim(),
      isAi: false,
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${config.apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.text
        }),
      });

      if (!response.ok || !response.body) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let currentResponse = '';
      let currentQuestions = '';
      let streamStarted = false;
      let questionsStreamStarted = false;
      let botMessageId = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        console.log('Received chunk:', chunk); // Debug log
        
        try {
          const marker = JSON.parse(chunk) as StreamMarker;
          
          if (marker.status === "start" && marker.node === "generate") {
            botMessageId = `bot-${timestamp}`;
            streamStarted = true;
            setMessages(prev => [...prev, {
              id: botMessageId,
              text: '',
              isAi: true,
              streaming: true,
              followUpQuestions: [] // Initialize empty array
            }]);
            continue;
          }
          
          if (marker.status === "start" && marker.node === "transform_query") {
            questionsStreamStarted = true;
            currentQuestions = ''; // Reset questions buffer
            // Show loading state for questions
            setMessages(prev => {
              const newMessages = [...prev];
              const lastMessage = newMessages[newMessages.length - 1];
              if (lastMessage && lastMessage.id === botMessageId) {
                lastMessage.followUpQuestions = ['...'];
                lastMessage.streaming = true;
              }
              return [...newMessages];
            });
            continue;
          }

          if (marker.status === "end" && marker.node === "transform_query") {
            // Split the questions text into an array
            const questions = currentQuestions
              .split('\n')
              .map(q => q.trim())
              .filter(q => q.length > 0);

            console.log('Parsed questions:', questions); // Debug log
            
            setMessages(prev => {
              const newMessages = [...prev];
              const lastMessage = newMessages[newMessages.length - 1];
              if (lastMessage && lastMessage.id === botMessageId) {
                lastMessage.followUpQuestions = questions;
                lastMessage.streaming = false;
              }
              return [...newMessages];
            });
            
            questionsStreamStarted = false;
            continue;
          }

        } catch (parseError) {
          // Not a JSON marker, treat as content
          if (streamStarted && !questionsStreamStarted) {
            currentResponse += chunk;
            setMessages(prev => {
              const newMessages = [...prev];
              const lastMessage = newMessages[newMessages.length - 1];
              if (lastMessage && lastMessage.id === botMessageId) {
                lastMessage.text = currentResponse;
              }
              return [...newMessages];
            });
          } else if (questionsStreamStarted) {
            currentQuestions += chunk;
          }
        }
      }

    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        text: 'Sorry, something went wrong. Please try again.',
        isAi: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearConversation = () => {
    setMessages([]);
  };

  const handleFollowUpClick = (question: string) => {
    setInputMessage(question);
    const fakeEvent = { preventDefault: () => {} } as React.FormEvent;
    handleSubmit(fakeEvent);
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
                streaming={message.streaming}
                followUpQuestions={message.followUpQuestions}
                onFollowUpClick={handleFollowUpClick}
              />
            ))}
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