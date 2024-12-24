import React, { useState, useEffect } from 'react';
import { Bot, X } from 'lucide-react';
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import ChatApp from '@/pages/ChatApp';
import { cn } from "@/lib/utils";

const ChatFrame: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="fixed bottom-4 right-8 z-50">
      {!isOpen && (
        <Button
          onClick={() => setIsOpen(true)}
          className="rounded-full w-12 h-12 md:w-14 md:h-14 bg-white hover:bg-gray-100 shadow-lg flex items-center justify-center border"
        >
          <Bot className="h-5 w-5 md:h-6 md:w-6 text-blue-500" />
        </Button>
      )}

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className={cn(
          "p-0 bg-white shadow-xl",
          isMobile 
            ? "w-[calc(100vw-32px)] h-[calc(100vh-120px)] mt-auto bottom-20"
            : "w-[400px] h-[calc(100vh-120px)] mt-auto bottom-20 right-8"
        )}>
          <div className="relative flex flex-col h-full rounded-lg overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b bg-white">
              <div className="flex items-center gap-2">
                <Bot className="h-5 w-5 text-blue-500" />
                <span className="font-semibold">Ass-IA</span>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
                onClick={() => setIsOpen(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            {/* Chat Content */}
            <div className="flex-1 overflow-hidden">
              <ChatApp />
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ChatFrame; 