import React from 'react';
import { cn } from "@/lib/utils";
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
  // Handle numerical values and JSON status messages
  const formattedMessage = React.useMemo(() => {
    if (typeof message === 'number') {
      return message.toString();
    }
    try {
      const parsed = JSON.parse(message);
      if (parsed.status) return null;
      return parsed.content || message;
    } catch {
      return message;
    }
  }, [message]);

  if (!formattedMessage) return null;

  return (
    <div className={`flex ${isAi ? 'justify-start' : 'justify-end'} w-full mb-4`}>
      <div className={cn(
        "flex items-start gap-2 w-full",
        isAi ? "flex-row" : "flex-row-reverse"
      )}>
        {isAi && (
          <img 
            src={chatbotIcon} 
            alt="Bot" 
            className="w-8 h-8 rounded-full flex-shrink-0 mt-1"
          />
        )}
        <div className={cn(
          "rounded-lg p-4 max-w-[85%]",
          isAi 
            ? "bg-white border" 
            : "bg-[#0066b2] text-white whitespace-pre-line"
        )}>
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkBreaks]}
            className={cn(
              "prose prose-sm max-w-none break-words",
              !isAi && "text-white prose-headings:text-white prose-strong:text-white"
            )}
          >
            {formattedMessage}
          </ReactMarkdown>
          {isAi && followUpQuestions.length > 0 && (
            <div className="mt-4 whitespace-pre-line">
              <p className="text-sm font-medium mb-2">Suggestions:</p>
              <FollowUpQuestions 
                questions={followUpQuestions.map(q => q.trim())}
                onQuestionClick={onFollowUpClick} 
                className="whitespace-pre-line"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;