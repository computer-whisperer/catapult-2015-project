from tkinter import *
from tkinter import ttk
import threading

class Controller(threading.Thread):

    def __init__(self, world):
        self.world = world
        threading.Thread.__init__(self)

    def run(self):
        width = 20

        self.root = Tk()
        self.root.title("World Controller")
        self.root.resizable(width=0, height=0)
        self.mainframe = ttk.Frame(self.root, padding="3 3 2 2")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.agent_frame = ttk.Frame(self.mainframe, borderwidth=5, relief="groove")
        self.agent_frame.grid(column=0, row=0)

        self.agent_title = ttk.Label(self.agent_frame, text="No agent selected", width=width)
        self.agent_title.grid(column=0, row=0)

        self.agent_traits = ttk.Label(self.agent_frame, text="", width=width)
        self.agent_traits.grid(column=0, row=1)

        self.agent_state = ttk.Label(self.agent_frame, text="", width=width)
        self.agent_state.grid(column=0, row=2)

        self.control_frame = ttk.Frame(self.mainframe, width="300", height="300", borderwidth=5, relief="groove")
        self.control_frame.grid(column=0, row=1)

        self.control_label = ttk.Label(self.control_frame, text="World Controls", width=width)
        self.control_label.grid(column=0, row=0)

        self.run_button = ttk.Button(self.control_frame, text="Stop" if self.world.run else "Start", command=self.toggle_sim)
        self.run_button.grid(column=0, row=1)

        self.reset_button = ttk.Button(self.control_frame, text="Reset", command=self.reset_sim)
        self.reset_button.grid(column=0, row=2)

        self.root.after(100, self.tick)
        self.root.mainloop()

    def display_agent_stats(self, agent):
        self.agent_title.configure(text="{} {}".format(agent.agent_type, agent.id))
        self.agent_traits.configure(text="Traits: \n" + "\n".join("{}: {}".format(key, agent.agent_data[key]) for key in agent.agent_data))

    def tick(self):
        if self.world.selected_agent is not None:
            self.display_agent_stats(self.world.selected_agent)
        self.root.after(100, self.tick)

    def toggle_sim(self):
        self.world.run = not self.world.run
        self.run_button.configure(text="Stop" if self.world.run else "Start")

    def reset_sim(self):
        self.world.do_reset = True
