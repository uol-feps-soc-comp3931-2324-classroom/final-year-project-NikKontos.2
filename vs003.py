import tkinter as tk
import pyautogui
from tkinter import ttk
import os
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

class Graph:
    def __init__(self):
        self.nodes=[]
        self.edges=[]
        self.matchings=[]
    def printGraph(self):
        for nodes in self.graph.nodes:
            print("node",nodes.node_id)
        for edges in self.graph.edges:
            print("edge",edges.start_node.node_id,edges.end_node.node_id)
        for matches in self.graph.matchings:
            print("matching",matches.start_node.node_id,matches.end_node.node_id)

    def find_node_by_id(self, node_id):
        for node in self.graph.nodes:
            if node.node_id == node_id:
                return node
        return None
     
    def uploadGraph(file):
        graph= Graph()
        current_section = None
        obj_id = 0
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
                        obj_id, node_id, x, y = map(int, parts)
                        node = Node(obj_id, node_id, x, y)
                        graph.nodes.append(node)
                    elif current_section == "Edges":
                        parts = line.strip("()").split("),(")
                        count=0
                        for part in parts:
                            
                            obj_id, node_id = map(int, part.split(","))
                            
                            for node in graph.nodes:
                                if node_id==node.node_id and count==0:
                                    start_node=node
                                    count+=1
                                if node_id==node.node_id and count==1:
                                    end_node=node
                        edge = Edge(obj_id, start_node, end_node)
                        graph.edges.append(edge)
                    elif current_section == "Matchings":
                        count=0
                        for part in parts:
                            obj_id =part
                            for edge in graph.edges:
                                if obj_id==edge.obj_id and count==0:
                                    start_node=edge.start_node
                                    count+=1
                                if obj_id==edge.obj_id and count==1:
                                    end_node=edge.end_node


                        matching = Edge(obj_id, start_node, end_node)
                        graph.matchings.append(matching)
        return graph
    
    

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

        for node in self.graph.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                #print("Node clicked",node.node_id)
                return node  # Click within the radius of an existing node
        for edge in self.graph.edges:
            start_x, start_y = edge.start_node.x, edge.start_node.y
            end_x, end_y = edge.end_node.x, edge.end_node.y
            distance_to_edge = abs((end_y - start_y) * event.x - (end_x - start_x) * event.y + end_x * start_y - end_y * start_x) / ((end_y - start_y) ** 2 + (end_x - start_x) ** 2) ** 0.5

            if distance_to_edge <= 10:
                print("Edge clicked:", edge.start_node.node_id,edge.end_node.node_id,edge.start_node.x,edge.start_node.y,edge.end_node.x,edge.end_node.y)
                return edge  # Click within the radius of an existing edge
  # Click within the radius of an existing edges centre
        return False  # Click not within radius of any existing node





class Edmonds:  
    def __init__(self):
        self.maximum_matching = self.edmonds(self.graph)
    
    @staticmethod
    def unsatNode(graph):
        for node in graph.nodes:
            for edge in graph.matchings:
                if (node!=edge.start_node and node!=edge.end_node):
                    print(node.node_id,"unsatuared")
                
            



    
   
class Gui:
    def __init__(self,graph=Graph()):
        self.root = tk.Tk()
        self.root.title("Graph GUI")
        self.root.geometry("1000x700")
         
        # Create four canvases and place them in a grid
        
        
        
        
        
        
        
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
        #self.canvas.bind("<Double-Button-1>", self.dbl_clk)
        
        self.canvas.bind("<Button-2>", self.dbl_clk)
        self.canvas.bind("<Button-1>", self.b1_sngl_clk)
        self.canvas.bind("<Button-1>", self.b1_sngl_clk)
        self.canvas.bind("<B1-Motion>", self.draw_edge)
        self.canvas.bind("<ButtonRelease-1>", self.end_edge)
        if isinstance(graph,Graph):
            self.graph=graph
        else:
            print("AAAAAA",graph)
            self.graph=Graph.uploadGraph(graph)
            
            self.obj_id = self.graph.edges[-1].obj_id+1
            self.node_id_num=self.graph.nodes[-1].node_id+1
            print(self.obj_id,self.node_id_num)



    def append_matching(self,edge):
        for match in self.graph.matchings:
            if (edge.start_node.node_id == match.start_node.node_id or
                edge.start_node.node_id == match.end_node.node_id or
                edge.end_node.node_id == match.start_node.node_id or
                edge.end_node.node_id == match.end_node.node_id):                
                print("Invalid Match",edge.start_node.node_id,edge.end_node.node_id)
                return self
        self.graph.matchings.append(edge)
        self.displayGraph()
        return self
    
    def remove_matching(self,edge):
        for edges in self.graph.matchings:
            if edges.start_node.node_id==edge.start_node.node_id and edges.end_node.node_id==edge.end_node.node_id:
                print("REMOVE")
                self.graph.matchings.remove(edge)
                self.displayGraph()
        return self    
    def b1_sngl_clk(self,event):
        p=proximal(self,event)
        if isinstance(p,Node):
            self.start_edge(event)
            
        elif isinstance(p,Edge):
            for matching in self.graph.matchings:
                #print("aa",matching.start_node.node_id,matching.end_node.node_id)
                #print("bb",p.start_node.node_id,p.end_node.node_id)
                if (p.start_node.node_id,p.end_node.node_id) ==   (matching.start_node.node_id,matching.end_node.node_id):
                    print("remove match")
                    self.remove_matching(matching)
                    return self
                
            
            self.append_matching(p)
            return self
        
    
    
        
    
            
        
    def dbl_clk(self,event):
        if event.x<600 and event.y<500:
            self.addDelNode(event)
            
        else:
            print("cant add node outside of canvas1")

    def execute(self):
        for  i in range(0,len(self.graph.nodes)):
            print("Nodes",self.graph.nodes[i].node_id)
        for  i in range(0,len(self.graph.edges)):
            print("edges",self.graph.edges[i].start_node.node_id,self.graph.edges[i].end_node.node_id)
        for  i in range(0,len(self.graph.matchings)):
            print("matchings",self.graph.matchings[i].start_node.node_id,self.graph.matchings[i].end_node.node_id)
       
        self.maxGraph=Edmonds.unsatNode(self.graph)
        return self

    def getText(self):
        text=self.input_entry.get()
        return text
    def save(self):
        graph_data= self.graph
        text=self.getText()
        #text=self.input_entry.get()
        filename = f"graph_{text}_data.txt"
        with open(filename, 'w') as file:
        # Write nodes to the file
            file.write("Nodes:\n")
            for node in self.graph.nodes:
                file.write(f"{node.obj_id},{node.node_id},{node.x},{node.y}\n")

            # Write edges to the file
            file.write("\nEdges:\n")
            for edge in self.graph.edges:
                file.write(f"{edge.obj_id,edge.start_node.node_id},{edge.obj_id,edge.end_node.node_id}\n")
            
            # Write edges to the file
            file.write("\nMatchings:\n")
            for edge in self.graph.matchings:
                file.write(f"{edge.obj_id}\n")
            

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
        for node in self.graph.nodes:
            r = 20
            self.canvas.create_oval(node.x - r, node.y - r, node.x + r, node.y + r, fill="red")
            self.canvas.create_text(node.x, node.y,font=("Purisa",20), text=str(node.node_id))

        for edge in self.graph.edges:
            start_x, start_y = edge.start_node.x, edge.start_node.y
            
            end_x, end_y = edge.end_node.x, edge.end_node.y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="green", width=5)
        for edge in self.graph.matchings:
            start_x, start_y = edge.start_node.x, edge.start_node.y
            
            end_x, end_y = edge.end_node.x, edge.end_node.y
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=5)
        
       


    
    def addNode(self,event):
        x, y = event.x, event.y
        node_id = self.node_id_num
        self.node_id_num+=1
        n = Node(self.obj_id, node_id, x, y)
        self.obj_id += 1
        self.graph.nodes.append(n)
        # Draw a circle representing the node on the Tkinter canvas
        radius = 30
        # Save the last clicked node for adding edges
        self.last_clicked_node = node_id
        self.displayGraph()
        pyautogui.moveRel(1, 1)
        return self
    
    def removeNode(self,event,p):
        for node in self.graph.nodes:
            if p==node:
                self.graph.nodes.remove(node)

        for edge in self.graph.edges:
            self.graph.edges = [edge for edge in self.graph.edges if edge.start_node != p and edge.end_node != p]
        for matching in self.graph.matchings:
            self.graph.matchings=[matching for matching in self.graph.matchings if matching.start_node!=p and matching.end_node!=p]
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
            self.obj_id+=1

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
                self.graph.edges.append(self.current_edge)
        
        unique_edges = set()
        result = []

        for edge in self.graph.edges:
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



class HomeGui:
    def __init__(self):
        self.root1 = tk.Tk()
        self.root1.title("Home GUI")
        self.root1.geometry("500x500")
        self.canvas= tk.Canvas(self.root1,bg="lightgreen")

        self.input_graph = tk.Button(self.canvas, text="INPUT OWN GRAPH",command=self.inputTool) 
        self.input_graph.place(x=250,y=140,anchor="center")
        

        self.dropdown_var = tk.StringVar()
        self.dropdown_var.set("Select a file")

        self.dropdown = ttk.Combobox(self.canvas, textvariable=self.dropdown_var, state="readonly")
        self.dropdown.place(x=250,y=250,anchor="center")
        self.populate_dropdown()

        self.dropdown.bind("<<ComboboxSelected>>", self.update_selected_value)

        


        self.canvas.pack(fill=tk.BOTH, expand=True)

    def populate_dropdown(self):
        current_dir = os.getcwd()
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        self.dropdown["values"] = files

    def update_selected_value(self,event):
        # Update the selected value whenever the dropdown selection changes
        selected_value = self.dropdown_var.get()
        self.uploadTool(selected_value)

    def inputTool(self):
        # Create an instance of the GraphGUI class
        inputGraphGUI = Gui()

        # Run the Tkinter application
        inputGraphGUI.run()
    def uploadTool(self,file):
        # Create an instance of the GraphGUI class
        
        uploadGraphGUI = Gui(file)

        # Run the Tkinter application
        uploadGraphGUI.run()

    def run(self):
        self.root1.mainloop()

home_gui = HomeGui()
home_gui.run()


