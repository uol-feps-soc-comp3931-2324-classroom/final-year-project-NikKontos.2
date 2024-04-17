import tkinter as tk
from tkinter import ttk,scrolledtext
import itertools

import time
from collections import deque
import os
import math
import copy
from sortedcontainers import SortedSet
import networkx as nx


def rgb_to_hex(r, g, b):
    """Converts RGB color values to hexadecimal string."""
    return f'#{r:02x}{g:02x}{b:02x}'

def generate_colour_variations(base_colour, brightness_decrement, total_variations):
    """Generate color variations from dark to lighter for a given base color, decrementing brightness each time."""
    variations = []
    for i in range(1, total_variations + 1):
        scale = 1 - brightness_decrement * (i - 1) / 100  # Apply decrement each step
        r = int(base_colour[0] * scale)
        g = int(base_colour[1] * scale)
        b = int(base_colour[2] * scale)
        variations.append((r, g, b))
    return variations

def create_colour_cycle(n, m):
    base_colours = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 255),  # Cyan
        (255, 0, 255),  # Magenta
    ]
    # Only use as many colors as needed
    base_colours = base_colours[:n] if n <= len(base_colours) else base_colours
    # Generate variations for each color
    all_colours = []
    for colour in base_colours:
        all_colours.extend(generate_colour_variations(colour, m, 1))  # Generate one variation per color with decremented brightness
    
    # Convert RGB to hexadecimal
    hex_colours = [rgb_to_hex(*colour) for colour in all_colours]
    
    # Cycle through colors indefinitely
    return itertools.cycle(hex_colours)








class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Graph(nx.Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.no_nodes=1
        

    def new_node(self, event=None, node_id=None, x=None, y=None):
        if event is not None:
            #print("EVENT")
            node_id = self.no_nodes
            self.no_nodes += 1
            x = int(event.x)
            y = int(event.y)
        elif node_id is not None and x is not None and y is not None:
            while self.no_nodes <= node_id:
                self.no_nodes += 1
        else:
            print("Error: No coordinates provided for the node.")
            return
        self.add_node(node_id, x=x, y=y)
    
    def delete_node(self, node_id):
        if self.has_node(node_id):
            self.remove_node(node_id)  # NetworkX's remove_node method
            #print(f"Node {node_id} removed.")
        else:
            print(f"Node {node_id} does not exist.")

    def toggle_matching(self, u, v):
        if self.has_edge(u, v):
            current_status = self[u][v].get('matched', False)

            if self.is_valid_matching(u,v):
                
                #print("CURRENTSTATUS",current_status)
                
                self[u][v]['matched'] = not current_status
                print(f"Matching status for edge ({u}, {v}): {self[u][v]['matched']}")
            elif current_status == True:
                current_status=self[u][v].get('matched', False)
                
                #print("CURRENTSTATUS1:",current_status)
                self[u][v]['matched'] = not current_status
                print(f"Matching status for edge ({u}, {v}): {self[u][v]['matched']}")
            

    def is_valid_matching(self, u, v):
        if any(self[u][w].get('matched', False) for w in self[u]):
            return False
        if any(self[v][w].get('matched', False) for w in self[v]):
            return False
        return True

    def display_graph1(self):
        for u, v, attrs in self.edges(data=True):
            print(f"Edge ({u}, {v}) with attributes {attrs}")
        for n, attrs in self.nodes(data=True):
            print(f"Node {n} with attributes {attrs}")

    def proximal(self, event, radius=30):
        # Implementing proximity check to select nodes or edges by clicking
        for node_id, data in self.nodes(data=True):
            x, y = data['x'], data['y']
            distance = math.sqrt((event.x - x) ** 2 + (event.y - y) ** 2)
            if distance < radius:
                return node_id  # Return the node ID within proximity
        
        for u, v in self.edges():
            x1, y1 = self.nodes[u]['x'], self.nodes[u]['y']
            x2, y2 = self.nodes[v]['x'], self.nodes[v]['y']
            distance = point_distance(x1, y1, x2, y2, event.x, event.y)
            if  distance <= radius:
                
                closest_edge = (u, v)
                return closest_edge
        
        return None

    def load_from_file(self,filename):
        try:
            with open(filename, 'r') as file:
                phase = 'nodes'  # Start with nodes, switch to edges upon encountering the "# Edges" marker
                for line in file:
                    line = line.strip()
                    if line == "# Edges":
                        phase = 'edges'  # Switch to reading edges
                        continue

                    if phase == 'nodes':
                        if line.startswith("#") or not line:
                            continue  # Skip comments or empty lines

                        node_id, x_part, y_part = line.split(',')
                        node_id = int(node_id)
                        x = int(x_part.split('=')[1])
                        y = int(y_part.split('=')[1])
                        self.new_node(None,node_id, x=x, y=y)

                    elif phase == 'edges':
                        if line.startswith("#") or not line:
                            continue
                        u, v, matched = line.split(',')
                        u = int(u)
                        v = int(v)
                        #print(matched,": matched",type(matched))
                        matched = matched == 'True'
                        self.add_edge(u, v, matched=matched)

            print(f"Graph loaded from {filename}")
        except Exception as e:
            print(f"Error loading graph from file {filename}: {e}")


def point_distance(x1, y1, x2, y2, x, y):
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


class Algorithm:
    def __init__(self, main_graph, colour_cycle=None):
        
        self.copy_graph=copy.deepcopy(main_graph)
        self.temp_graph=copy.deepcopy(main_graph)


        
        

        self.highlight_edges = set()

        
    
    def print_edges(self):
        for u,v,matched in self.copy_graph.edges(data=True):
            print("edge",u,v,matched['matched'])
        self.display_tree(self.copy_graph)

    def unsat_nodes(self):
        unsat = SortedSet()
        # Track nodes that are part of any matched edges
        matched_nodes = set()

        for u, v, attrs in self.copy_graph.edges(data=True):
            if attrs.get('matched', False):  # Use get to avoid KeyError
                matched_nodes.update([u, v])
        
        # Now, check for nodes not in matched_nodes
        for node_id,attrs in self.copy_graph.nodes(data=True):
            x, y = attrs['x'], attrs['y']
            if node_id not in matched_nodes:
                unsat.add(node_id)
                print(f"Added {node_id} to unsat")
        
        #print(f"Unsatisfied nodes: {list(unsat)}")
        
        return unsat
     
    def grow_unmatched(self,parents):
        new_edges = set()
        for parent in parents:

            neighbours = sorted(nx.descendants_at_distance(self.temp_graph,parent,1))
            
            if neighbours:
                #print("errrr",parent,"---",neighbours[0],self.temp_graph.nodes[neighbours[0]]['x'],self.temp_graph.nodes[neighbours[0]]['y'])
                new_edges.add((parent,neighbours[0]))
                
                for p in parents:
                    if p==neighbours[0]:
                        parents.remove(p)
                        print("AUG PATH BETWEEN ",parent,neighbours[0])
                self.copy_graph.delete_node(parent)
                self.temp_graph.delete_node(parent)
                self.temp_graph.delete_node(neighbours[0])    
        #self.temp_graph=self.copy_graph
        sorted_edges = sorted(new_edges, key=lambda x: parents.index(x[0]))            
        #self.tree.add_edge(parent,neighbours[0],matched=False)
        self.temp_graph=self.copy_graph
        
        return sorted_edges

    def grow_matched(self, parents):
        print("GROWMATCHED")
        parents_list = list(parents)  # Ensure parents is a list
        print(parents_list)
        new_edges = set()

        for parent in parents_list:
            if parent in self.copy_graph:
                print("parent in copy_graph", parent)
                for neighbor in self.copy_graph.neighbors(parent):
                    if self.copy_graph.has_edge(parent, neighbor) and self.copy_graph[parent][neighbor].get('matched', False):
                        new_edges.add((parent, neighbor))
                        print("new edges", new_edges)
                        print(f"Matched path found between {parent} and {neighbor}")
                        self.copy_graph.remove_node(parent)
                        self.temp_graph.remove_node(neighbor)

        sorted_edges = sorted(new_edges, key=lambda x: parents_list.index(x[0]))
        print("sorted matched edges", sorted_edges)
        self.temp_graph = self.copy_graph
        return sorted_edges
        

    


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
        
        
        
        

        
        self.line_number = 1
        
        
        self.n = False
        self.root.bind("<KeyPress-n>", self.n_pressed)
        self.root.bind("<KeyRelease-n>", self.n_released)
        self.e = False
        self.root.bind("<KeyPress-e>", self.e_pressed)
        self.root.bind("<KeyRelease-e>", self.e_released)
        
        self.canvas1.bind("<Button-1>",lambda event: self.button1(event))

        self.execute_button = tk.Button(self.canvas1,text="Execute",font=("Ariel",20),borderwidth=2,highlightcolor="black",foreground="black",highlightbackground="black",command=lambda: self.execute())
        self.execute_button.place(x=490, y=10,anchor="ne") 
        
        self.input_entry = tk.Entry(self.canvas1,width=20,font=("Ariel",20),borderwidth=2,highlightcolor="black",foreground="black",highlightbackground="black")
        default_text = "Save graph as (....).txt"
        self.input_entry.insert(0, default_text)
        self.input_entry.place(x=85, y=10, anchor="nw")
        
        self.save_button = tk.Button(self.canvas1, text="Save",font=("Ariel",20),borderwidth=2,highlightcolor="black",foreground="black",highlightbackground="black", command=self.save)
        self.save_button.place(x=10, y=10, anchor="nw")

        self.text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=4, width=35,font=("Ariel",20),bg="lightblue",borderwidth=2,highlightcolor="black",foreground="black",highlightbackground="black")
        self.text.place(x=10, y=60, anchor="nw")


        
        
        self.node_radius=20
        
        self.active_edge=[-1,-1]

        self.main_graph = Graph()
        
        if file:
            self.load_graph(file)
        self.highlight_edges = set()

    def on_enter_press(self,event):
            self.continue_execution = True  # Change the flag to True when Enter is pressed

    def execute(self,tree=None):
        #self.main_graph.display_graph1()


        
        self.root2 = tk.Tk()
        self.root2.style = ttk.Style() # type: ignore
        self.root2.style.theme_use('clam')  # type: ignore # Change the theme to 'clam' for a modern look
        self.root2.style.configure("Custom.TButton", foreground="white", background="lightblue", padding=20, font=("Helvetica", 20)) # type: ignore
        self.root2.title("INPUT Graph ")
        self.x_size=500
        self.y_size=700
        self.root2.geometry("{}x{}".format(self.x_size, self.y_size))
        self.root2.geometry("+505+10")
        self.canvas2 = tk.Canvas(self.root2, bg="lightblue", height=2000, width=500)
        self.canvas2.delete("all")
        self.canvas2.pack(fill=tk.BOTH)

        self.continue_execution = False
        self.root2.bind("<Return>", self.on_enter_press)
        self.highlight_edges = set()
        self.highlight_nodes = set()
        self.leaves = set()
        if tree==None:
            self.tree =Graph()
        else:
            self.tree=tree

        paths={}


        augment_flag=False
        while augment_flag==False:
            self.algo = Algorithm(self.main_graph) 
            unsat1 = list(self.algo.unsat_nodes())
            self.colour_cycle = create_colour_cycle(len(unsat1), 8)
            self.algo = Algorithm(self.main_graph,self.colour_cycle) 
            unsat1 = list(self.algo.unsat_nodes())
            self.highlight_nodes.union(unsat1)
            print("unsat1-",unsat1)
            
            
            for node in unsat1:
                paths[node]=[]
                self.tree.new_node(None,node,self.main_graph.nodes[node]['x'],self.main_graph.nodes[node]['y'])
                output = f"{self.line_number}__ Plant UNSATURATED node {node} as a root of the forest.\n"
                self.add_text(output)
                self.delay_graphic(self.tree,self.canvas2)
            print("1")
            new_unmatched_edges=self.algo.grow_unmatched(unsat1)
            
            
            
            #self.delay_graphic(self.tree,self.canvas2)
            #print("2")
            

            unsat2=self.algo.unsat_nodes()
            
            for u,v in new_unmatched_edges:
                self.tree.new_node(None,u,self.main_graph.nodes[u]['x'],self.main_graph.nodes[u]['y'])
                self.tree.new_node(None,v,self.main_graph.nodes[v]['x'],self.main_graph.nodes[v]['y'])
                paths[u].append(v)
                self.tree.add_edge(u,v)
                
                #print("unsat=",unsat1)
                print("!!")
                if u in unsat1 and v in unsat2:
                    augment_flag=True

                    continue
                    output = f"Line {self.line_number}: Nodes {u},{v} are both unsaturated so theyre adjoinging edge can be augmented!.\n"
                    self.add_text(output)
                    print(u,v,"AUGMENT")
                    self.main_graph.toggle_matching(u,v)
                    self.display_graph(self.main_graph,self.canvas1)
                    self.delay_graphic(self.tree,self.canvas2)
                    self.root.update()
                    self.root2.iconify()




                    self.execute()
                    print("4")
                
                elif u in unsat1 and v not in unsat2:
                    self.leaves.add(v)
                    output = f"{self.line_number}__ LOWEST NODE IN TREE {u}: - SMALLEST neighbour is {v} \n \t - {v} is SATURATED so \n \t--> Edge ({u},{v}) can be added to the tree!.\n"
                    self.add_text(output)
                    paths[u].append(v)
                    self.tree.add_edge(u,v)
                    self.display_graph(self.main_graph,self.canvas1)
                    print("5")
                    self.delay_graphic(self.tree,self.canvas2)
                    print("6")


            #self.delay_graphic(self.algo.copy_graph,self.canvas2)
            new_matched_edges=self.algo.grow_matched(self.leaves)
            print("new matched edges",new_matched_edges)
            print("55",unsat1)
            print("66",self.leaves)
            for u,v in new_matched_edges:
                print("edge88",u,v)
                if self.tree.has_node(u) and self.tree.has_node(v):
                    print("AUG PATH FOUND",u,v)   

                    augment_flag=True
                    break
                    self.tree.add_edge(u,v)
                    self.tree.toggle_matching(u,v)
                #self.tree.new_node(None,u,self.main_graph.nodes[u]['x'],self.main_graph.nodes[u]['y'])
                else:
                    self.tree.new_node(None,v,self.main_graph.nodes[v].get('x', 0),self.main_graph.nodes[v].get('y', 0))
                
                    self.tree.add_edge(u,v)
                    self.tree.toggle_matching(u,v)
                    self.delay_graphic(self.tree,self.canvas2)

            ##check if matched node forms aug path ie u and v are both in self.tree already
            self.delay_graphic(self.tree,self.canvas2)
        print("PATHS",paths)
        self.execute()
        return 0
    

    def load_graph(self, filename,):
        if filename:
            self.main_graph.load_from_file(filename)
            self.display_graph(self.main_graph,self.canvas1)
            print("#nodes:",self.main_graph.number_of_nodes())
            
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
    
    def button1(self,event):
        
        p=self.main_graph.proximal(event)
        
        #print("p=",p )
        if self.n==True:
            ##EDIT NODES
            if p==None:
                #ADD NODES
                self.main_graph.new_node(event)
                self.display_graph(self.main_graph,self.canvas1)
                
                
            elif isinstance(p,int):
                self.main_graph.delete_node(p)
                self.display_graph(self.main_graph,self.canvas1)

        elif self.e==True:
            if isinstance(p,int):
                self.draw_edge(event)
            elif isinstance(p,tuple):
                
                u,v=p
                #print("REMOVE EDGE",u,v)
                self.main_graph.remove_edge(u,v)
                self.display_graph(self.main_graph,self.canvas1)
                
        elif self.e==False and self.n==False and isinstance(p,tuple)==True and p!=None:   
            u,v=p
            #print("TOGGLE")
            self.main_graph.toggle_matching(u,v)
            self.display_graph(self.main_graph,self.canvas1)
            #self.main_graph.displayAdj(self.canvas1)
        return self  

    def draw_edge(self, event):
        p = self.main_graph.proximal(event)
        
        if isinstance(p,int):
            # Start edge at node p
            self.active_edge[0] = p
            # Binnd motion to the canvas to update the temporary edge
            self.canvas1.bind("<B1-Motion>",lambda event: self.temp_edge(event))
            self.canvas1.bind("<ButtonRelease-1>", lambda event: self.end_edge(event))  # Ensure end edge on release

    def temp_edge(self, event):
        if self.active_edge[0] != -1:
            # Clear any existing temporary edge
            self.canvas1.delete("temp_edge")
            # Get start node coordinates
            start_x, start_y = self.main_graph.nodes[self.active_edge[0]]['x'], self.main_graph.nodes[self.active_edge[0]]['y']
            # Draw a line from start node to current mouse position
            self.canvas1.create_line(start_x, start_y, event.x, event.y, fill="blue", tags="temp_edge")

    def end_edge(self, event):
        p = self.main_graph.proximal(event)
        if self.active_edge[0] != -1 and isinstance(p, int) and p != self.active_edge[0]:
            # Create a permanent edge if the release is on a different node
            self.main_graph.add_edge(self.active_edge[0], p)
            self.display_graph(self.main_graph,self.canvas1)
        # Clean up
        self.canvas1.delete("temp_edge")
        self.canvas1.unbind("<B1-Motion>")
        self.canvas1.unbind("<ButtonRelease-1>")
        self.active_edge = [-1, -1]  

    def display_graph(self,graph,canvas):
        node_radius = 20
        canvas.delete("all")  # Clear the canvas entirely to redraw.

        # Draw edges with colours based on their 'matched' attribute
        for u, v in graph.edges():
            if self.main_graph.has_node(u) and self.main_graph.has_node(v):  # Check if both nodes exist
                matched = graph[u][v].get('matched', False)
                line_colour = "red" if matched else "blue"
                x1, y1 = self.main_graph.nodes[u]['x'], self.main_graph.nodes[u]['y']
                x2, y2 = self.main_graph.nodes[v]['x'], self.main_graph.nodes[v]['y']
                canvas.create_line(x1, y1, x2, y2, fill=line_colour, width=2)

        # Draw nodes
        for node_id, attrs in graph.nodes(data=True):
            x, y = attrs.get('x', 0), attrs.get('y', 0) 
            print("NODE:",node_id,x,y)
            #print("1display!!",node_id,x,y)
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius,fill="white", outline="black")
            canvas.create_text(x, y, text=str(node_id))
        
        
    def save(self):
        filename = f"{self.input_entry.get()}.txt"
        try:
            with open(filename, 'w') as file:
                # Saving nodes with coordinates
                file.write("# Nodes\n")
                for node_id, attrs in self.main_graph.nodes(data=True):
                    x = attrs['x']
                    y = attrs['y']
                    file.write(f"{node_id},x={x},y={y}\n")
                    print(f"Node saved: {node_id},x={x},y={y}")

                # Saving edges with matching information
                file.write("# Edges\n")
                for u, v, attrs in self.main_graph.edges(data=True):
                    is_matched = 'True' if attrs.get('matched', False) else 'False'
                    file.write(f"{u},{v},{is_matched}\n")
                    print(f"Edge saved: {u}-{v}, Matched: {is_matched}")
            
            print(f"Graph saved as {filename}")
        except Exception as e:
            print(f"An error occurred while saving the graph: {e}")

    

    def run(self):
        self.root.mainloop()


    def delay_graphic(self,graph,canvas):
        self.continue_execution=False
        while not self.continue_execution:
            self.root2.update() 
        self.display_graph(graph,canvas)
        return 0
    
    
    def add_text(self,output):
    # Function to add text to the ScrolledText widget
        self.text.insert(tk.END, output)  # Insert at the end of the text widget
        self.line_number += 1  # Increment line number for the next output
        self.text.see(tk.END)
        self.text.update() 

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
        style.map("Custom.TButton", background=[("active", "darkblue")],foreground=[], padding=[], font=[])  # Keep the same background colour when pressed
        style.configure("Custom.TCombobox", padding=20, font=("Helvetica", 20),background="darkblue",foreground="white")
        

        style.map("Custom.TCombobox", background=[("active", "grey")])  # Change background colour when pressed

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
