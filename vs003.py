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




class Screen:
    def __init__(self,screen_num,start_x,start_y,end_x,end_y):
        self.screen_num=screen_num
        self.start_x=start_x
        self.start_y=start_y
        self.end_x=end_x
        self.end_y=end_y

    def showScreens(self,screens):
        for screen in screens:
            self.canvas.create_rectangle(screen.start_x,screen.start_y,screen.end_x,screen.end_y,width=10)
            self.canvas.pack()
        return self

  
def proximal(self, event):
        r = 30

        #if isinstance(object,Node)==True:
            #print("NODE")

        for node in self.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                print("Node clicked",node.node_id)
                return node  # Click within the radius of an existing node
        for edge in self.edges:
            start_x, start_y = edge.start_node.x, edge.start_node.y
            end_x, end_y = edge.end_node.x, edge.end_node.y
            distance_to_edge = abs((end_y - start_y) * event.x - (end_x - start_x) * event.y + end_x * start_y - end_y * start_x) / ((end_y - start_y) ** 2 + (end_x - start_x) ** 2) ** 0.5

            if distance_to_edge <= r+20:
                #print("Edge clicked:", edge.start_node.node_id,edge.end_node.node_id)
                return edge  # Click within the radius of an existing edge
  # Click within the radius of an existing edges centre
        return False  # Click not within radius of any existing node





def edmonds():
    return 0
    
   
class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph GUI")
        self.root.geometry("1000x700")
         
        # Create four canvases and place them in a grid
    

    

        self.nodes = []
        self.edges = []
        self.matchings=[]
        self.obj_id = 0
        self.node_id_num=0
        self.current_edge = None

        
        self.canvas= tk.Canvas(self.root,bg="lightgreen")
        self.canvas.create_line(0,0,600,500,width=5,activefill="blue",fill="blue")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.screen1=Screen(1,0,0,600,500)
        self.screen2=Screen(2,600,0,1000,500)
        self.screen3=Screen(3,0,500,600,700)
        self.screen4=Screen(4,600,500,1000,700)
        screens=[self.screen1,self.screen2,self.screen3,self.screen4]
        Screen.showScreens(self,screens)


        self.input_entry = tk.Entry(self.canvas)
        self.input_entry.place(x=self.screen4.start_x+60,y=self.screen4.start_y+140,anchor="w")
        self.save_button = tk.Button(self.canvas, text="Save", command=self.save) 
        self.save_button.place(x=self.screen4.end_x-60,y=self.screen4.start_y+140,anchor="e")
        self.execute = tk.Button(self.canvas, text="Execute", command=self.execute) 
        self.execute.place(x=self.screen4.start_x +200,y=self.screen4.start_y+60,anchor="c")

        self.last_clicked_node = None
        self.current_edge = None  # Variable to track the current edge being drawn

        self.canvas.bind("<Double-Button-1>", self.dbl_clk)
        self.canvas.bind("<Button-2>", self.dbl_clk)
        self.canvas.bind("<Button-1>", self.b1_sngl_clk)
        self.canvas.bind("<Button-1>", self.b1_sngl_clk)
        self.canvas.bind("<B1-Motion>", self.draw_edge)
        self.canvas.bind("<ButtonRelease-1>", self.end_edge)
        
        
    def b1_sngl_clk(self,event):
        p=proximal(self,event)
        if isinstance(p,Node):
            
            self.start_edge(event)
            #print("EdgeStart:")
        elif isinstance(p,Edge):
            if p in self.matchings:
                self.remove_matching(p)
            else:
                self.valid_matching(p)
            #for i in range(len(self.matchings)):

                #print("matching",self.matchings[i].start_node.node_id,self.matchings[i].end_node.node_id)
        return 1
        
    
    def append_matching(self,edge):
        self.matchings.append(edge)
        return self
    def remove_matching(self,edge):
        self.matchings.remove(edge)
        return self
        
    def valid_matching(self,edge):
        for matching in self.matchings:

            
            if (matching.start_node==edge.start_node or matching.end_node==edge.end_node)or (matching.end_node==edge.start_node or matching.start_node==edge.end_node) :
                print("invalid matching")
                return 0
        self.append_matching(edge)
        return self
            
        
    def dbl_clk(self,event):
        if event.x<600 and event.y<500:
            self.addDelNode(event)
            
        else:
            print("cant add node outside of canvas1")

    def execute(self):
        for  i in range(0,len(self.nodes)):
            print("Nodes",self.nodes[i].node_id)
        for  i in range(0,len(self.edges)):
            print("edges",self.edges[i].start_node.node_id,self.edges[i].end_node.node_id)
        for  i in range(0,len(self.matchings)):
            print("matchings",self.matchings[i].start_node.node_id,self.matchings[i].end_node.node_id)
       

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


    def display_edge(self):
        # Helper function to dynamically display the edge
        self.canvas.delete("temp_edge")
        if self.current_edge:
            start_x, start_y = self.current_edge.start_node.x, self.current_edge.start_node.y
            end_x, end_y = self.current_edge.end_node.x, self.current_edge.end_node.y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", tags="temp_edge")


    def delete_shapes_in_region(self,canvas, x1, y1, x2, y2):
        items_in_region = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items_in_region:
            self.canvas.delete(item)

    def displayGraph(self):
        self.delete_shapes_in_region(self.canvas,self.screen1.start_x,self.screen1.start_y,self.screen1.end_x-10,self.screen1.end_y-10)
        for node in self.nodes:
            r = 20
            self.canvas.create_oval(node.x - r, node.y - r, node.x + r, node.y + r, fill="red")
            self.canvas.create_text(node.x, node.y,font=("Purisa",20), text=str(node.node_id))

        for edge in self.edges:
            start_x, start_y = edge.start_node.x, edge.start_node.y
            
            end_x, end_y = edge.end_node.x, edge.end_node.y
            if edge in self.matchings:
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="Red", width=5)
            else:
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)
        
       


    
    def addNode(self,event):
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
        return self,event.x+1,event.y+1
    
    def removeNode(self,event,p):
        for node in self.nodes:
            if p==node:
                self.nodes.remove(node)

        for edge in self.edges:
            self.edges = [edge for edge in self.edges if edge.start_node != p and edge.end_node != p]
        for matching in self.matchings:
            self.matchings=[matching for matching in self.matchings if matching.start_node!=p or matching.end_node!=p]
        self.displayGraph()
        return self


    def addDelNode(self,event):
        p=proximal(self,event)
        if p==False:
            self.addNode(event)
        else:
            self.removeNode(event,p)


    def start_edge(self, event):
        # Start drawing a new edge from an existing node
        p = proximal(self,event)
        if p is not False:
            self.current_edge = Edge(self.obj_id, p, p)

    def draw_edge(self, event):
        # Update the end point of the current edge while dragging
        if self.current_edge:
            self.current_edge.end_node = Node(self.obj_id, -1, event.x, event.y)
            self.display_edge()

    def end_edge(self, event):
        # End drawing the edge and add it to the list of edges
        p = proximal(self,event)

        
        if self.current_edge and p is not False:
            self.current_edge.end_node = p
            if self.current_edge.start_node.node_id!=p.node_id:
                self.edges.append(self.current_edge)
        
        unique_edges = set()
        result = []

        for edge in self.edges:
        # Sort the node IDs to make (0, 3) and (3, 0) equivalent
            sorted_nodes = tuple(sorted((edge.start_node.node_id, edge.end_node.node_id)))

            if sorted_nodes not in unique_edges:
                unique_edges.add(sorted_nodes)
                result.append(edge)

        
        self.current_edge = None
        self.displayGraph()
        return self


  

    def run(self):
        self.root.mainloop()

# Create an instance of the GraphGUI class
graph_gui = Gui()

# Run the Tkinter application
graph_gui.run()
