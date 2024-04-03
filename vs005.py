import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import math
import time
import copy

class Node:
    def __init__(self,node_id,x,y):
        self.node_id=node_id
        self.x=x
        self.y=y

    
            
class Edge:
    def __init__(self,edge_id,node1,node2):
        self.edge_id=edge_id
        self.node1=node1
        self.node2=node2

class Matching:
    def __init__(self,edge_id,node1,node2):
        self.edge_id=edge_id
        self.node1=node1
        self.node2=node2

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.matchings = []

    def add_node(self, node_id, x, y):
        self.nodes.append(Node(node_id, x, y))

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            # Remove all edges connected to the removed node
            self.edges = [edge for edge in self.edges if edge.node1 != node and edge.node2 != node]
            self.matchings = [matchings for matchings in self.matchings if matchings.node1 != node and matchings.node2 != node]

    def add_edge(self, edge_id, node1, node2):
        for edge in self.edges:
            if (edge.node1==node1 and edge.node2==node2) or (edge.node2==node1 and edge.node1==node2):
                print("EDGE EXISTS")
                return 0
            else:
                continue
        self.edges.append(Edge(edge_id, node1, node2))
       
    
    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
    
    def add_matching(self,matching):
        for match in self.matchings:
            if isinstance(match,Matching):
                print("match")
            elif isinstance(match,Edge):
                print("edge")
            if match.node1==matching.node1 or match.node2==matching.node1 or match.node1==matching.node2 or match.node2==matching.node2:
                print("INVALID MATCHING")
                return None
        self.matchings.append(matching)

    def remove_matching(self,matching):
        if matching in self.matchings:
            self.matchings.remove(matching)
            self.add_edge(matching.edge_id,matching.node1,matching.node2)
        return 0
    
    def find_node(self,node_id):
        for node in self.nodes:
            if node_id==node.node_id:
                return node
            else:
                print("NODENOT FOUND")

    def uploadGraph(file):
        graph = Graph()
        current_section = None
        max_nodeID=0
        max_edgeID=0
        with open(file, 'r') as file:
            for line in file:
                line = line.strip()
                if line == "Nodes:":
                    current_section = "Nodes"
                elif line == "Edges:":
                    current_section = "Edges"
                elif line == "Matchings:":
                    current_section = "Matchings"
                elif line:  # Non-empty line
                    if current_section == "Nodes":
                        parts = line.split(",")
                        node_id, x, y = map(int, parts)
                        if max_nodeID<=node_id:
                            max_nodeID=node_id+1
                        graph.add_node(node_id, x, y)
                    elif current_section == "Edges":
                        parts = line.strip("()").split("),(")
                        for part in parts:
                            edge_id, node1_id, node2_id = map(int, part.split(","))
                            node1 = next((node for node in graph.nodes if node.node_id == node1_id), None)
                            node2 = next((node for node in graph.nodes if node.node_id == node2_id), None)
                            
                            if max_edgeID<=edge_id:
                                max_edgeID=edge_id+1
                            if node1 and node2:
                                graph.add_edge(edge_id, node1, node2)
                    elif current_section == "Matchings":
                        parts = line.split(",")
                        edge_id, node1_id, node2_id = map(int, parts)
                        node1 = next((node for node in graph.nodes if node.node_id == node1_id), None)
                        node2 = next((node for node in graph.nodes if node.node_id == node2_id), None)
                        if max_edgeID<=edge_id:
                                max_edgeID=edge_id+1
                        if node1 and node2:
                            graph.add_matching(Matching(edge_id, node1, node2))
        return graph,max_nodeID,max_edgeID








class InputGUI:
    def __init__(self,file=None):
        
        self.root = tk.Tk()
        self.root.title("INPUT Graph ")
        self.root.geometry("1000x600")

        self.canvas1 = tk.Canvas(self.root, bg="green", height=2000, width=500)
        self.canvas1.pack(side=tk.LEFT)
        self.canvas2 = tk.Canvas(self.root, bg="blue", height=2000, width=500)
        self.canvas2.pack(side=tk.RIGHT)

        
        self.active_edge = None
        

        self.last_click_time = 0  # Initialize variable to store last click time
        self.click_delay = 0.01

        self.input_entry = tk.Entry(self.canvas1)
        self.input_entry.place(x=60, y=140, anchor="w")
        self.save_button = tk.Button(self.canvas1, text="Save", command=self.save)
        self.save_button.place(x=90, y=140, anchor="e")
        
        self.forward_button = tk.Button(self.canvas1, text="Forward", command=self.forward)
        self.forward_button.place(x=10, y=10)  # Adjust the position as needed

        self.backward_button = tk.Button(self.canvas1, text="Backward", command=self.backward)
        self.backward_button.place(x=100, y=10)  # Adjust the position as needed
        
        if file==None:
            self.graph = Graph()
            self.node_id = 0
            self.edge_id = 0
        else:
            self.graph,self.node_id,self.edge_id = Graph.uploadGraph(file)
            for nodes in self.graph.nodes:
                print("Nodes:",nodes.node_id,nodes.x,nodes.y)
            for edges in self.graph.edges:
                print("edges:",edges.edge_id,edges.node1.node_id,edges.node2.node_id)
            for match in self.graph.matchings:
                print("matchings:",match.edge_id,match.node1.node_id,match.node2.node_id)
        

        self.history = []
        self.history_index=-1

        self.canvas1.bind("<Double-Button-1>", self.dbl_clk_b1)
        self.canvas1.bind("<Button-1>", self.sngl_clk_b1)
    def run(self):
        self.root.mainloop()

    
    def save_to_history(self):
        # Save the current state of the graph to history
        self.history = self.history[:self.history_index + 1]  # Truncate history after current index
        self.history.append(copy.deepcopy(self.graph))  # Deep copy to avoid reference issues
        self.history_index += 1
    def backward(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.graph = self.history[self.history_index]
            self.displayGraph()

    def forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.graph = self.history[self.history_index]
            self.displayGraph()

    def dbl_clk_b1(self, event):
        current_time = time.time()
        if current_time - self.last_click_time < self.click_delay:
            return  # Ignore subsequent clicks within the delay period

        p = self.proximal(event)
        self.save_to_history()
        if p == 0:
            self.last_click_time = current_time  # Update last click time
            self.graph.add_node(self.node_id, event.x, event.y)
            self.node_id += 1

            

        elif isinstance(p, Node):
            self.graph.remove_node(p)
        self.save_to_history()
        self.displayGraph()

        self.last_click_time = current_time
        return self

    def sngl_clk_b1(self, event):
        p = self.proximal(event)
        self.save_to_history()
        if isinstance(p, Node):
            print("NODE")
            self.active_edge = Edge(self.edge_id, p, None)
            self.canvas1.bind("<B1-Motion>", self.draw_edge)
        elif isinstance(p,Matching):
            print("EDGE3")
            self.graph.remove_matching(p)
            self.save_to_history()

        
        elif isinstance(p, Edge):
            print("EDGE1")
            self.graph.add_matching(p)
            self.save_to_history()

        self.displayGraph() 
    def end_edge(self, event):
        p = self.proximal(event)
        if self.active_edge and isinstance(p, Node) and self.active_edge.node1 != p:
            self.active_edge.node2 = p
            self.graph.add_edge(self.edge_id, self.active_edge.node1, self.active_edge.node2)
            self.edge_id += 1
            self.save_to_history()
        self.active_edge = None
        self.canvas1.unbind("<B1-Motion>")
        
        self.displayGraph()
        return self

    def display_temp_edge(self, event):
        self.canvas1.delete("temp_edge")
        if self.active_edge:
            start_x, start_y = self.active_edge.node1.x, self.active_edge.node1.y
            end_x, end_y = event.x, event.y
            self.canvas1.create_line(start_x, start_y, end_x, end_y, fill="blue", tags="temp_edge")
            self.canvas1.bind("<ButtonRelease-1>", self.end_edge)

    def draw_edge(self, event):
        if self.active_edge:
            self.active_edge.node2 = Node(-1, event.x, event.y)
            self.display_temp_edge(event)

    def delete_shapes_in_region(self, canvas, x1, y1, x2, y2):
        items_in_region = self.canvas1.find_overlapping(x1, y1, x2, y2)
        for item in items_in_region:
            self.canvas1.delete(item)

    def displayGraph(self):
        self.delete_shapes_in_region(self.canvas1, 0, 0, 500, 1000)
        
        r = 20
        for edge in self.graph.edges:
            self.canvas1.create_line(edge.node1.x,edge.node1.y,edge.node2.x,edge.node2.y,fill="blue",width=10)
        for matching in self.graph.matchings:
            self.canvas1.create_line(matching.node1.x,matching.node1.y,matching.node2.x,matching.node2.y,fill="red",width=10)
        
        for node in self.graph.nodes:
            self.canvas1.create_oval(node.x - r, node.y - r, node.x + r, node.y + r, fill="white")
            self.canvas1.tag_raise(self.canvas1.create_text(node.x, node.y, font=("Purisa", 20), text=str(node.node_id)))

        
    


    def point_distance(self,x1, y1, x2, y2, x, y):
    # Vector representing the line segment
        dx = x2 - x1
        dy = y2 - y1

    # Vector representing the point's position relative to the line segment
        px = x - x1
        py = y - y1

    # dot product of line segment and  point
        dot_product = px * dx + py * dy

    # squared length of the line segment vector
        line_length_squared = dx * dx + dy * dy

    # project the point onto the line segment
        t = max(0, min(1, dot_product / line_length_squared))
        projection_x = x1 + t * dx
        projection_y = y1 + t * dy

    # distance from  point to projection
        distance = math.sqrt((x - projection_x) ** 2 + (y - projection_y) ** 2)
        return distance

    def proximal(self, event):
        r = 30
        for node in self.graph.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                print("Node clicked", node.node_id)
                return node


        for match in self.graph.matchings:
            x1, y1 = match.node1.x, match.node1.y
            x2, y2 = match.node2.x, match.node2.y

            # Calculate distance from the point to the line segment
            #print(self.point_distance(x1,y1,x2,y2,event.x,event.y))
            distance=self.point_distance(x1,y1,x2,y2,event.x,event.y)

            edge_perimeter = 10  # Adjust as needed
        
        # If the distance is within the perimeter, return the edge
            if distance <= edge_perimeter:
                print("match clicked:", match.edge_id)
                return match


        for edge in self.graph.edges:
            x1, y1 = edge.node1.x, edge.node1.y
            x2, y2 = edge.node2.x, edge.node2.y

            # Calculate distance from the point to the line segment
            #print(self.point_distance(x1,y1,x2,y2,event.x,event.y))
            distance=self.point_distance(x1,y1,x2,y2,event.x,event.y)

            edge_perimeter = 10  # Adjust as needed
        
        # If the distance is within the perimeter, return the edge
            if distance <= edge_perimeter:
                print("Edge clicked:", edge.edge_id)
                return edge
            


        return 0

    def getText(self):
        text=self.input_entry.get()
        return text
    def save(self):
        
        text=self.getText()
        #text=self.input_entry.get()
        filename = f"graph_{text}_data.txt"
        with open(filename, 'w') as file:
        # Write nodes to the file
            file.write("Nodes:\n")
            for node in self.graph.nodes:
                file.write(f"{node.node_id},{node.x},{node.y}\n")

            # Write edges to the file
            file.write("\nEdges:\n")
            for edge in self.graph.edges:
                
                file.write(f"{edge.edge_id},{edge.node1.node_id},{edge.node2.node_id}\n")
            
            # Write edges to the file
            file.write("\nMatchings:\n")
            for match in self.graph.matchings:
                file.write(f"{match.edge_id},{match.node1.node_id},{match.node2.node_id}\n")
        print(f"Graph data saved to {filename}")


class HomeGui:
    def __init__(self):
        self.root1 = tk.Tk()
        self.root1.title("Home GUI")
        self.root1.geometry("500x500")
        self.canvas = tk.Canvas(self.root1, bg="lightgreen")

        self.input_graph = tk.Button(self.canvas, text="INPUT OWN GRAPH", command=self.inputTool)
        self.input_graph.place(x=250, y=140, anchor="center")

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select a file")

        self.dropdown = ttk.Combobox(self.canvas, textvariable=self.dropdown_var, state="readonly")
        self.dropdown.place(x=250, y=250, anchor="center")
        self.populate_dropdown()

        self.dropdown.bind("<<ComboboxSelected>>", self.update_selected_value)

        self.canvas.pack(fill=tk.BOTH, expand=True)

    def populate_dropdown(self):
        current_dir = os.getcwd()
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        self.dropdown["values"] = files

    def update_selected_value(self, event):
        selected_value = self.dropdown_var.get()
        self.uploadTool(selected_value)

    def inputTool(self):
        inputGraphGUI = InputGUI()
        inputGraphGUI.run()

    def uploadTool(self, file):
        uploadGraphGUI = InputGUI(file)
        uploadGraphGUI.run()

    def run(self):
        self.root1.mainloop()


home_gui = HomeGui()
home_gui.run()
