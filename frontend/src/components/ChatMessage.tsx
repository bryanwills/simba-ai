import React from 'react';
import { cn } from "@/lib/utils";
import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import FollowUpQuestions from './FollowUpQuestions';
import chatbotIcon from "../assets/chatbot-icon.svg";

interface ChatMessageProps {
  isAi: boolean;
  message: string;
  streaming?: boolean;
  followUpQuestions?: string[];
  onFollowUpClick?: (question: string) => void;
}

const ChatMessage = ({ 
  isAi, 
  message, 
  streaming,
  followUpQuestions = [],
  onFollowUpClick 
}: ChatMessageProps) => {
  return (
    <div className={`flex ${isAi ? 'justify-start' : 'justify-end'} max-w-full px-4`}>
      {isAi && (
        <img 
          src={chatbotIcon} 
          alt="Bot" 
          className="w-8 h-8 rounded-full mr-2 flex-shrink-0"
        />
      )}
      <div className={cn(
        "rounded-lg px-4 py-2 break-words",
        "max-w-[85%] md:max-w-[75%]",
        isAi 
          ? "bg-gray-100 text-gray-900" 
          : "bg-[#0066b2] text-white",
        streaming && "animate-pulse"
      )}>
        {isAi ? (
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkBreaks]}
            className="prose prose-sm max-w-none overflow-hidden"
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0 whitespace-pre-wrap">{children}</p>,
              ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
              li: ({ children }) => <li className="marker:text-gray-400">{children}</li>,
              code: ({ node, inline, className, children, ...props }) => (
                <code className={cn(
                  "bg-gray-100 rounded px-1 py-0.5",
                  inline ? "text-sm" : "block p-2 my-2 text-sm overflow-x-auto",
                  className
                )} {...props}>
                  {children}
                </code>
              ),
              pre: ({ children }) => <pre className="bg-gray-100 rounded p-2 my-2 overflow-x-auto">{children}</pre>,
            }}
          >
            {message || ''}
          </ReactMarkdown>
        ) : (
          <p className="whitespace-pre-wrap">{message}</p>
        )}
      </div>
    </div>
  );
};

export default ChatMessage; 