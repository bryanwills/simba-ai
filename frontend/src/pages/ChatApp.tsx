import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Bot, Send, Trash2 } from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import { config } from '@/config';
import { cn } from "@/lib/utils";
import { Message } from '@/types/chat';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  streaming?: boolean;
  followUpQuestions?: string[];
}

interface StreamMarker {
  status: "start" | "end";
  node: string;
  details: string;
}

interface ChatAppProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

const ChatApp: React.FC<ChatAppProps> = ({ messages, setMessages }) => {
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

  const handleStreamingMessage = (chunk: string) => {
    try {
      // Try to parse as JSON first
      const jsonData = JSON.parse(chunk);
      if (jsonData.status === "end") return;
      
      setMessages(prevMessages => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        if (lastMessage && lastMessage.streaming) {
          // Convert numbers to strings if present
          const newText = typeof jsonData.content === 'number' 
            ? lastMessage.text + jsonData.content.toString()
            : lastMessage.text + (jsonData.content || '');

          return [
            ...prevMessages.slice(0, -1),
            { ...lastMessage, text: newText }
          ];
        }
        return prevMessages;
      });
    } catch (e) {
      // If not JSON, treat as regular text
      setMessages(prevMessages => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        if (lastMessage && lastMessage.streaming) {
          // Handle potential number strings
          const newText = !isNaN(Number(chunk)) 
            ? lastMessage.text + chunk
            : lastMessage.text + chunk;

          return [
            ...prevMessages.slice(0, -1),
            { ...lastMessage, text: newText }
          ];
        }
        return prevMessages;
      });
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4 max-w-3xl mx-auto">
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
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-4">
        <form onSubmit={handleSubmit} className="flex gap-2 max-w-3xl mx-auto">
          <Input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ecrivez ici..."
            className="flex-1"
            disabled={isLoading}
          />
          <Button 
            type="submit" 
            disabled={isLoading || !inputMessage.trim()}
            className="bg-[#0066b2] hover:bg-[#0077cc] text-white"
            size="icon"
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </div>
  );
};

export default ChatApp; 