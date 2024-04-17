import tkinter as tk
from tkinter import ttk,scrolledtext

import time
from collections import deque
import os
import math
import copy
from collections import OrderedDict
import networkx as nx
class Graph(nx.Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the set that will hold matchings
        self.matchings = set()
        self.node_count = 0



    def new_node(self,event,node_id=None,x=None,y=None):
        self.node_count+=1
        if event!=None:
            self.add_node(self.node_count ,x=int(event.x), y=int(event.y))
        elif event==None and x!=None and y!=None:
            self.add_node(node_id ,x=x, y=y)

    def delete_node(self, node_id):
        if self.has_node(node_id):
            # Prepare a set of edges to remove from the matchings
            to_remove = {(u, v) for u, v in self.matchings if u == node_id or v == node_id}
            # Remove these edges from the matchings
            self.matchings.difference_update(to_remove)
            # Remove the node, which also removes its edges
            self.remove_node(node_id)
            print(f"Node {node_id} and related matchings removed.")
        else:
            print(f"Node {node_id} does not exist.")
    
    def change_matching(self, edge):
        u, v = edge[1]  # Directly unpack the edge tuple
        print("Edge to toggle matching:", edge, "Nodes:", u, v)
        print("***",u,v)
        if (u, v) in self.matchings or (v, u) in self.matchings:
            # Remove the matching if it already exists
            self.matchings.discard((u, v))
            self.matchings.discard((v, u))
            print("Matching removed for edge:", edge)
        else:
            # Add the edge as a new matching only if it does not create invalid matching
            if self.is_valid_matching(u, v):
                self.matchings.add((u, v))
                print("Matching added for edge:", edge)
            else:
                print("Invalid matching, edge not added:", edge)

        
    def is_valid_matching(self, u, v):
        # Check if either node is already in the matching set
        print("U,V",u,v)
        for edge in self.matchings:
            x,y=edge
            print("%%%%7",x,y)
            if u == x or u == y or v == x or v == y:
                return False
        return True

    def delete_edge(self, edge):
        u,v=edge[1]
          # Unpacking the tuple
        print("Edge to delete:", edge, "Nodes:", u, v)
        if self.has_edge(u, v):
            print("Deleting edge")
            self.remove_edge(u, v)
            for match in self.matchings:
                if (u,v) == match:
                    print("DELETE MATCHING")
                    self.matchings.remove(match)
                    break
                
    def unsat_nodes(self):
        sat=set()
        
        for edge in self.matchings:
            x,y=edge
            
            sat.add(x)
            sat.add(y)

        all_nodes = set(self.nodes())

        unsat = all_nodes - sat

        unsat_coords = {}

        for node in unsat:
            node_data = self.nodes[node]
            unsat_coords[node] = (node_data['x'], node_data['y'])
        unsat_coords = {k: unsat_coords[k] for k in sorted(unsat_coords)}
        return unsat_coords

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
        r = 30
        
        for node_id, data in self.nodes(data=True):
        # Ensure x and y are integers
            x = int(data['x'])  # Convert x and y to integers
            y = int(data['y'])
        
        # Calculate distance
            distance = math.sqrt((event.x - x) ** 2 + (event.y - y) ** 2)

        # Check if this node is closer and within radius r
            if distance <= r:
                #print("Node clicked", node.node_id)
                return node_id
            


        min_distance = float('inf')
        closest_edge = None
        for u, v in self.edges():
            x1, y1 = self.nodes[u]['x'], self.nodes[u]['y']
            x2, y2 = self.nodes[v]['x'], self.nodes[v]['y']
            distance = self.point_distance(x1, y1, x2, y2, event.x, event.y)
            if distance < min_distance and distance <= r:
                min_distance = distance
                closest_edge = (u, v)

        if closest_edge:
            return ('edge', closest_edge)

        return None

        
    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            phase = 'nodes'  # Start with nodes, switch to edges upon encountering the "# Edges" marker
            for line in file:
                line = line.strip()
                if line == "# Edges":
                    phase = 'edges'  # Switch to reading edges
                    continue

                if phase == 'nodes':
                    node_id, x_part, y_part = line.split(',')
                    node_id = int(node_id)
                    x = int(x_part.split('=')[1])
                    y = int(y_part.split('=')[1])
                    
                    self.new_node(None,node_id=node_id,x=x,y=y)

                elif phase == 'edges':
                    u, v, matched = line.split(',')
                    u = int(u)
                    v = int(v)
                    if matched=="True":
                        matched=True
                    elif matched == "False":
                        matched= False
                    print("load edges",u,v,matched)
                    self.add_edge(u, v)
                    if matched:
                        
                        self.matchings.add((u, v))
            print("nodes",self.nodes())
            print("edges",self.edges())
            print("magtchings",list[self.matchings])
            print(f"Graph loaded from {filename}")

    




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
        
        self.active_edge=[-1,-1]
        

        self.input_entry = tk.Entry(self.canvas1)
        self.input_entry.place(x=60, y=140, anchor="w")
        
        self.save_button = tk.Button(self.canvas1, text="Save", command=self.save)
        self.save_button.place(x=90, y=140, anchor="e")

        
        self.graph = Graph()
        
        if file:
            self.load_graph(file, self.graph, self.canvas1)
            
        
            

       
            

        self.n = False
        self.root.bind("<KeyPress-n>", self.n_pressed)
        self.root.bind("<KeyRelease-n>", self.n_released)
        self.e = False
        
        self.root.bind("<KeyPress-e>", self.e_pressed)
        self.root.bind("<KeyRelease-e>", self.e_released)
        
        
        self.canvas1.bind("<Button-1>",lambda event: self.button1(event, self.graph, self.canvas1))

        self.execute_button = tk.Button(self.canvas1,text="Execute",command=lambda: self.execute(self.graph, self.canvas1))
        self.execute_button.place(x=50, y=40) 
        
    def load_graph(self, filename, graph, canvas):
        if filename:
            self.graph.load_from_file(filename)
            self.display_graph(graph,canvas)
            
        else:
            print("Please enter a file name.")
    
    def n_pressed(self, event):
        self.n = True
        #print("N-T",self.n)
        return self.n

    def n_released(self, event):
        self.n = False
        #print("N-F",self.n)
        return self.n
    
    def e_pressed(self, event):
        self.e = True
        #print("E-T",self.e)
        return self.e

    def e_released(self, event):
        self.e = False
        #print("E-F",self.e)
        return self.e
    
    def button1(self,event,graph,canvas):
        
        p=graph.proximal(event)
        if self.n==True:
            ##EDIT NODES
            if p==None:
                #ADD NODES
                graph.new_node(event)
                self.display_graph(graph,canvas)
                
                
            elif isinstance(p,int):
                graph.delete_node(p)
                self.display_graph(graph,canvas)

        elif self.e==True:
            if isinstance(p,int):
                self.draw_edge(event,graph,canvas)
            elif isinstance(p,tuple):
                graph.delete_edge(p)
                self.display_graph(graph,canvas)
                
        elif self.e==False and self.n==False and isinstance(p,int)==False and p!=None :   
            
            graph.change_matching(p)
            self.display_graph(graph,canvas)
            #self.graph.displayAdj(self.canvas1)
        return self  

    def draw_edge(self, event,graph,canvas):
        p = graph.proximal(event)
        if isinstance(p, int):
            # Start edge at node p
            self.active_edge[0] = p
            # Bind motion to the canvas to update the temporary edge
            canvas.bind("<B1-Motion>",lambda event: self.temp_edge(event, self.graph, self.canvas1))
            canvas.bind("<ButtonRelease-1>", lambda event: self.end_edge(event, self.graph, self.canvas1))  # Ensure end edge on release

    def temp_edge(self, event,graph,canvas):
        if self.active_edge[0] != -1:
            # Clear any existing temporary edge
            canvas.delete("temp_edge")
            # Get start node coordinates
            start_x, start_y = graph.nodes[self.active_edge[0]]['x'], graph.nodes[self.active_edge[0]]['y']
            # Draw a line from start node to current mouse position
            canvas.create_line(start_x, start_y, event.x, event.y, fill="blue", tags="temp_edge")

    def end_edge(self, event,graph,canvas):
        p = graph.proximal(event)
        if self.active_edge[0] != -1 and isinstance(p, int) and p != self.active_edge[0]:
            # Create a permanent edge if the release is on a different node
            graph.add_edge(self.active_edge[0], p)
            self.display_graph(graph,canvas)
        # Clean up
        canvas.delete("temp_edge")
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<ButtonRelease-1>")
        self.active_edge = [-1, -1]  

        
    
        

    def display_graph(self,graph,canvas,colour=None):
        
        node_radius = 20
        if canvas == self.canvas1:
            print("Displaying on canvas1")
            canvas.delete("all")  # Clear the canvas entirely to redraw.
            for u, v in graph.edges():
                #print("EDGES:",u,v)
                if graph.has_node(u) and graph.has_node(v):  # Check if both nodes exist
                    line_color = "blue" 
                    #print(line_color)
                    x1, y1 = graph.nodes[u]['x'], graph.nodes[u]['y']
                    x2, y2 = graph.nodes[v]['x'], graph.nodes[v]['y']
                    canvas.create_line(x1, y1, x2, y2, fill=line_color, width=2)
                    
            for edge in graph.matchings:
            
                u,v=edge
                #print("MATCHINGS:",u,v)
                if graph.has_node(u) and graph.has_node(v):  # Check if both nodes exist
                    line_color = "red" 
                    #print(line_color)
                    x1, y1 = graph.nodes[u]['x'], graph.nodes[u]['y']
                    x2, y2 = graph.nodes[v]['x'], graph.nodes[v]['y']
                    canvas.create_line(x1, y1, x2, y2, fill=line_color, width=2)
                    
            
            for node_id in list(graph.nodes()):
                if graph.has_node(node_id):  # Ensure node still exists
                    x, y = graph.nodes[node_id]['x'], graph.nodes[node_id]['y']
                    canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="white", outline="black")
                    canvas.create_text(x, y, text=str(node_id))
                    
            
        
        
        # Drawing edges first
        
    def save(self):
        
        filename = f"{self.input_entry.get()}.txt"
        with open(filename, 'w') as file:
            # Saving nodes with coordinates
            for node in self.graph.nodes(data=True):
                print("node!!",node[0],node[1])

                file.write(f"{node[0]},x={node[1]['x']},y={node[1]['y']}\n")
            
            # Saving edges with matching information
            file.write("# Edges\n")
            for edge in self.graph.edges():
                
                is_matched = 'True' if edge in self.graph.matchings or (edge[1], edge[0]) in self.graph.matchings else 'False'
                print("EDGE!!",edge,is_matched)
                file.write(f"{edge[0]},{edge[1]},{is_matched}\n")
        
        print(f"Graph saved as {filename}")


    def execute(self,graph,canvas):
        self.setup_tree_window()
        
        self.algo_main(graph,canvas)

    

    def setup_tree_window(self):
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
        self.canvas2_xoffset = 510
        return self

    def algo_main(self,graph,canvas):
        copyGraph=Graph()
        copyGraph=copy.deepcopy(graph)
        matchedGraph ,unmatchedGraph= self.separate_matched_unmatched(copyGraph)
        self.tree = Graph()
        #self.display_graph(copyGraph, self.canvas2)

        #self.display_graph(matchedGraph, self.canvas2,colour="red")
        #self.display_graph(unmatchedGraph, self.canvas2,colour="blue")

        #edges2add = []
        unsat = copyGraph.unsat_nodes()
        print("unsat",unsat)
        children = self.grow_unmatched(copyGraph,canvas,unmatchedGraph,unsat)
        print("children",children)

    def display_tree(self, tree, canvas):
        #canvas.delete("all")
        node_radius = 20
        for u, v in tree.edges():
            x1, y1 = tree.nodes[u]['x'], tree.nodes[u]['y']
            x2, y2 = tree.nodes[v]['x'], tree.nodes[v]['y']
            canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
        for edge in tree.matchings:
            
            u,v=edge
            print("MATCHINGS:",u,v)
            if tree.has_node(u) and tree.has_node(v):  # Check if both nodes exist
                line_color = "red" 
                
                x1, y1 = tree.nodes[u]['x'], tree.nodes[u]['y']
                x2, y2 = tree.nodes[v]['x'], tree.nodes[v]['y']
                canvas.create_line(x1, y1, x2, y2, fill=line_color, width=2)
                    
        
        for node_id in tree.nodes():
            x, y = tree.nodes[node_id]['x'], tree.nodes[node_id]['y']
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="white", outline="black")
            canvas.create_text(x, y, text=str(node_id))
        canvas.update()  # Ensure the canvas is updated immediately


    def add_nodes_and_edges_with_delay(self, nodes, edges, canvas, index=0, delay=300):
            """Adds nodes and edges to the canvas with a delay."""
            if index < len(nodes):
                node_id, (x, y) = nodes[index]
                self.tree.new_node(None, node_id=node_id, x=x, y=y)  # Assuming new_node handles drawing
                self.display_tree(self.tree, canvas)  # Update display
                # Schedule next node addition
                canvas.after(delay, self.add_nodes_and_edges_with_delay, nodes, edges, canvas, index + 1, delay)
            elif edges:
                edge = edges.pop(0)
                u, v = edge
                if self.tree.has_node(u) and self.tree.has_node(v):
                    self.tree.add_edge(u, v)
                    self.display_tree(self.tree, canvas)  # Update display after adding an edge
                    # Schedule next edge addition
                    canvas.after(delay, self.add_nodes_and_edges_with_delay, nodes, edges, canvas, index, delay)

    def grow_unmatched(self, graph, canvas, unmatchedGraph, leaves):
        nodes=[]
        edges = []
        children = []
        for node in leaves:
            
            node = int(node)
            next_node = sorted(list(nx.descendants_at_distance(unmatchedGraph, node, 1)))[0]
            print(node,next_node)
            nodes.append((node,(self.graph.nodes[node]['x'],self.graph.nodes[node]['y'])))
            nodes.append((next_node,(self.graph.nodes[next_node]['x'],self.graph.nodes[next_node]['y'])))
            print("1",unmatchedGraph.edges())
            unmatchedGraph.delete_node(node)
            print("2",unmatchedGraph.edges())
            edges.append((node, next_node))
            children.append(next_node)
        if edges:
            self.add_nodes_and_edges_with_delay(sorted(nodes), sorted(edges, key=lambda x: min(x)), self.canvas2)
            next_edge = edges.pop(0)
        return children
    def separate_matched_unmatched(self,graph):
        self.matched_graph = nx.Graph()
        self.unmatched_graph = nx.Graph()

    # Add all nodes to both graphs to ensure they have the same nodes
        for node, data in graph.nodes(data=True):
            self.matched_graph.add_node(node, **data)
            self.unmatched_graph.add_node(node, **data)

    # Add edges to matched and unmatched graphs appropriately
        for u, v, data in graph.edges(data=True):
            if (u, v) in graph.matchings or (v, u) in graph.matchings:
                self.matched_graph.add_edge(u, v, **data)
            else:
                self.unmatched_graph.add_edge(u, v, **data)

        return self.matched_graph, self.unmatched_graph



    def run(self):
        self.root.mainloop()






class HomeGui:
    def __init__(self):
        self.root1 = tk.Tk()
        
        self.root1.title("HOME")
        self.root1.geometry("500x500")
        self.canvas = tk.Canvas(self.root1, bg="lightblue")

        self.input_graph = ttk.Button(self.canvas, text="INPUT OWN GRAPH", command=self.input_tool,style="Custom.TButton")
        self.input_graph.place(x=250, y=140, anchor="center")

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select a file")

        self.dropdown = ttk.Combobox(self.canvas, textvariable=self.dropdown_var, state="readonly",style="Custom.TCombobox")
        self.dropdown.place(x=250, y=250, anchor="center")
        self.populate_dropdown()

        self.dropdown.bind("<<ComboboxSelected>>", self.update_selected_value)
        
        style = ttk.Style()
        style.theme_use('clam')  # Change the theme to 'clam' for a modern look
        style.configure("Custom.TButton", foreground="white", background="darkblue", padding=20, font=("Helvetica", 20))
        style.map("Custom.TButton", background=[("active", "darkblue")],foreground=[], padding=[], font=[])  # Keep the same background color when pressed
        style.configure("Custom.TCombobox", padding=20, font=("Helvetica", 20),background="darkblue",foreground="white")
        

        style.map("Custom.TCombobox", background=[("active", "grey")])  # Change background color when pressed

        self.canvas.pack(fill=tk.BOTH, expand=True)
         

    def populate_dropdown(self):
        current_dir = os.getcwd()
        txt_files = [f for f in os.listdir(current_dir) if f.endswith('.txt')]
        self.dropdown["values"] = txt_files

    def update_selected_value(self, event):
        selected_value = self.dropdown_var.get()
        self.upload_tool(selected_value)

    def input_tool(self):
        input_gui_instance = InputGUI()
        
        input_gui_instance.run()

    def upload_tool(self, file):
        uploadGraphGUI = InputGUI(file)
        uploadGraphGUI.run()

    def run(self):
        self.root1.mainloop()
home_gui = HomeGui()
home_gui.run()
