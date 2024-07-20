import asyncio
import websockets
import threading

import tkinter as tk

from tkinter import ttk, messagebox

class SimpleChat:
    def __init__(self, root):
        self.root = root
        self.websocket = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.connection_ready = threading.Event()
        threading.Thread(target=self.run_loop).start()
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # wait for websocket connection to be ready before unlocking UI
        self.root.after(100, self.check_connection)

    def setup_ui(self):
        self.root.title("Content Moderation Chat")

        self.mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.chat_display = tk.Text(self.mainframe, height=20, width=70, state=tk.DISABLED)
        self.chat_display.grid(column=1, row=1, columnspan=3, sticky=(tk.W, tk.E))

        ttk.Label(self.mainframe, text="Enter text:").grid(column=1, row=2, sticky=tk.W)
        self.text_entry = ttk.Entry(self.mainframe, width=50)
        self.text_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

        self.submit_button = ttk.Button(self.mainframe, text="Submit", command=self.on_submit)
        self.submit_button.grid(column=3, row=2, sticky=tk.W)
        self.submit_button.config(state=tk.DISABLED)

    async def start_websocket(self):
        ws_endpoint = "ws://localhost:8000/receive"
        try:
            self.websocket = await websockets.connect(ws_endpoint)
            self.connection_ready.set()  # connection is ready
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")

    def check_connection(self):
        if self.connection_ready.is_set():
            # enable buttons
            self.submit_button.config(state=tk.NORMAL)
        else:
            # check again after 500 ms
            print("Retrying...")
            self.root.after(500, self.check_connection)

    async def send_message(self, msg):
        await self.websocket.send(msg)
        response = await self.websocket.recv()
        return response
    
    def on_submit(self):
        text = self.text_entry.get()
        if text.strip() == "":
            messagebox.showwarning("Warning", "Please enter some text.")
            return
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {text}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.text_entry.delete(0, tk.END)

        asyncio.run_coroutine_threadsafe(self.handle_message(text), self.loop)

    async def handle_message(self, text):
        prediction = await self.send_message(text)
        result = prediction

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"System: Your message {result}.\n")
        self.chat_display.config(state=tk.DISABLED)

    def run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.start_websocket())
        self.loop.run_forever()

    def on_closing(self):
        self.loop.stop()
        if self.websocket:
            self.loop.run_until_complete(self.websocket.close())
        self.root.destroy()

root = tk.Tk()
app = SimpleChat(root)
root.mainloop()