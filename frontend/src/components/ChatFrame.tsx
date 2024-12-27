import React, { useState, useEffect } from 'react';
import ChatApp from '@/pages/ChatApp';
import { cn } from "@/lib/utils";
import { MoreVertical, RotateCw } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Message } from '@/types/chat';

const ChatFrame: React.FC = () => {
  const [isMobile, setIsMobile] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleClearMessages = () => {
    setMessages([]);
  };

  const handleEndDiscussion = () => {
    handleClearMessages();
    window.parent.postMessage({ type: 'CLOSE_CHAT' }, '*');
  };

  return (
    <div className="fixed inset-0 flex">
      <div className={cn(
        "bg-white shadow-xl flex flex-col w-full",
        isMobile ? "h-full" : "max-w-[400px] h-full ml-auto"
      )}>
        <div className="bg-[#0066b2] text-white py-2 px-4 flex items-center justify-between shrink-0">
          <h1 className="text-xl font-semibold">Ass-IA</h1>
          
          <div className="flex items-center gap-2">
            <DropdownMenu>
              <DropdownMenuTrigger className="hover:bg-[#0077cc] p-1 rounded">
                <MoreVertical className="h-5 w-5" />
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem onClick={handleClearMessages}>
                  Nouvelle discussion
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleEndDiscussion}>
                  Terminer la discussion
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <button 
              onClick={handleClearMessages}
              className="hover:bg-[#0077cc] p-1 rounded"
            >
              <RotateCw className="h-5 w-5" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-hidden">
          <ChatApp messages={messages} setMessages={setMessages} />
        </div>
      </div>
    </div>
  );
};

export default ChatFrame; 