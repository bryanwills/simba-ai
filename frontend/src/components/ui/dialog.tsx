import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root

const DialogTrigger = DialogPrimitive.Trigger

const DialogPortal = DialogPrimitive.Portal

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/50 transition-opacity animate-in fade-in" />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed right-4 bottom-4 z-50 grid w-full max-w-lg translate-y-0 gap-4 border bg-background p-6 shadow-lg duration-200 animate-in fade-in-90 zoom-in-90 sm:rounded-lg",
        className
      )}
      {...props}
    >
      {children}
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

export {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogPortal,
} 