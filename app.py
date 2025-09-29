import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox, ttk
from PIL import Image, ImageTk
import base64
import httpx
import asyncio
import io
import threading
import time
import platform

class AIChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chat Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f2f5')
        
        # Make window resizable
        self.root.minsize(600, 500)
        
        # Set theme colors with improved contrast
        self.colors = {
            'primary': '#2d88ff',
            'secondary': '#1877f2',
            'background': '#f0f2f5',
            'user_msg': '#0084ff',
            'bot_msg': '#e4e6eb',
            'text_dark': '#1c1e21',
            'text_light': '#65676b',
            'white': '#ffffff',
            'focus': '#ffbf47'  # High contrast focus color
        }
        
        # Configure styles
        self.setup_styles()
        
        # Create main layout
        self.create_header()
        self.create_chat_area()
        self.create_input_area()
        self.create_status_bar()
        
        # Initialize state variables
        self.conversation_history = []
        self.image_to_send = None
        self.is_typing = False
        self.last_focused_widget = None

        # Setup asyncio loop in a separate thread
        self.async_loop = asyncio.new_event_loop()
        self.async_thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.async_thread.start()
        
        # Set up keyboard navigation
        self.setup_keyboard_navigation()
        
        # Announce application start for screen readers
        self.announce("AI Chat Assistant application started. Ready to chat.")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles with improved focus indicators
        style.configure('Primary.TButton',
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       borderwidth=2,
                       focuscolor=self.colors['focus'])
        
        style.configure('Secondary.TButton',
                       background=self.colors['white'],
                       foreground=self.colors['primary'],
                       borderwidth=2,
                       focuscolor=self.colors['focus'])
        
        # Configure scrollbar style
        style.configure('Vertical.TScrollbar', 
                       background=self.colors['secondary'],
                       troughcolor=self.colors['background'],
                       borderwidth=1,
                       relief='raised')

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="AI Chat Assistant", 
                              font=("Segoe UI", 18, "bold"),
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Add ARIA role for screen readers
        title_label.aria_role = "heading"
        title_label.aria_level = 1
        
        # Model info
        model_label = tk.Label(header_frame,
                              text="Model: LLaVA-Phi3",
                              font=("Segoe UI", 10),
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        model_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Add ARIA role for screen readers
        model_label.aria_role = "status"

    def create_chat_area(self):
        # Main chat container
        chat_container = tk.Frame(self.root, bg=self.colors['background'])
        chat_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Add label for screen readers
        chat_label = tk.Label(chat_container, text="Chat Messages", font=("Segoe UI", 12, "bold"),
                             bg=self.colors['background'], fg=self.colors['text_dark'])
        chat_label.pack(anchor='w')
        chat_label.aria_role = "heading"
        chat_label.aria_level = 2
        
        # Chat history frame with shadow effect
        self.chat_frame = tk.Frame(chat_container, bg=self.colors['white'], relief='solid', bd=1)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Create a canvas and scrollbar for chat messages
        self.chat_canvas = tk.Canvas(self.chat_frame, bg=self.colors['white'], highlightthickness=1,
                                    highlightbackground=self.colors['text_light'])
        scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview,
                                 style='Vertical.TScrollbar')
        self.scrollable_frame = tk.Frame(self.chat_canvas, bg=self.colors['white'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        
        self.chat_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.chat_canvas.winfo_reqwidth())
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=2)
        
        # Bind mousewheel to scroll
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        self.chat_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Add ARIA attributes for screen readers
        self.chat_canvas.aria_role = "log"
        self.chat_canvas.aria_label = "Chat messages"

    def create_input_area(self):
        input_container = tk.Frame(self.root, bg=self.colors['background'])
        input_container.pack(fill=tk.X, padx=15, pady=10)
        
        # Add label for screen readers
        input_label = tk.Label(input_container, text="Message Input", font=("Segoe UI", 12, "bold"),
                              bg=self.colors['background'], fg=self.colors['text_dark'])
        input_label.pack(anchor='w')
        input_label.aria_role = "heading"
        input_label.aria_level = 2
        
        # Top row for image attachment and clear button
        top_row = tk.Frame(input_container, bg=self.colors['background'])
        top_row.pack(fill=tk.X, pady=(5, 8))
        
        self.attach_btn = ttk.Button(top_row, 
                                    text="📎 Attach Image", 
                                    command=self.attach_image,
                                    style='Secondary.TButton')
        self.attach_btn.pack(side=tk.LEFT)
        self.attach_btn.aria_label = "Attach image to message"
        
        self.clear_btn = ttk.Button(top_row,
                                   text="🗑️ Clear Chat",
                                   command=self.clear_chat,
                                   style='Secondary.TButton')
        self.clear_btn.pack(side=tk.RIGHT)
        self.clear_btn.aria_label = "Clear all chat messages"
        
        # Main input area
        input_frame = tk.Frame(input_container, bg=self.colors['white'], relief='solid', bd=2)
        input_frame.pack(fill=tk.X)
        
        self.user_input = scrolledtext.ScrolledText(input_frame, 
                                                   font=("Segoe UI", 11),
                                                   height=4,
                                                   wrap=tk.WORD,
                                                   relief='flat',
                                                   padx=12,
                                                   pady=12,
                                                   highlightthickness=1,
                                                   highlightcolor=self.colors['primary'],
                                                   highlightbackground=self.colors['text_light'])
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add ARIA attributes
        self.user_input.aria_role = "textbox"
        self.user_input.aria_label = "Type your message here"
        
        # Send button container
        send_container = tk.Frame(input_frame, bg=self.colors['white'])
        send_container.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        self.send_button = ttk.Button(send_container,
                                     text="Send\n(Enter)",
                                     command=self.send_message,
                                     style='Primary.TButton',
                                     width=8)
        self.send_button.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        self.send_button.aria_label = "Send message"
        
        # Bind Enter key (but not Shift+Enter)
        self.user_input.bind("<Return>", self.on_enter_pressed)
        self.user_input.bind("<Shift-Return>", self.on_shift_enter)
        
        # Add keyboard shortcuts info
        shortcuts_label = tk.Label(input_container, 
                                  text="Keyboard shortcuts: Enter to send, Shift+Enter for new line",
                                  font=("Segoe UI", 9),
                                  bg=self.colors['background'],
                                  fg=self.colors['text_light'])
        shortcuts_label.pack(anchor='w', pady=(5, 0))

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg=self.colors['white'], height=30, relief='solid', bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame,
                                    text="Ready to chat",
                                    font=("Segoe UI", 9),
                                    bg=self.colors['white'],
                                    fg=self.colors['text_dark'])
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add ARIA role for screen readers
        self.status_label.aria_role = "status"
        
        self.typing_indicator = tk.Label(self.status_frame,
                                        text="",
                                        font=("Segoe UI", 9, "italic"),
                                        bg=self.colors['white'],
                                        fg=self.colors['primary'])
        self.typing_indicator.pack(side=tk.RIGHT, padx=10, pady=5)

    def setup_keyboard_navigation(self):
        # Set up tab order for keyboard navigation
        widgets = [
            self.attach_btn,
            self.user_input,
            self.send_button,
            self.clear_btn
        ]
        
        for i, widget in enumerate(widgets):
            widget.bind('<FocusIn>', lambda e, w=widget: self.on_focus_in(w))
            widget.bind('<FocusOut>', lambda e: self.on_focus_out())
        
        # Set initial focus
        self.user_input.focus_set()
        
        # Add global keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.clear_chat())
        self.root.bind('<Control-o>', lambda e: self.attach_image())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Escape>', lambda e: self.focus_chat_area())

    def on_focus_in(self, widget):
        self.last_focused_widget = widget
        # Add visual focus indicator
        if hasattr(widget, 'configure'):
            try:
                widget.configure(relief='solid', borderwidth=2)
            except:
                pass

    def on_focus_out(self):
        # Remove visual focus indicator
        if self.last_focused_widget and hasattr(self.last_focused_widget, 'configure'):
            try:
                self.last_focused_widget.configure(relief='flat', borderwidth=0)
            except:
                pass

    def focus_chat_area(self):
        self.chat_canvas.focus_set()

    def announce(self, message):
        """Announce message for screen readers"""
        # This is a simplified version - in a real application, 
        # you would use a proper screen reader API
        print(f"Screen reader: {message}")
        self.update_status(message)

    def on_canvas_configure(self, event):
        self.chat_canvas.itemconfig(1, width=event.width)

    def on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_enter_pressed(self, event):
        if not event.state & 0x1:  # If Shift is not pressed
            self.send_message()
            return "break"  # Prevents default behavior
        return None

    def on_shift_enter(self, event):
        # Allow new line when Shift+Enter is pressed
        self.user_input.insert(tk.INSERT, "\n")
        return "break"

    def append_message(self, sender, message, is_image=False):
        message_frame = tk.Frame(self.scrollable_frame, bg=self.colors['white'])
        message_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Configure alignment based on sender
        if sender == "user":
            bg_color = self.colors['user_msg']
            text_color = self.colors['white']
            anchor = "e"
            message_frame.pack(anchor="e")
        else:
            bg_color = self.colors['bot_msg']
            text_color = self.colors['text_dark']
            anchor = "w"
            message_frame.pack(anchor="w")
        
        # Message bubble
        bubble_frame = tk.Frame(message_frame, bg=bg_color, relief='solid', bd=1, padx=15, pady=10)
        bubble_frame.pack(anchor=anchor)
        
        # Sender label
        sender_label = tk.Label(bubble_frame,
                               text=sender.capitalize(),
                               font=("Segoe UI", 9, "bold"),
                               bg=bg_color,
                               fg=text_color)
        sender_label.pack(anchor=anchor)
        
        # Message content
        if is_image:
            content_label = tk.Label(bubble_frame,
                                   text="📷 Image attached",
                                   font=("Segoe UI", 10, "italic"),
                                   bg=bg_color,
                                   fg=text_color)
        else:
            content_label = tk.Label(bubble_frame,
                                   text=message,
                                   font=("Segoe UI", 10),
                                   bg=bg_color,
                                   fg=text_color,
                                   wraplength=400,
                                   justify=tk.LEFT)
        
        content_label.pack(anchor=anchor)
        
        # Timestamp
        timestamp = time.strftime("%H:%M")
        time_label = tk.Label(bubble_frame,
                            text=timestamp,
                            font=("Segoe UI", 8),
                            bg=bg_color,
                            fg=text_color)
        time_label.pack(anchor=anchor)
        
        # Update scroll region
        self.chat_canvas.update_idletasks()
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1.0)
        
        # Announce new message for screen readers
        if sender == "user":
            self.announce(f"You said: {message if not is_image else 'Image attached'}")
        else:
            self.announce(f"Assistant: {message}")

    def show_typing_indicator(self):
        self.is_typing = True
        self.typing_indicator.config(text="AI is typing...")
        self.announce("AI is typing a response")
        
    def hide_typing_indicator(self):
        self.is_typing = False
        self.typing_indicator.config(text="")

    def update_status(self, message):
        self.status_label.config(text=message)

    def send_message(self):
        user_text = self.user_input.get("1.0", tk.END).strip()
        if not user_text and not self.image_to_send:
            messagebox.showinfo("No Content", "Please type a message or attach an image before sending.")
            return

        if user_text:
            self.append_message("user", user_text)
        if self.image_to_send:
            self.append_message("user", "[Image Attached]", is_image=True)

        # Clear input
        self.user_input.delete("1.0", tk.END)
        self.update_status("Sending message...")

        # Show typing indicator
        self.show_typing_indicator()

        # Schedule the coroutine in the async loop
        self.async_loop.call_soon_threadsafe(
            asyncio.create_task, self.get_bot_response(user_text, self.image_to_send)
        )
        self.image_to_send = None

    def clear_chat(self):
        if not self.conversation_history:
            messagebox.showinfo("Chat Already Empty", "There are no messages to clear.")
            return
            
        result = messagebox.askyesno("Clear Chat", "Are you sure you want to clear all chat messages?")
        if result:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.conversation_history.clear()
            self.update_status("Chat cleared")
            self.announce("Chat history cleared")

    def attach_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            try:
                # Validate image size (max 5MB)
                if self.get_file_size(file_path) > 5 * 1024 * 1024:
                    messagebox.showerror("File Too Large", "Please select an image smaller than 5MB.")
                    return
                    
                with open(file_path, "rb") as image_file:
                    self.image_to_send = image_file.read()
                filename = file_path.split('/')[-1]
                self.update_status(f"Image '{filename}' attached")
                self.announce(f"Image {filename} attached successfully")
                messagebox.showinfo("Image Attached", 
                                  f"Image '{filename}' attached successfully!\n\nSend your message to analyze the image.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read image file: {e}")
                self.image_to_send = None

    def get_file_size(self, file_path):
        import os
        return os.path.getsize(file_path)

    def _run_async_loop(self):
        asyncio.set_event_loop(self.async_loop)
        self.async_loop.run_forever()

    async def get_bot_response(self, user_message, image_data=None):
        self.conversation_history.append({"role": "user", "content": user_message})

        try:
            if image_data:
                self.update_status("Analyzing image...")
                description = await self._get_image_description(image_data)
                self.hide_typing_indicator()
                self.append_message("assistant", f"I see an image: {description}")
                self.conversation_history.append({"role": "assistant", "content": f"I see an image: {description}"})
                
                if user_message:
                    self.show_typing_indicator()
                    response_text = await self._generate_text_response(user_message, self.conversation_history)
                    self.hide_typing_indicator()
                    self.append_message("assistant", response_text)
                    self.conversation_history.append({"role": "assistant", "content": response_text})
            elif user_message:
                self.update_status("Generating response...")
                response_text = await self._generate_text_response(user_message, self.conversation_history)
                self.hide_typing_indicator()
                self.append_message("assistant", response_text)
                self.conversation_history.append({"role": "assistant", "content": response_text})
            
            self.update_status("Ready")
            
        except Exception as e:
            self.hide_typing_indicator()
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.append_message("assistant", error_msg)
            self.update_status("Error occurred")
            self.announce(f"Error: {str(e)}")

    async def _get_image_description(self, image_data: bytes) -> str:
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llava-phi3",
            "prompt": "Analyze this image in detail. First, identify the main subject and the overall setting. Then, list the key objects and their spatial relationships. Finally, describe the mood and any notable actions.",
            "images": [encoded_image],
            "stream": False,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("https://d38d14803ae0.ngrok-free.app/api/generate", headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                response_data = response.json()
                return response_data["response"]
            except Exception as e:
                return f"Could not analyze the image: {str(e)}"

    async def _generate_text_response(self, prompt: str, history: list) -> str:
        headers = {"Content-Type": "application/json"}
        messages = [{"role": m["role"], "content": m["content"]} for m in history]
        
        payload = {
            "model": "llava-phi3",
            "messages": messages,
            "stream": False,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("https://d38d14803ae0.ngrok-free.app/api/chat", headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
                response_data = response.json()
                return response_data["message"]["content"]
            except Exception as e:
                return f"Could not generate response: {str(e)}"


if __name__ == "__main__":
    root = tk.Tk()
    app = AIChatApp(root)
    
    # Set application icon and title for taskbar
    root.iconname("AI Chat Assistant")
    
    # Make sure window appears on top initially for focus
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    root.mainloop()