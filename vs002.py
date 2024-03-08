import tkinter as tk

class Node:
    def __init__(self, obj_id, node_id, x, y):
        self.obj_id = obj_id
        self.node_id = node_id
        self.x = x
        self.y = y

class Edge:
    def __init__(self, obj_id, start_node, end_node):
        self.obj_id = obj_id
        self.start_node = start_node
        self.end_node = end_node




class GraphGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph GUI")

        # Create a Tkinter canvas
        self.canvas = tk.Canvas(self.root, width=1000, height=1000, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=2,columnspan=2, sticky="nsew")
         # Create three sections (top, middle, bottom)
        self.top_left = tk.Frame(self.root, bg="lightgray")
        self.top_left.grid(row=0, column=0, sticky="nsew")

        self.top_right = tk.Frame(self.root, bg="lightblue")
        self.top_right.grid(row=0, column=1, sticky="nsew")

        self.bottom_right = tk.Frame(self.root, bg="orange")
        self.bottom_right.grid(row=1, column=0, sticky="nsew")

        self.bottom_right = tk.Frame(self.root, bg="lightgreen")
        self.bottom_right.grid(row=1, column=1, sticky="nsew")

        # Configure row and column weights to allow resizing
        self.root.columnconfigure(0, weight=80)
        self.root.columnconfigure(1, weight=40)
        self.root.rowconfigure(0, weight=70)
        self.root.rowconfigure(1, weight=30)
        

        # Add content to frames (you can customize this part)
        tk.Label(self.top_left, text="Top left", bg="lightgray").pack(fill=tk.BOTH, expand=True)
        tk.Label(self.top_right, text="Middle Section", bg="lightblue").pack(fill=tk.BOTH, expand=True)
        tk.Label(self.bottom_right, text="Bottom Section", bg="lightgreen").pack(fill=tk.BOTH, expand=True)


        # Initialize variables to store nodes and edges
        self.nodes = []
        self.edges = []
        self.obj_id = 0
        self.node_id_num=0
        
        self.input_entry = tk.Entry(self.bottom_right)
        self.input_entry.pack()
        self.save_button = tk.Button(self.bottom_right, text="Save", command=self.save) 
        self.save_button.pack()
        self.execute = tk.Button(self.bottom_right, text="Execute", command=self.execute) 
        self.execute.pack()
        self.last_clicked_node = None
        self.current_edge = None  # Variable to track the current edge being drawn

        # Bind mouse events to functions
        self.top_left.bind("<Double-Button-1>", self.dbl_clk)
        self.top_left.bind("<Button-1>", self.start_edge)
        self.top_left.bind("<B1-Motion>", self.draw_edge)
        self.top_left.bind("<ButtonRelease-1>", self.end_edge)
        
    def execute(self):


        return self
    def getText(self):
        text=self.input_entry.get()
        return text
    def save(self):
        graph_data= [self.nodes,self.edges]
        text=self.getText()
        #text=self.input_entry.get()
        filename = f"graph_{text}_data.txt"
        with open(filename, 'w') as file:
        # Write nodes to the file
            file.write("Nodes:\n")
            for node in self.nodes:
                file.write(f"{node.node_id}: {node.x}, {node.y}\n")

            # Write edges to the file
            file.write("\nEdges:\n")
            for edge in self.edges:
                file.write(f"{edge.start_node.node_id} -> {edge.end_node.node_id}\n")

        print(f"Graph data saved to {filename}")


    def displayEdge(self,edge,event):
        self.displayGraph()
        start_x, start_y = self.current_edge.start_node.x, self.current_edge.start_node.y
        end_x, end_y = event.x, event.y
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue")
        

    def displayGraph(self):
        self.top_left.delete("all")
        for node in self.nodes:
            r = 30
            self.top_left.create_oval(node.x - r, node.y - r, node.x + r, node.y + r, fill="red")
            self.top_left.create_text(node.x, node.y,font=("Purisa",20), text=str(node.node_id))

        for edge in self.edges:
            start_x, start_y = edge.start_node.x, edge.start_node.y
            
            end_x, end_y = edge.end_node.x, edge.end_node.y

            self.top_left.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)

            print("1..",edge.start_node.node_id,edge.end_node.node_id)
        print("\n")
        self.top_left.pack()

    def proximal(self, event):
        r = 30
        for node in self.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                return node  # Click within the radius of an existing node
        return False  # Click not within radius of any existing node

    def add_node(self, event):
        # Add a node at the clicked position
        x, y = event.x, event.y
        node_id = self.node_id_num
        self.node_id_num+=1
        n = Node(self.obj_id, node_id, x, y)
        self.obj_id += 1
        self.nodes.append(n)
        # Draw a circle representing the node on the Tkinter canvas
        radius = 30
        # Save the last clicked node for adding edges
        self.last_clicked_node = node_id
        self.displayGraph()
        return self

    def remove_node(self, event, p):
        for node in self.nodes:
            if p.x == node.x and p.y == node.y:
                self.nodes.remove(node)
       
        self.edges = [edge for edge in self.edges if edge.start_node != p and edge.end_node != p]

        self.displayGraph()

    def start_edge(self, event):
        # Start drawing a new edge from the last clicked node
        p = self.proximal(event)
        if p != False:
            self.current_edge = Edge(self.obj_id, p, p)

    def draw_edge(self, event):
        # Update the end point of the current edge while dragging
        if self.current_edge:
            self.current_edge.end_node = Node(self.obj_id, -1, event.x, event.y)
            self.displayEdge(self.current_edge,event)
            # Dynamically display the edge while the cursor is moving
            

    def end_edge(self, event):
        # End drawing the edge and add it to the list of edges
        p = self.proximal(event)
        if isinstance(self.current_edge,type(None)):
            print("aaaa")
            return
        if self.current_edge.start_node==p:
            print(p.node_id)
            self.current_edge=None
        else:
            if self.current_edge and p:
                self.current_edge.end_node = p
                #print("3//",self.current_edge.start_node.node_id,self.current_edge.end_node.node_id)
                for edge in self.edges:
                    if ((self.current_edge!=None)and(edge.end_node!=None))and(self.current_edge.start_node.node_id==edge.start_node.node_id and self.current_edge.end_node.node_id== edge.end_node.node_id) or (self.current_edge.start_node.node_id==edge.end_node.node_id and self.current_edge.end_node.node_id== edge.start_node.node_id):
                        self.current_edge=None
                if self.current_edge!=None:
                    self.edges.append(self.current_edge)
                self.current_edge = None
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
