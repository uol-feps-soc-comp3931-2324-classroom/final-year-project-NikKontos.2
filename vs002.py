import tkinter as tk
from pyvis.network import Network
import webbrowser
import os

class GraphGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph GUI")

        # Create an empty graph
        self.graph = Network(height="500px", width="100%", notebook=True, cdn_resources='in_line')

        # Create a Tkinter canvas for pyvis
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Initialize variables to store nodes and edges
        self.nodes = []
        self.edges = []
        self.draw = [[None, None]]

        self.last_clicked_node = None
        self.current_edge = None  # Variable to track the current edge being drawn

        # Bind mouse events to functions
        self.canvas.bind("<Double-Button-1>", self.dbl_clk)

    def proximal(self, event):
        x = event.x
        y = event.y
        r = 60

        for node_id, node_x, node_y in self.nodes:
            distance = ((x - node_x) ** 2 + (y - node_y) ** 2) ** 0.5
            if distance <= r:
                return node_id, node_x, node_y  # Double click within radius of an existing node

        return False  # Double click not within radius of any existing node

    def add_node(self, event):
        # Add a node at the clicked position
        x, y = event.x, event.y
        num_node = len(self.nodes)
        node_id = num_node + 1
        self.nodes.append((node_id, x, y))

        self.graph.add_node(node_id, x=x, y=y)  # Add the node to the graph at the clicked position

        # Draw a circle representing the node on the Tkinter canvas
        radius = 15
        pict = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue",tag=str(node_id))
        text = self.canvas.create_text(x, y, text=node_id,tag=str(node_id))
        self.draw.append([pict, text])
        # Save the last clicked node for adding edges
        self.last_clicked_node = node_id

            return self

    def dbl_clk(self, event):
        p = self.proximal(event)
        if p == False:
            self.add_node(event)
        else:
            self.remove_node(event, p)
        return self

    def run(self):
        self.root.mainloop()

# Create an instance of the GraphGUI class
graph_gui = GraphGUI()

# Run the Tkinter application
graph_gui.run()
