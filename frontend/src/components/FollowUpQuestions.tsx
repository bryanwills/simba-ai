import React from 'react';
import { Button } from "@/components/ui/button";
import { MessageSquarePlus } from 'lucide-react';
import { cn } from "@/lib/utils";

interface FollowUpQuestionsProps {
  questions: string[];
  onQuestionClick: (question: string) => void;
  className?: string;
  streaming?: boolean;
}

const FollowUpQuestions: React.FC<FollowUpQuestionsProps> = ({
  questions,
  onQuestionClick,
  className,
  streaming
}) => {
  if (!questions.length) return null;

  // Don't show the component while streaming unless we have the loading placeholder
  if (streaming && !questions.includes('...')) return null;

  return (
    <div className={cn("mt-2 space-y-2", className)}>
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <MessageSquarePlus className="h-3 w-3" />
        <span>Follow-up questions</span>
      </div>
      <div className={cn(
        "flex flex-wrap gap-2",
        streaming && "animate-pulse"
      )}>
        {questions.map((question, index) => (
          <Button
            key={`${question}-${index}`}
            variant="outline"
            size="sm"
            className={cn(
              "text-xs border-gray-200",
              streaming 
                ? "bg-gray-50 text-gray-400 cursor-wait" 
                : "bg-gray-50 hover:bg-gray-100 text-gray-700"
            )}
            onClick={() => !streaming && onQuestionClick(question)}
            disabled={streaming}
          >
            {question}
          </Button>
        ))}
      </div>
    </div>
  );
};

export default FollowUpQuestions; 