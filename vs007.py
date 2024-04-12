
import tkinter as tk
from tkinter import ttk,scrolledtext

from collections import deque
import os
import math
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
    def __init__(self,match_id,node1,node2):
        self.match_id=match_id
        self.node1=node1
        self.node2=node2

class tkinterUserGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.matchings = []
        self.node_id = 0
        self.edge_id = 0
    
    def find_node(self,node_id):
        for node in self.nodes:
            if node.node_id==node_id:
                return node
      
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

        for matching in self.matchings:
            if edge.node1==matching.node1 or edge.node1==matching.node2 or edge.node2==matching.node1 or edge.node2==matching.node2:
                return print("INVALID MATCHING")
        self.removeEdge(edge)
        match=Matching(edge.edge_id,edge.node1,edge.node2)
        self.matchings.append(match)
        #for match in self.matchings:
        #   print("MATCHINGS",match.node1.node_id,match.node2.node_id)
        
        return self
        
    def removeMatching(self,edge):
        self.matchings=[match for match in self.matchings if edge.match_id!=match.match_id]
        edge=Edge(edge.match_id,edge.node1,edge.node2)
        self.addEdge(edge)
        return self
    
    @staticmethod
    def uploadGraph(file):
        graph = tkinterUserGraph()
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
        self.root.style.configure("Custom.TButton", foreground="white", background="lightblue", padding=20, font=("Helvetica", 20)) # type: ignore
        self.root.title("INPUT Graph ")
        self.x_size=500
        self.y_size=700
        self.root.geometry("{}x{}".format(self.x_size, self.y_size))
        self.root.geometry("+10+10")
        self.canvas1 = tk.Canvas(self.root, bg="lightblue", height=2000, width=500)
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
            self.graph = tkinterUserGraph()
            
            
        else:
            self.graph,max_node,max_edge = tkinterUserGraph.uploadGraph(file)
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
        p=self.proximal(event)
        if self.n_pressed==True:
            self.editNodes(event)
        elif self.e_pressed==True:
            if isinstance(p,Node):
                self.drawEdge(event)
                
            elif isinstance(p,Edge) or isinstance(p,Matching):
                self.removeEdge(p)
                
        elif self.n_pressed==False and self.e_pressed==False and (isinstance(p,Edge) or isinstance(p,Matching)):
            self.changeMatching(event)

    def removeEdge(self,e):
        
        if (isinstance(e,Edge)==True):
            self.graph.edges=[edge for edge in self.graph.edges if edge.edge_id !=e.edge_id]

        if (isinstance(e,Matching)==True):
            self.graph.matchings=[match for match in self.graph.matchings if match.match_id !=e.match_id]

            
        self.displayGraph()

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
            #print("EDGE: ",edge.edge_id,edge.node1.node_id,edge.node2.node_id)
        for matching in self.graph.matchings:
            self.canvas1.tag_raise(self.canvas1.create_line(matching.node1.x,matching.node1.y,matching.node2.x,matching.node2.y,fill="red",width=10))
            #print("MATCH: ",matching.match_id,matching.node1.node_id,matching.node2.node_id)

        for node in self.graph.nodes:
            self.canvas1.create_oval(node.x - self.node_radius, node.y - self.node_radius, node.x + self.node_radius, node.y + self.node_radius, fill="white")
            self.canvas1.tag_raise(self.canvas1.create_text(node.x, node.y, font=("Purisa", 20), text=str(node.node_id)))
            #print("NODE: ",node.node_id,node.x,node.y)
    

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
                match=Matching(match.match_id,match.node1,match.node2)
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
        adj_graph = AdjListGraph()

        adj_graph.convert_tkinter2adj(graph_copy)
        adj_graph.print_adj_list()
        ed = EdmondsMethods(adj_graph)

        print("NEW TKINTER")
        g=adj_graph.convert_adj2tkinter(graph_copy)
        self.graph=g
        self.displayGraph()

###
## For Algorithm



class AdjListGraph:

    def __init__(self):
        # Initialize an empty dictionary for the adjacency list
        self.nodes = set()
        self.adj_list = {}
        
    def convert_tkinter2adj(self,graph):
        for node in graph.nodes:
            self.add_node(node.node_id)
        for edges in graph.edges:
            self.add_edge(edges.node1.node_id,edges.node2.node_id,matched=False)
        for matching in graph.matchings:
            self.add_edge(matching.node1.node_id,matching.node2.node_id,matched=True)
        self.sort_adj_list()

    def convert_adj2tkinter(self,tkinterGraph):
        g = tkinterUserGraph()
        max_edge_id=0
        max_match_id=0

        for node in self.nodes:
            n=tkinterGraph.find_node(node)
            print("node:",node,"coords",n.x,n.y)
            g.addNode(Node(node,n.x,n.y))
            for neighbour,n in self.get_neighbors(node):
                if n ==False:
                    print("EDGE:",node,neighbour,n)
                    edge1 = Edge(max_edge_id,tkinterGraph.find_node(node),tkinterGraph.find_node(neighbour))
                    max_edge_id+=1
                    g.addEdge(edge1)
                elif n==True:
                    print("MATCHING:",node,neighbour,n)
                    match1 = Matching(max_match_id,tkinterGraph.find_node(node),tkinterGraph.find_node(neighbour))
                    max_match_id+=1
                    g.addMatching(match1)
        return g

                
                


        
    def add_node(self, node):
        # Initialize the adjacency list for the node with an empty dictionary
        if node not in self.adj_list:
            self.adj_list[node] = {}
            self.nodes.add(node)
            self.sort_adj_list()

    def add_edge(self, node1, node2, matched=False):
        # Add an edge by setting node2 in node1's list and vice versa
        # The value is True if the edge is matched, False otherwise
        if node1 in self.adj_list and node2 in self.adj_list:
            self.adj_list[node1][node2] = matched
            self.adj_list[node2][node1] = matched
            self.sort_adj_list()
        else:
            print("One or both nodes do not exist.")

    
    def add_matching(self, node1, node2):
        # Check if both nodes exist
        if node1 not in self.adj_list or node2 not in self.adj_list:
            print("One or both nodes do not exist.")
            return
    
        # Check if the edge exists
        if node2 not in self.adj_list[node1]:
            print("The edge does not exist.")
            return

        # Check if either node is already involved in a matching
        for neighbor, matched in self.get_neighbors(node1):
            if matched:
                print(f"Node {node1} is already matched.")
                return
        for neighbor, matched in self.get_neighbors(node2):
            if matched:
                print(f"Node {node2} is already matched.")
                return

        # If all checks pass, set the edge as matched
        self.adj_list[node1][node2] = True
        self.adj_list[node2][node1] = True
        print(f"Matching between Node {node1} and Node {node2} added.")
        self.sort_adj_list()

    
    def remove_matching(self, node1, node2):
        # Set an existing edge as matched
        if node1 in self.adj_list and node2 in self.adj_list[node1] and self.adj_list[node1][node2] == True:
            self.adj_list[node1][node2] = False
            self.adj_list[node2][node1] = False
            self.sort_adj_list()
        else:
            print("CANT TURN NONMATCH  TO NONMATCH")
    
    def get_neighbors(self, node):
        # Return a list of tuples for each neighbor and whether the edge is matched
        return [(neighbor, self.adj_list[node][neighbor]) for neighbor in self.adj_list[node]]


    def print_adj_list(self):
        for node in self.nodes:
            print(node,"->",self.adj_list[node])

    def sort_adj_list(self):
        # Sort the adjacency list for each node
        for node in self.adj_list:
            # Sorting the dictionary by keys (node IDs) and updating the dictionary
            self.adj_list[node] = {k: self.adj_list[node][k] for k in sorted(self.adj_list[node])}

class AlternatingForest:
    def __init__(self):
        self.roots = {}  # Store roots with their corresponding tree. Key: root node, Value: Tree
        self.parent = {}  # Parent pointers to reconstruct paths. Key: node, Value: parent node
        self.matched = {}  # Edge matching status from node to parent. Key: node, Value: Boolean indicating if edge to parent is matched

    def add_root(self, root):
        if root not in self.roots:
            self.roots[root] = None  # Initialize with None, can later link to a specific tree node if needed
            self.parent[root] = None  # Root has no parent
            self.matched[root] = False  # Root edge status is unmatched (since it's a root)

    def add_edge(self, from_node, to_node, is_matched):
        # This method assumes the from_node is already in the forest
        self.parent[to_node] = from_node
        self.matched[to_node] = is_matched

    def find_augmenting_path(self,adjGraph):
        for root in self.roots:
            visited = set()  # Keep track of visited nodes to prevent cycles
            queue = [(root, [root])]  # Initialize queue with root and path

            while queue:
                current_node, path = queue.pop(0)
                if current_node in visited:
                    continue
                visited.add(current_node)

                if current_node != root and current_node not in self.roots:
                    # Found an augmenting path
                    return path

                for neighbor, is_matched in adjGraph.get_neighbors(current_node):
                    # Ensure we're alternating between matched and unmatched edges
                    if is_matched != self.matched.get(current_node, not is_matched):
                        next_path = path + [neighbor]
                        queue.append((neighbor, next_path))

        # If no augmenting path is found
        return None

    def is_in_forest(self, node):
        return node in self.parent

    def path_to_root(self, node):
        # Reconstruct the path from a node to its root in the forest
        path = []
        while node is not None:
            path.append(node)
            node = self.parent[node]
        path.reverse()  # Reverse to get the path from root to the node
        return path

    def print_forest(self):
        # Utility method to print the forest structure
        for root in self.roots:
            print(f"Root: {root}, Path: {self.path_to_root(root)}")

class EdmondsMethods:
    def __init__(self,adj_graph):
        self.adjGraph = adj_graph
        self.forest = AlternatingForest()
        self.marked_vertices = set()
        self.marked_edges = set()
        
    def unsat_nodes(self):
        unsatNodes = []
        # Iterate through each node
        for node in self.adjGraph.nodes:
            # Assume node is unsaturated initially
            unsaturated = True
            # Check if any edge for the node is matched
            for neighbor, matched in self.adjGraph.get_neighbors(node):
                if matched:  # If at least one edge is matched, the node is saturated
                    unsaturated = False
                    break  # No need to check further edges
            if unsaturated:
                unsatNodes.append(node)
        for unsat in unsatNodes:
            self.forest.add_root(unsat)
        return self.forest
    
    def grow_forest(self):
    # Initialize the forest with unsaturated nodes as roots
        self.forest = self.unsat_nodes()
        queue = deque()  # Using deque for efficient pops from the left

    # Start with all roots in the queue
        for root in self.forest.roots:
            queue.append((root, None))  # Append root and parent (None for roots)
            print("ROOTS:", root)

    # Process nodes in the queue
        while queue:
            current_node, parent = queue.popleft()  # Use popleft for BFS
            print("QUEUE:", queue)

        # Iterate over all neighbors of the current node
            for neighbor, is_matched in self.adjGraph.get_neighbors(current_node):
                # Check if the neighbor is not already in the forest
                if not self.forest.is_in_forest(neighbor):
                    # Add the neighbor and the edge to the forest
                    self.forest.add_edge(current_node, neighbor, is_matched)
                    print("add edge", current_node, neighbor)
                    # If the edge is unmatched, it's a potential path for growth
                    if not is_matched:
                        queue.append((neighbor, current_node))
                else:
                    # Handle cases where both nodes are already in the forest
                    # This might be where you handle blossoms or augmenting paths detection
                    print("AUG edge", current_node, neighbor)
                    self.adjGraph.add_matching(current_node,neighbor)
        self.adjGraph.print_adj_list()
        self.forest.print_forest()
            

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
