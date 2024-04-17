import tkinter as tk
from tkinter import ttk,scrolledtext


from collections import deque
import os
import math
import copy
from collections import OrderedDict





class Node:
    def __init__(self,node_id,x,y):
        self.node_id=node_id
        self.x=x
        self.y=y
        
    
    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Node):
            return self.node_id == other.node_id
        return False
    
    def __lt__(self, other):
        return self.node_id < other.node_id

    def __repr__(self):
        return f"{self.node_id}"

class AdjacencyList:
    def __init__(self):
        self.nodes = set()
        self.adj_list = OrderedDict()
        self.matched_nodes = set()  # Tracks nodes that are part of any matched edge.
        self.node_id = 0

    def addEdge(self, node1, node2, matched=False):
        if node1 in self.adj_list and node2 in self.adj_list:
            if not any(end_node == node2 for end_node, _ in self.adj_list[node1]):
                self.adj_list[node1].append((node2, matched))
                self.adj_list[node2].append((node1, matched))
                if matched:
                    self.matched_nodes.update([node1, node2])
                print(f"Edge added between {node1.node_id} and {node2.node_id}, Matched: {matched}")
                self.sortEdges(node1)
                self.sortEdges(node2)
            else:
                print(f"Edge already exists between {node1.node_id} and {node2.node_id}")
        else:
            print("One or both nodes do not exist in the graph.")

    def changeMatching(self, node1, node2):
    # Determine the current matching status of the edge
        current_matched = None
        for end_node, matched in self.adj_list[node1]:
            if end_node == node2:
                current_matched = matched
                break

        if current_matched is None:
            print("Edge does not exist.")
            return

        # If trying to match, ensure both nodes are not already matched in other edges
        if not current_matched:
            if any(matched for end_node, matched in self.adj_list[node1] if matched and end_node != node2):
                print("Invalid matching: Node", node1.node_id, "is already matched.")
                return
            if any(matched for end_node, matched in self.adj_list[node2] if matched and end_node != node1):
                print("Invalid matching: Node", node2.node_id, "is already matched.")
                return

        # Toggle the matching status
        for i, (end_node, matched) in enumerate(self.adj_list[node1]):
            if end_node == node2:
                self.adj_list[node1][i] = (node2, not matched)
        for i, (end_node, matched) in enumerate(self.adj_list[node2]):
            if end_node == node1:
                self.adj_list[node2][i] = (node1, not matched)

        # Update matched nodes set
        if not current_matched:
            self.matched_nodes.update([node1, node2])
            print("Edge between", node1.node_id, "and", node2.node_id, "matched successfully.")
        else:
            self.matched_nodes.discard(node1)
            self.matched_nodes.discard(node2)
            print("Match removed between", node1.node_id, "and", node2.node_id)


    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            # Remove node from adjacency lists of its neighbors
            for neighbor, _ in self.adj_list.pop(node, []):
                self.adj_list[neighbor] = [(n, m) for n, m in self.adj_list[neighbor] if n != node]
            print(f"Node {node.node_id} removed.")
    
    def sortEdges(self, node=None):
        if node:
            self.adj_list[node].sort(key=lambda edge: edge[0].node_id)
        else:
            for n in self.adj_list:
                self.adj_list[n].sort(key=lambda edge: edge[0].node_id)
    
   
    
    def uploadNode(self, node_id,x,y):
        node=Node(node_id,x,y)
        #print("NODE!!!!",node.node_id,node.x,node.y)
        if node not in self.nodes:
            self.nodes.add(node)  # Add the node to the set of nodes
            self.adj_list[node] = []  # Initialize its adjacency list
            self.node_id += 1 


    def addNode(self, event):
    
        n = Node(self.node_id, event.x, event.y)
        if n not in self.nodes:
            #print("hi")
            self.nodes.add(n)  # Add the node to the set of nodes
            self.adj_list[n] = []  # Initialize its adjacency list
            self.node_id += 1
            return 
        else:
            self.node_id += 1
            self.addNode(event)
    
    
        
    def printAdjList(self):
        print("PRINTING ADJ GRAPH:")
        for node in self.adj_list:
            for edge, is_matched in self.adj_list[node]:  # Unpack the tuple here
                print(node.node_id, "->", edge.node_id, "Matching:", is_matched)

    def getNeighbours(self,node):
        n = []
        for neigh,matched in self.adj_list[node]:
            n.append((neigh,matched))
        return n

    def displayAdj(self, canvas):
        
        self.printAdjList()
        for node in self.nodes:
            if node not in self.matched_nodes:
                print("!!UNMATCHED LSIT",node.node_id)
        
        node_radius = 20
    
        # Clear existing items
        items_in_region = canvas.find_overlapping(0, 0, 500, 700)
        for item in items_in_region:
            canvas.delete(item)
    
        # Note: No need to convert self.nodes to a set and sort again if it's already maintained as a sorted set.
        # Drawing edges
        for start_node in self.adj_list:
            for end_node, is_matched in self.adj_list[start_node]:  # Correctly unpack the tuple here
                if is_matched==True:
                    line_color = "red"
                else :
                    line_color="blue"  # Example: change line color based on matching status
                canvas.create_line(start_node.x, start_node.y, end_node.x, end_node.y, fill=line_color, width=10)

    # Drawing nodes
        for node in self.nodes:
            canvas.create_oval(node.x - node_radius, node.y - node_radius, node.x + node_radius, node.y + node_radius, fill="white")
            canvas.create_text(node.x, node.y, font=("Purisa", 20), text=str(node.node_id))
        return self
    def load_from_file(self, file):
        nodes=[]
        nodes2=[]
        edges={}
        node_lookup = {}  # Temporary dictionary to store Node objects by ID
        with open(file, 'r', encoding='utf-8') as file:
            data= file.read()
            for line in data.strip().splitlines():
                node_part, connections_part = line.split(':', 1)
                parts=node_part.split(",")
                node_id=0
                x=0
                y=0
                matched=False
                for part in parts:
                    if 'x=' in part:
                        x = int(part.split('=')[1])
                    elif 'y=' in part:
                        y = int(part.split('=')[1])
                    else:
                        #  Assuming the first part without 'x=' or 'y=' is the node_id
                        node_id = int(part)
                node1=Node(node_id,x,y)
                self.nodes.add(node1)
                self.adj_list[node1]=[]
                parts1 = connections_part.strip("-").split("-")
                
                
                for part in parts1:
                            a,b,c,d=part.split(",",4)
                            node_id=int(a)
                            x = int(b.split('=')[1])
                            y = int(c.split('=')[1])
                            matched = d.split(': ')[1]
                            if matched == "True":
                                matched=True
                            else:
                                matched=False
                            node2=Node(node_id,x,y)
                            #self.adj_list[node1].append((node2, matched))
                            self.addEdge(node1,node2,matched)
            
        return self
            
             



        

class InputGUI:
    def __init__(self,file=None):
        
        self.root = tk.Tk()
        self.root.style = ttk.Style() # type: ignore
        self.root.style.theme_use('clam')  # type: ignore # Change the theme to 'clam' for a modern look
        self.root.style.configure("Custom.TButton", foreground="white", background="lightblue", padding=20, font=("Helvetica", 20)) # type: ignore
        self.root.title("INPUT Graph ")
        self.x_size=500
        self.y_size=700
        self.root.geometry("{}x{}".format(self.x_size, self.y_size))
        self.root.geometry("+10+10")
        self.canvas1 = tk.Canvas(self.root, bg="lightblue", height=2000, width=500)
        self.canvas1.pack(fill=tk.BOTH)

        
        
        
        self.node_radius=20
        self.null_node=Node(-1,-1,-1)
        self.active_edge=[self.null_node,self.null_node]
        

        self.input_entry = tk.Entry(self.canvas1)
        self.input_entry.place(x=60, y=140, anchor="w")
        
        self.save_button = tk.Button(self.canvas1, text="Save", command=self.save)
        self.save_button.place(x=90, y=140, anchor="e")
        
        self.execute_button = tk.Button(self.canvas1,text="Execute",command=self.execute)
        self.execute_button.place(x=50, y=40) 
        self.graph = AdjacencyList()
        if file:
            self.load_graph(file)
            
        
            

       
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
        
            
    def load_graph(self,file):
          # Get filename from input entry
        if file:
            self.graph.load_from_file(file)
            self.graph.sortEdges()
            self.graph.displayAdj(self.canvas1)
        else:
            print("Please enter a file name.")

        
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
        p=self.proximal(event)
        if self.n_pressed==True:
            ##EDIT NODES
            if p==None:
                #ADD NODES
                self.graph.addNode(event)
                self.graph.displayAdj(self.canvas1)
                
                
            elif isinstance(p,Node):
                self.graph.removeNode(p)
                self.graph.displayAdj(self.canvas1)

        elif self.e_pressed==True:
            if isinstance(p,Node):
                self.drawEdge(event)
                
                #self.graph.displayAdj(self.canvas1)
        elif self.e_pressed==False and self.n_pressed==False and isinstance(p,Node)==False and p!=None :   
            print(p[0].node_id,p[1].node_id)
            self.graph.changeMatching(p[0],p[1])
            self.graph.displayAdj(self.canvas1)

        
        return self

    def endEdge(self,event):
        p = self.proximal(event)
        if self.active_edge and isinstance(p, Node) and self.active_edge[0] != p:
            self.active_edge[1] = p # type: ignore
            self.graph.addEdge(self.active_edge[0],self.active_edge[1])
        self.canvas1.unbind("<B1-Motion>")
        self.canvas1.unbind("<ButtonRelease-1>")
        #print("end edge at node:",self.active_edge.node2.node_id)
        self.active_edge = [self.null_node,self.null_node]

        self.graph.displayAdj(self.canvas1)
        return self

    def tempEdge(self, event):
        self.canvas1.delete("temp_edge")
        if self.active_edge:
            start_x, start_y = self.active_edge[0].x, self.active_edge[0].y
            end_x, end_y = event.x, event.y
            self.canvas1.create_line(start_x, start_y, end_x, end_y, fill="blue", tags="temp_edge")
            self.canvas1.bind("<ButtonRelease-1>", self.endEdge)

    def drawEdge(self, event):
        p=self.proximal(event)
        
        if isinstance(p,Node):
            #print("start edge at node:",p.node_id)
            
            self.active_edge[0] = p
            self.canvas1.bind("<B1-Motion>",self.tempEdge)
        
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
    
    def proximal(self,event):
        r = 35
        min_distance = float('inf')
        closest_edge = None
        for node in self.graph.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                #print("Node clicked", node.node_id)
                return node
        for start_node in self.graph.adj_list:
            for end_node,isMatching in self.graph.adj_list[start_node]:
                distance = self.point_distance( start_node.x, start_node.y, end_node.x, end_node.y,event.x, event.y)
                if distance < min_distance and distance <= r:
                    min_distance = distance
                    closest_edge = (start_node, end_node)

        if closest_edge:
            print(f"Edge clicked between Node {closest_edge[0].node_id} and Node {closest_edge[1].node_id}")
            return closest_edge

        return None
    
    
    def save(self):
        filename = f"{self.input_entry.get()}_adj_list.txt"
        with open(filename, 'w') as file:
            for node in self.graph.nodes:
                connections = []
                for edge, matched in self.graph.adj_list.get(node, []):
                    connection = f"{edge.node_id}, x={edge.x}, y={edge.y}, Matched: {matched}-"
                    connections.append(connection)
                connections_str = ''.join(connections)
                print("adding EDGE",f"{node.node_id}, x={node.x}, y={node.y}: {connections_str}\n")

                file.write(f"{node.node_id}, x={node.x}, y={node.y}: {connections_str}\n")
        print(f"Graph saved as {filename}")

    def execute(self):
        self.root1 = tk.Tk()
        self.root1.style = ttk.Style() # type: ignore
        self.root1.style.theme_use('clam')  # type: ignore # Change the theme to 'clam' for a modern look
        self.root1.style.configure("Custom.TButton", foreground="white", background="lightblue", padding=20, font=("Helvetica", 20)) # type: ignore
        self.root1.title("Tree Graph ")
        self.x_size=600
        self.y_size=700
        self.root1.geometry("{}x{}".format(self.x_size, self.y_size))
        self.root1.geometry("+510+10")
        self.canvas2 = tk.Canvas(self.root1, bg="lightblue", height=2000, width=500)
        self.canvas2.pack(fill=tk.BOTH)


        self.graph.printAdjList()
        
   


    

    def run(self):
        self.root.mainloop()




class HomeGui:
    def __init__(self):
        self.root1 = tk.Tk()
        
        self.root1.title("HOME")
        self.root1.geometry("500x500")
        self.canvas = tk.Canvas(self.root1, bg="lightblue")

        self.input_graph = ttk.Button(self.canvas, text="INPUT OWN GRAPH", command=self.inputTool,style="Custom.TButton")
        self.input_graph.place(x=250, y=140, anchor="center")

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select a file")

        self.dropdown = ttk.Combobox(self.canvas, textvariable=self.dropdown_var, state="readonly",style="Custom.TCombobox")
        self.dropdown.place(x=250, y=250, anchor="center")
        self.populateDropdown()

        self.dropdown.bind("<<ComboboxSelected>>", self.updateSelectedValues)
        
        style = ttk.Style()
        style.theme_use('clam')  # Change the theme to 'clam' for a modern look
        style.configure("Custom.TButton", foreground="white", background="darkblue", padding=20, font=("Helvetica", 20))
        style.map("Custom.TButton", background=[("active", "darkblue")],foreground=[], padding=[], font=[])  # Keep the same background color when pressed
        style.configure("Custom.TCombobox", padding=20, font=("Helvetica", 20),background="darkblue",foreground="white")
        

        style.map("Custom.TCombobox", background=[("active", "grey")])  # Change background color when pressed

        self.canvas.pack(fill=tk.BOTH, expand=True)
         

    def populateDropdown(self):
        current_dir = os.getcwd()
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        self.dropdown["values"] = files

    def updateSelectedValues(self, event):
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



