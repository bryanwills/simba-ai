import React from 'react';
import { cn } from "@/lib/utils";
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  isAi: boolean;
  message: string;
  streaming?: boolean;
}

const ChatMessage = ({ isAi, message, streaming }: ChatMessageProps) => {
  return (
    <div className={cn("flex items-start space-x-2", isAi ? "flex-row" : "flex-row-reverse space-x-reverse")}>
      <div className={cn(
        "w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center",
        isAi ? "bg-blue-100" : "bg-gray-100"
      )}>
        {isAi ? (
          <Bot className="h-4 w-4 sm:h-5 sm:w-5 text-blue-500" />
        ) : (
          <User className="h-4 w-4 sm:h-5 sm:w-5 text-gray-500" />
        )}
      </div>
      <div className={cn(
        "rounded-lg px-3 py-2 sm:px-4 sm:py-2 max-w-[85%] shadow-sm text-sm sm:text-base",
        isAi ? "bg-white" : "bg-blue-500 text-white",
        streaming && "animate-pulse"
      )}>
        {message || '...'}
      </div>
    </div>
  );
};

export default ChatMessage; 