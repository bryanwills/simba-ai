import React from 'react';
import { cn } from "@/lib/utils";
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  isAi: boolean;
  message: string;
}

const ChatMessage = ({ isAi, message }: ChatMessageProps) => {
  return (
    <div className={cn("flex items-start space-x-2", isAi ? "flex-row" : "flex-row-reverse space-x-reverse")}>
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center",
        isAi ? "bg-blue-100" : "bg-gray-100"
      )}>
        {isAi ? (
          <Bot className="h-5 w-5 text-blue-500" />
        ) : (
          <User className="h-5 w-5 text-gray-500" />
        )}
      </div>
      <div className={cn(
        "rounded-lg px-4 py-2 max-w-[80%] shadow-sm",
        isAi ? "bg-white" : "bg-blue-500 text-white"
      )}>
        {message}
      </div>
    </div>
  );
};

export default ChatMessage; 