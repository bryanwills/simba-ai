import React from 'react';
import { Button } from "@/components/ui/button";
import { MessageSquarePlus } from 'lucide-react';
import { cn } from "@/lib/utils";

interface FollowUpQuestionsProps {
  questions: string[];
  onQuestionClick?: (question: string) => void;
  className?: string;
}

const FollowUpQuestions: React.FC<FollowUpQuestionsProps> = ({ 
  questions, 
  onQuestionClick,
  className 
}) => {
  return (
    <div className={cn("space-y-2", className)}>
      {questions.map((question, index) => (
        <button
          key={index}
          onClick={() => onQuestionClick?.(question)}
          className="block w-full text-left p-2 rounded border hover:bg-gray-50 whitespace-pre-line text-sm"
        >
          {question}
        </button>
      ))}
    </div>
  );
};

export default FollowUpQuestions; 