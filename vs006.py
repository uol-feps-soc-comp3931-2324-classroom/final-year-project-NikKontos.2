
import tkinter as tk
from tkinter import ttk,scrolledtext

import os
import math

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

class Graph:
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
        self.nodes.remove(node)
        return self
    
    def addEdge(self,edge):
        if edge.node1.node_id>edge.node2.node_id: #keeps edges in ascending order 
            edge=Edge(self.edge_id,edge.node2,edge.node1)
        for edges in self.edges:
            print("2:",edges.node1.node_id,edges.node2.node_id)
            if edge.node1==edges.node1 and edge.node2==edges.node2:
                    
                return print("EDGE EXISTS")
        self.edge_id+=1
        self.edges.append(edge)
        return self

    def removeEdge(self,edge):
        self.edges=[edges for edges in self.edges if edge!=edges]
        return self
    
    def addMatching(self,edge):
        
        for matching in self.matchings:
            if edge.node1==matching.node1 or edge.node1==matching.node2 or edge.node2==matching.node1 or edge.node2==matching.node2:
                return print("INVALID MATCHING")
        self.removeEdge(edge)
        match=Matching(edge.edge_id,edge.node1,edge.node2)
        self.matchings.append(match)
        return self
        
    def removeMatching(self,edge):
        self.matchings=[match for match in self.matchings if edge!=match]
        edge=Edge(edge.match_id,edge.node1,edge.node2)
        self.addEdge(edge)
        return self

class InputGUI:
    def __init__(self,file=None):
        
        self.root = tk.Tk()
        self.root.style = ttk.Style() # type: ignore
        self.root.style.theme_use('clam')  # type: ignore # Change the theme to 'clam' for a modern look
        self.root.style.configure("Custom.TButton", foreground="white", background=lightblue, padding=20, font=("Helvetica", 20)) # type: ignore
        self.root.title("INPUT Graph ")
        self.root.geometry("1000x600")

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
            self.graph = Graph()
            
            
        #else:
            #self.graph,self.node_id,self.edge_id = Graph.uploadGraph(file)
           # self.displayGraph()
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
        print("N-T",self.n_pressed)
        return self.n_pressed

    def nReleased(self, event):
        self.n_pressed = False
        print("N-F",self.n_pressed)
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
        print("end edge at node:",self.active_edge.node2.node_id)
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
            print("start edge at node:",p.node_id)
            
            self.active_edge.node1 = p
            self.canvas1.bind("<B1-Motion>",self.tempEdge)
        
            
            



    def editNodes(self,event):
        p = self.proximal(event)
        
        if p == 0:
            node = Node(self.graph.node_id, event.x, event.y)
            self.graph.node_id += 1
            self.graph.addNode(node)
        elif isinstance(p, Node):
            print(p.node_id)
            self.graph.removeNode(p)
        self.displayGraph()

        
    def delete_shapes_in_region(self, canvas, x1, y1, x2, y2):
        items_in_region = self.canvas1.find_overlapping(x1, y1, x2, y2)
        for item in items_in_region:
            self.canvas1.delete(item)

    def displayGraph(self):
        self.delete_shapes_in_region(self.canvas1, 0, 0, 500, 1000)
        
        
        for edge in self.graph.edges:
            self.canvas1.create_line(edge.node1.x,edge.node1.y,edge.node2.x,edge.node2.y,fill="blue",width=10)
            print("EDGE: ",edge.edge_id,edge.node1.node_id,edge.node2.node_id)
        for matching in self.graph.matchings:
            self.canvas1.create_line(matching.node1.x,matching.node1.y,matching.node2.x,matching.node2.y,fill="red",width=10)
        
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
                print("MATCHING clicked:", match.node1.node_id,match.node2.node_id)
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
                print("Edge clicked:", edge.node1.node_id,edge.node2.node_id)
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

    


    def run(self):
        self.root.mainloop()


class HomeGui:
    def __init__(self):
        self.root1 = tk.Tk()
        
        self.root1.title("Home GUI")
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
