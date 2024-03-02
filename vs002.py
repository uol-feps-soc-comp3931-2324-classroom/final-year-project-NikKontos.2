import tkinter as tk
from pyvis.network import Network

class GraphGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph GUI")

        # Create an empty graph
        self.graph = Network(height="500px", width="100%")

        # Create a canvas for pyvis to embed in Tkinter
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Initialize variables to store nodes and edges
        self.nodes = set()
        self.edges = set()

        # Bind mouse events to functions
        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<B1-Motion>", self.add_edge)

    def add_node(self, event):
        # Add a node at the clicked position
        node_id = f"Node_{len(self.nodes) + 1}"
        self.nodes.add(node_id)
        self.graph.add_node(node_id)
        self.graph.show("graph_visualization.html")

    def add_edge(self, event):
        # Add an edge by click-dragging
        x, y = event.x, event.y
        element = self.canvas.find_closest(x, y)

        if element:
            # Find the closest node to the click position
            node_id = self.graph.get_node_at(event.x, event.y)
            if node_id:
                # Add an edge from the last clicked node to the current node
                edge_id = f"Edge_{len(self.edges) + 1}"
                self.edges.add((node_id, edge_id))
                self.graph.add_edge(node_id, edge_id)
                self.graph.show("graph_visualization.html")

    def run(self):
        self.root.mainloop()

# Create an instance of the GraphGUI class
graph_gui = GraphGUI()

# Run the Tkinter application
graph_gui.run()
how do i run this if its saved in a GitHub repo opened in vscode