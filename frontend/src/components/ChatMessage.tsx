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
  // Filter out status messages
  const cleanMessage = message.replace(
    /\{"status":\s*"end",\s*"node":\s*"generate",\s*"details":\s*"Node stream ended"\}/g, 
    ''
  ).trim();

  // Don't render if message is empty after cleaning
  if (!cleanMessage) {
    return null;
  }

  return (
    <div className="flex flex-col">
      {!isAi && (
        <div className="flex justify-end w-full">
          <div className="rounded-lg p-4 bg-[#0066b2] text-white whitespace-pre-line max-w-[85%]">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkBreaks]}
              className="prose prose-sm max-w-none break-words text-white prose-headings:text-white prose-strong:text-white"
            >
              {cleanMessage}
            </ReactMarkdown>
          </div>
        </div>
      )}
      
      {isAi && (
        <div className="flex flex-col w-full">
          <img 
            src={chatbotIcon} 
            alt="Bot" 
            className="w-8 h-8 rounded-full mb-2"
          />
          <div className="flex justify-start w-full">
            <div className="rounded-lg p-4 bg-white border w-full">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
                className="prose prose-sm max-w-none break-words"
              >
                {cleanMessage}
              </ReactMarkdown>
              {followUpQuestions.length > 0 && (
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
      )}
    </div>
  );
};

export default ChatMessage;