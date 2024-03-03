import tkinter as tk

import networkx as nx
import webbrowser
import os

class Node:
     def __init__(self, obj_id,node_id, x, y):
        self.obj_id=obj_id
        self.node_id = node_id
        self.x = x
        self.y = y

class Edge:
     def __init__(self, obj_id,node_s,node_t):
        self.obj_id = obj_id
        self.x1 = node_s.x
        self.y1 = node_s.y
        self.x2 = node_t.x
        self.y2 = node_t.y
        

        
class GraphGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph GUI")

        # Create an empty graph
        

        # Create a Tkinter canvas for pyvis
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        # Initialize variables to store nodes and edges
        self.nodes=[]
        self.edge=[]
        
        self.obj_id=0

        self.last_clicked_node = None
        self.current_edge = None  # Variable to track the current edge being drawn

        # Bind mouse events to functions

        self.canvas.bind("<Double-Button-1>", self.dbl_clk)
    
    def displayGraph(self):
        self.canvas.delete("all")
        for node in self.nodes:
            r=30
            print(node)
            self.canvas.create_oval(node.x-r,node.y-r,node.x+r,node.y+r,fill="red")
            self.canvas.create_text(node.x,node.y,text=str(node.node_id))
            
        self.canvas.pack()


    def proximal(self, event):
        
        r = 30

        for node in self.nodes:
            print("node:",node.obj_id,node.x,node.y)
            
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                return node  # Double click within radius of an existing node

        return False  # Double click not within radius of any existing node

    def add_node(self, event):
        # Add a node at the clicked position
        x, y = event.x, event.y
        node_id = len(self.nodes)
        n=Node(self.obj_id,node_id,x,y)
        self.obj_id+=1
        self.nodes.append(n)

        # Draw a circle representing the node on the Tkinter canvas
        radius = 30

        
        # Save the last clicked node for adding edges
        self.last_clicked_node = node_id
        self.displayGraph()
        return self

    def remove_node(self,event,p):
        
        for node in self.nodes:
            if p.x==node.x and p.y==node.y:
                self.nodes.remove(node)


        for edge in self.edge:
            if (p.node_id==edge.node_s or p.node_id==edge.node_t):
                self.edges.remove(edge)

        self.displayGraph()

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
