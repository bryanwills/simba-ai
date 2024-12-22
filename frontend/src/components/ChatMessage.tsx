import React from 'react';
import { cn } from "@/lib/utils";
import { Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import FollowUpQuestions from './FollowUpQuestions';

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
      <div className="flex flex-col flex-1">
        <div className={cn(
          "rounded-lg px-3 py-2 sm:px-4 sm:py-2 max-w-[85%] shadow-sm text-sm sm:text-base",
          isAi ? "bg-white prose prose-sm max-w-none" : "bg-blue-500 text-white",
          streaming && "animate-pulse"
        )}>
          {isAi ? (
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkBreaks]}
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
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
            message
          )}
        </div>
        {isAi && followUpQuestions && (
          <FollowUpQuestions
            questions={followUpQuestions}
            onQuestionClick={onFollowUpClick!}
            className="ml-0 sm:ml-4"
            streaming={streaming}
          />
        )}
      </div>
    </div>
  );
};

export default ChatMessage; 