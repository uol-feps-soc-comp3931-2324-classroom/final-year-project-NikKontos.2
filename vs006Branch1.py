
import tkinter as tk
from tkinter import ttk,scrolledtext
import networkx as nx
from collections import deque
import os
import math


###  TRY simplfied of edmonds algo where lowest unsat node is bfs seached greedily until another unsat node is hit, 
# then augment the path



import copy

#cobalt #054bb4
#shipcove #658cc2
#shuttle grey #5db6169

global grey,lightblue,darkblue
darkblue="#054bb4"
lightblue="#658cc2"
grey="#5db6169"
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
    def __init__(self,match_id,node1,node2):
        self.match_id=match_id
        self.node1=node1
        self.node2=node2

class Graph1:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.matchings = []
        self.node_id = 0
        self.edge_id = 0
      
    def addNode(self,node):
        self.nodes.append(node)
        return self
    def removeNode(self,node):
        self.nodes=[nodes for nodes in self.nodes if node!=nodes]
        self.edges=[edges for edges in self.edges if edges.node1!=node and edges.node2!=node]
        self.matchings=[matches for matches in self.matchings if matches.node1!=node and matches.node2!=node]

        #return self
    
    def addEdge(self,edge):
        if edge.node1.node_id > edge.node2.node_id:
        # Swap nodes if node1 has a greater node_id than node2
            edge = Edge(self.edge_id, edge.node2, edge.node1)
        for index, existing_edge in enumerate(self.edges):
        # Compare node IDs to determine the insertion position
            if existing_edge.node1.node_id > edge.node1.node_id or (existing_edge.node1.node_id == edge.node1.node_id and existing_edge.node2.node_id > edge.node2.node_id):
                self.edges.insert(index, edge)
                break
        else:
            # If the loop completes without breaking, append to the end
            self.edges.append(edge)
        self.edge_id += 1
        return self

    def removeEdge(self,edge):
        self.edges=[edges for edges in self.edges if edge.edge_id!=edges.edge_id]
        return self
    
    def addMatching(self,edge):
        print("add matching",edge.node1.node_id,edge.node2.node_id)

        for matching in self.matchings:
            if edge.node1==matching.node1 or edge.node1==matching.node2 or edge.node2==matching.node1 or edge.node2==matching.node2:
                return print("INVALID MATCHING")
        self.removeEdge(edge)
        match=Matching(edge.edge_id,edge.node1,edge.node2)
        self.matchings.append(match)
        for match in self.matchings:
            print("MATCHINGS",match.node1.node_id,match.node2.node_id)
        
        return self
        
    def removeMatching(self,edge):
        self.matchings=[match for match in self.matchings if edge!=match]
        edge=Edge(edge.match_id,edge.node1,edge.node2)
        self.addEdge(edge)
        return self
    
    @staticmethod
    def uploadGraph(file):
        graph = Graph1()
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
                        node=Node(node_id,x,y)
                        graph.addNode(node)
                    elif current_section == "Edges":
                        parts = line.strip("()").split("),(")
                        for part in parts:
                            edge_id, node1_id, node2_id = map(int, part.split(","))
                            node1 = next((node for node in graph.nodes if node.node_id == node1_id), None)
                            node2 = next((node for node in graph.nodes if node.node_id == node2_id), None)
                            
                            if max_edgeID<=edge_id:
                                max_edgeID=edge_id+1
                            if node1 and node2:
                                edge=Edge(edge_id,node1,node2)
                                graph.addEdge(edge)
                    elif current_section == "Matchings":
                        parts = line.split(",")
                        edge_id, node1_id, node2_id = map(int, parts)
                        node1 = next((node for node in graph.nodes if node.node_id == node1_id), None)
                        node2 = next((node for node in graph.nodes if node.node_id == node2_id), None)
                        if max_edgeID<=edge_id:
                                max_edgeID=edge_id+1
                        if node1 and node2:
                            graph.addMatching(Edge(edge_id, node1, node2))
        
        return graph,max_nodeID,max_edgeID
    
    def unMatchedNeigh(self,node):
        neighbours=[]
        for edge in self.edges:
            if node.node_id==edge.node1.node_id:
                neighbours.append(edge.node2.node_id)
            elif node.node_id==edge.node2.node_id:
                neighbours.append(edge.node1.node_id)
        return neighbours
    def findEdge(self,node1_id,node2_id):
        for edge in self.edges:
            if (edge.node1.node_id==node1_id and edge.node2.node_id==node2_id) or (edge.node1.node_id==node2_id and edge.node2.node_id==node1_id):
                return edge
            

class InputGUI:
    def __init__(self,file=None):
        
        self.root = tk.Tk()
        self.root.style = ttk.Style() # type: ignore
        self.root.style.theme_use('clam')  # type: ignore # Change the theme to 'clam' for a modern look
        self.root.style.configure("Custom.TButton", foreground="white", background=lightblue, padding=20, font=("Helvetica", 20)) # type: ignore
        self.root.title("INPUT Graph ")
        self.x_size=500
        self.y_size=700
        self.root.geometry("{}x{}".format(self.x_size, self.y_size))
        self.root.geometry("+10+10")
        self.canvas1 = tk.Canvas(self.root, bg=lightblue, height=2000, width=500)
        self.canvas1.pack(fill=tk.BOTH)

        
        
        self.active_edge = Edge(-1,Node(-1,-1,-1),Node(-1,-1,-1))
        
        self.node_radius=20
        
        

        self.input_entry = tk.Entry(self.canvas1)
        self.input_entry.place(x=60, y=140, anchor="w")
        
        self.save_button = tk.Button(self.canvas1, text="Save", command=self.save)
        self.save_button.place(x=90, y=140, anchor="e")
        
        self.execute_button = tk.Button(self.canvas1,text="Execute",command=self.execute)
        self.execute_button.place(x=50, y=40) 
    
        if file==None:
            self.graph = Graph1()
            
            
        else:
            self.graph,max_node,max_edge = Graph1.uploadGraph(file)
            self.graph.node_id=max_node
            self.graph.edge_id=max_edge
            self.displayGraph()
            #for nodes in self.graph.nodes:
            #    print("Nodes:",nodes.node_id,nodes.x,nodes.y)
            #for edges in self.graph.edges:
            #    print("edges:",edges.edge_id,edges.node1.node_id,edges.node2.node_id)
           # for match in self.graph.matchings:
            #    print("matchings:",match.edge_id,match.node1.node_id,match.node2.node_id)


        self.n_pressed = False
        self.root.bind("<KeyPress-n>", self.nPressed)
        self.root.bind("<KeyRelease-n>", self.nReleased)
        self.e_pressed = False
        
        self.root.bind("<KeyPress-e>", self.ePressed)
        self.root.bind("<KeyRelease-e>", self.eReleased)
        
        
        self.canvas1.bind("<Button-1>",self.button1)
        
            


        
    def nPressed(self, event):
        self.n_pressed = True
        #print("N-T",self.n_pressed)
        return self.n_pressed

    def nReleased(self, event):
        self.n_pressed = False
        #print("N-F",self.n_pressed)
        return self.n_pressed
    
    def ePressed(self, event):
        self.e_pressed = True
        #print("E-T",self.e_pressed)
        return self.e_pressed

    def eReleased(self, event):
        self.e_pressed = False
        #print("E-F",self.e_pressed)
        return self.e_pressed

    def button1(self,event):
        if self.n_pressed==True:
            self.editNodes(event)
        elif self.e_pressed==True:
            self.drawEdge(event)
        elif self.n_pressed==False and self.e_pressed==False:
            
            self.changeMatching(event)

    def changeMatching(self,event):
        
        p=self.proximal(event)
        
            
        if (isinstance(p,Edge)==True):
            self.graph.addMatching(p)
        if (isinstance(p,Matching)==True):
            
            self.graph.removeMatching(p)

        self.displayGraph()
    
    def endEdge(self,event):
        p = self.proximal(event)
        if self.active_edge and isinstance(p, Node) and self.active_edge.node1 != p:
            self.active_edge.node2 = p # type: ignore
            edge=Edge(self.graph.edge_id, self.active_edge.node1, self.active_edge.node2)
            self.graph.addEdge(edge)
            self.graph.edge_id += 1
        self.canvas1.unbind("<B1-Motion>")
        self.canvas1.unbind("<ButtonRelease-1>")
        #print("end edge at node:",self.active_edge.node2.node_id)
        self.active_edge = Edge(-1,Node(-1,-1,-1),Node(-1,-1,-1))

        self.displayGraph()
        return self

    def tempEdge(self, event):
        self.canvas1.delete("temp_edge")
        if self.active_edge:
            start_x, start_y = self.active_edge.node1.x, self.active_edge.node1.y
            end_x, end_y = event.x, event.y
            self.canvas1.create_line(start_x, start_y, end_x, end_y, fill="blue", tags="temp_edge")
            self.canvas1.bind("<ButtonRelease-1>", self.endEdge)

    def drawEdge(self, event):
        p=self.proximal(event)
        
        if isinstance(p,Node):
            #print("start edge at node:",p.node_id)
            
            self.active_edge.node1 = p
            self.canvas1.bind("<B1-Motion>",self.tempEdge)
        
            
            



    def editNodes(self,event):
        p = self.proximal(event)
        
        if p == 0:
            node = Node(self.graph.node_id, event.x, event.y)
            self.graph.node_id += 1
            self.graph.addNode(node)
        elif isinstance(p, Node):
            #print("DELETE NODE")
            self.graph.removeNode(p)
        self.displayGraph()

        
    def delete_shapes_in_region(self, canvas, x1, y1, x2, y2):
        items_in_region = self.canvas1.find_overlapping(x1, y1, x2, y2)
        for item in items_in_region:
            self.canvas1.delete(item)

    def displayGraph(self):
        self.delete_shapes_in_region(self.canvas1, 0, 0, self.x_size, self.y_size)
        
        self.graph.nodes=sorted(self.graph.nodes, key=lambda node: node.node_id)  
        #self.graph.edges=sorted(self.graph.edges, key=lambda edge: edge.node1.node_id)  
        #self.graph.matchings=sorted(self.graph.matchings, key=lambda match: match.node1.node_id) 


        for edge in self.graph.edges:
            self.canvas1.create_line(edge.node1.x,edge.node1.y,edge.node2.x,edge.node2.y,fill="blue",width=10)
            print("EDGE: ",edge.edge_id,edge.node1.node_id,edge.node2.node_id)
        for matching in self.graph.matchings:
            self.canvas1.tag_raise(self.canvas1.create_line(matching.node1.x,matching.node1.y,matching.node2.x,matching.node2.y,fill="red",width=10))
            print("MATCH: ",matching.match_id,matching.node1.node_id,matching.node2.node_id)

        for node in self.graph.nodes:
            self.canvas1.create_oval(node.x - self.node_radius, node.y - self.node_radius, node.x + self.node_radius, node.y + self.node_radius, fill="white")
            self.canvas1.tag_raise(self.canvas1.create_text(node.x, node.y, font=("Purisa", 20), text=str(node.node_id)))
            print("NODE: ",node.node_id,node.x,node.y)
    

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

        r = self.node_radius
        for node in self.graph.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                #print("Node clicked", node.node_id)
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
                #print("MATCHING clicked:", match.node1.node_id,match.node2.node_id)
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
                #print("Edge clicked:", edge.node1.node_id,edge.node2.node_id)
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
                file.write(f"{match.match_id},{match.node1.node_id},{match.node2.node_id}\n")
        print(f"Graph data saved to {filename}")

    

    def run(self):
        self.root.mainloop()






    def highlightEdge(self,edge):
        self.canvas1.tag_lower(self.canvas1.create_line(edge.node1.x,edge.node1.y,edge.node2.x,edge.node2.y,fill="black",width=20))
    def highlightNode(self,node):
        r=35
        self.canvas1.tag_lower(self.canvas1.create_oval(node.x-r,node.y-r,node.x+r,node.y+r,fill="black"))

    def execute(self):

        graph_copy = copy.deepcopy(self.graph)
        algoMain(graph_copy)

        
class TreeNode:
    def __init__(self,value,children=None,x=None,y=None):
        self.value=value
        self.children=children
        self.x=x
        self.y=y


class Tree:
    def __init__(self,root):
        self.root=root
        
    def add_child(self, parent, child):
        parent.children.append(child)

def draw_tree(canvas, node, x, y, level_width=80, level_height=50):
    if not node:
        return

    # Constants for drawing
    RADIUS = 20

    # Draw node
    canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill="skyblue")
    canvas.create_text(x, y, text=node.value.node_id)

    # Recursively draw children
    child_y = y + level_height
    if node.children!=None:
        for i, child in enumerate(node.children):
            child_x = x + (i - len(node.children) / 2) * level_width
            canvas.create_line(x, y, child_x, child_y, fill="gray")
            draw_tree(canvas, child, child_x, child_y)

def draw_forest(canvas, forest):
    canvas.delete("all")  # Clear canvas

    start_x = 80  # Starting x-coordinate for the first tree
    y=50
    for tree in forest:
        draw_tree(canvas, tree.root, start_x, y)
        start_x += 90  # Increase start_x for the next tree
        tree.root.x=start_x
        tree.root.y=y
    return forest

def setup_forest(roots):
    # Create a simple forest for demonstration
    forest = []
    
    for r in roots:
        root = TreeNode(r)
        tree = Tree(root)
        forest.append(tree)
    return forest

def algoMain(graph):
    root2 = tk.Tk()
    root2.title("Forest Visualization")

    x_size=800
    y_size=700
    root2.geometry("{}x{}".format(x_size,y_size))
    
    canvas = tk.Canvas(root2, width=x_size, height=y_size, bg="white")
    canvas.pack(fill="both", expand=True)
    root2.geometry("+{}+{}".format(500,10))
    # Button to draw the forest
    draw_button = tk.Button(root2, text="Draw Forest", command=lambda: draw_forest(canvas, forest))
    draw_button.pack()



    ed=EdmondsMethods(graph)
    roots = ed.getRoots()
    roots=sorted(roots, key=lambda node: node.node_id)        
    forest = setup_forest(roots)
    print("START__PLANT__ROOTS")
    draw_forest(canvas,forest)
    print("END__PLANT__ROOTS")
    first_edges = ed.firstLayer(forest)
   
    

    if first_edges is not None:
        for edge in first_edges:
            # Ensure coordinates are fetched from the current graph's node positions
            ##TAG
            start_node, end_node = edge.node1, edge.node2
            # Calculate bounding box for the arc based on start and end node positions
            bbox = (start_node.x, start_node.y, end_node.x, end_node.y)
            # Draw the arc on the canvas
            canvas.create_arc(bbox, start=0, extent=180, style=tk.ARC, outline="red", tags="arc")
            

    root2.mainloop()


    

class EdmondsMethods:
    def __init__(self,graph):
        self.graph1 = graph
         
    def getRoots(self):
        sat_nodes=[]
        
        for match in self.graph1.matchings:
            sat_nodes.append(match.node1.node_id)
            sat_nodes.append(match.node2.node_id)
        
        unsat_nodes = set()

        for node in self.graph1.nodes:
            if node.node_id not in sat_nodes:
                unsat_nodes.add(node)  # Add unsaturated nodes to the list

        return unsat_nodes

    def firstLayer(self,forest):
        visited=set()
        first_layer_nodes=[]
        for tree in forest:
            print(tree.root.value.node_id,"Has unvisted,unmatched neighbours:")
            
            if tree.root.value.node_id not in visited:
                visited.add(tree.root.value.node_id)
                for edge in self.graph1.edges:
                    add_node=None
                    if tree.root.value.node_id==edge.node1.node_id:
                        add_node=edge.node2
                        visited.add(add_node.node_id)
                    else:
                        if tree.root.value.node_id==edge.node2.node_id:
                        
                            add_node=edge.node1
                            visited.add(add_node.node_id)
                    
                    if add_node!=None:
                        self.graph1.edges = [edge for edge in self.graph1.edges if (edge.node1.node_id not in visited)and( edge.node2.node_id not in visited) ]
                        add_edge = Edge(edge.edge_id,add_node,tree.root.value)
                        first_layer_nodes.append(add_edge)
                        print("UNM_neighbours:",add_node.node_id)
                        
                    continue
                print("VISITED==",visited)
                for edge in self.graph1.edges:
                    print("REMAINING AVAILABLE EDGES",edge.node1.node_id,edge.node2.node_id)
                    
        return first_layer_nodes
        
            
        # need to draw first layer of arcs in trees for CASE: all unsat node

    


    
    
           
class HomeGui:
    def __init__(self):
        self.root1 = tk.Tk()
        
        self.root1.title("HOME")
        self.root1.geometry("500x500")
        self.canvas = tk.Canvas(self.root1, bg=lightblue)

        self.input_graph = ttk.Button(self.canvas, text="INPUT OWN GRAPH", command=self.inputTool,style="Custom.TButton")
        self.input_graph.place(x=250, y=140, anchor="center")

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select a file")

        self.dropdown = ttk.Combobox(self.canvas, textvariable=self.dropdown_var, state="readonly",style="Custom.TCombobox")
        self.dropdown.place(x=250, y=250, anchor="center")
        self.populate_dropdown()

        self.dropdown.bind("<<ComboboxSelected>>", self.update_selected_value)
        
        style = ttk.Style()
        style.theme_use('clam')  # Change the theme to 'clam' for a modern look
        style.configure("Custom.TButton", foreground="white", background=darkblue, padding=20, font=("Helvetica", 20))
        style.map("Custom.TButton", background=[("active", darkblue)],foreground=[], padding=[], font=[])  # Keep the same background color when pressed
        style.configure("Custom.TCombobox", padding=20, font=("Helvetica", 20),background=darkblue,foreground="white")
        

        style.map("Custom.TCombobox", background=[("active", grey)])  # Change background color when pressed

        self.canvas.pack(fill=tk.BOTH, expand=True)
         

    def populate_dropdown(self):
        current_dir = os.getcwd()
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        self.dropdown["values"] = files

    def update_selected_value(self, event):
        selected_value = self.dropdown_var.get()
        self.uploadTool(selected_value)

    def inputTool(self):
        input_gui_instance = InputGUI()
        
        input_gui_instance.run()

    def uploadTool(self, file):
        uploadGraphGUI = InputGUI(file)
        uploadGraphGUI.run()

    def run(self):
        self.root1.mainloop()
home_gui = HomeGui()
home_gui.run()
