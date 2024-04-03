# Import necessary libraries
import tkinter as tk
from tkinter import ttk, scrolledtext
import os
import networkx as nx
import time

class Node:
    def __init__(self,node_id,x,y):
        self.node_id=node_id
        self.x=x
        self.y=y

    def findCords(self,node_id):
        for node in self.graph.nodes():
            #print("NODEs:",node.node_id)
            if node.node_id==node_id:
                x,y=node.x,node.y
                return x,y
            else:
                #print("ERROR:NODE COORDS NOT FOUND")
                return None
class Edge:
    def __init__(self,edge_id,node1,node2):
        self.edge_id=edge_id
        self.node1=node1
        self.node2=node2

class InputGUI:
    def __init__(self):
        

        self.root = tk.Tk()
        self.root.title("INPUT Graph ")
        self.root.geometry("1000x600")

        self.canvas1= tk.Canvas(self.root,bg="green",height=2000,width=500)
        self.canvas1.pack(side=tk.LEFT)
        self.canvas2= tk.Canvas(self.root,bg="blue",height=2000,width=500)
        self.canvas2.pack(side=tk.RIGHT)     
        
        self.node_id=0
        self.edge_id=0
        self.graph=nx.Graph()

        self.last_click_time = 0  # Initialize variable to store last click time
        self.click_delay = 0.5  

        self.active_edge=None


        self.input_entry = tk.Entry(self.canvas1)
        self.input_entry.place(x=60,y=140,anchor="w")
        self.save_button = tk.Button(self.canvas1, text="Save", command=self.save) 
        self.save_button.place(x=90,y=140,anchor="e")
        

        self.canvas1.bind("<Double-Button-1>", self.dbl_clk_b1)
        #self.canvas1.bind("<Button-2>", self.dbl_clk)
        self.canvas1.bind("<Button-1>", self.sngl_clk_b1)
        #self.canvas1.bind("<Button-1>", self.b1_sngl_clk)
        #self.canvas1.bind("<B1-Motion>", self.draw_edge)
        #self.canvas1.bind("<ButtonRelease-1>", self.end_edge)
        


        
        self.root.mainloop()

    def delete_shapes_in_region(self,canvas, x1, y1, x2, y2):
        items_in_region = self.canvas1.find_overlapping(x1, y1, x2, y2)
        for item in items_in_region:
            self.canvas1.delete(item)

    def displayGraph(self):
        self.delete_shapes_in_region(self.canvas1,0,0,500,1000)
        graph=self.graph
      
        r=20
        for edge in graph.edges:
            self.canvas1.create_line(edge[0].x,edge[0].y,edge[1].x,edge[1].y,fill="red",width=10)
            print(edge[0].node_id,edge[1].node_id)
        for node in graph.nodes:
            self.canvas1.create_oval(node.x-r,node.y-r,node.x+r,node.y+r,fill="white")
            self.canvas1.tag_raise(self.canvas1.create_text(node.x, node.y,font=("Purisa",20), text=str(node.node_id)))
        
        return self
    def proximal(self,event):
        
        r = 30

        #if isinstance(object,Node)==True:
            #print("NODE")
        
        for node in self.graph.nodes:
            distance = ((event.x - node.x) ** 2 + (event.y - node.y) ** 2) ** 0.5
            if distance <= r:
                print("Node clicked",node.node_id)
                return node  # Click within the radius of an existing node
        print(self.graph.edges())
        for i in self.graph.edges:
            print("edges:",i[0].node_id,i[1].node_id)
            #if edge[0] is not None and edge[1] is not None:
                #if (Node.findCords(self,edge[0]) is not None) and (Node.findCords(self,edge[1]) is not None):
                    #start_x, start_y = Node.findCords(self,edge[0])
                    #end_x, end_y = Node.findCords(self,edge[1])
                    #distance_to_edge = abs((end_y - start_y) * event.x - (end_x - start_x) * event.y + end_x * start_y - end_y * start_x) / ((end_y - start_y) ** 2 + (end_x - start_x) ** 2) ** 0.5

                    #if distance_to_edge <= 10:
                        #print("Edge clicked:", edge.start_node.node_id,edge.end_node.node_id,edge.start_node.x,edge.start_node.y,edge.end_node.x,edge.end_node.y)
                        #return edge  # Click within the radius of an existing edge
    # Click within the radius of an existing edges centre
        return 0  # Click not within radius of any existing node

    def display_temp_edge(self, event):
        # Helper function to dynamically display the temporary edge
        self.canvas1.delete("temp_edge")
        if self.active_edge:
            start_x, start_y = self.active_edge.node1.x, self.active_edge.node1.y
            end_x, end_y = event.x, event.y  # Use cursor position as end point
            self.canvas1.create_line(start_x, start_y, end_x, end_y, fill="blue", tags="temp_edge")
            self.canvas1.bind("<ButtonRelease-1>", self.end_edge)

    def draw_edge(self, event):
        # Update the end point of the current edge while dragging
        if self.active_edge:
            self.active_edge.node2 = Node(-1, event.x, event.y)
            self.display_temp_edge(event)
            
    def sngl_clk_b1(self,event):
        # Create an active edge when a single click on a node occurs
        
        p = self.proximal(event)
        if isinstance(p, Node):
            self.active_edge = Edge( p, None,self.edge_id,)
            self.canvas1.bind("<B1-Motion>", self.draw_edge)  # Bind mouse motion to draw_edge method
            return self
        if isinstance(p,Edge):
            print(p.edge_id)
    def end_edge(self, event):
    # End drawing the edge and add it to the list of edges
        p = self.proximal(event)
        if self.active_edge and isinstance(p, Node) and self.active_edge.nodes[0]!=p:
            self.canvas1.delete("temp_edge")  # Remove the temporary edge
            self.active_edge.nodes[1] = p
            print("ADDING EDGE:",self.active_edge.nodes[0], self.active_edge.nodes[1], self.active_edge.edge_id)
            self.graph.add_edge(self.active_edge.nodes[0], self.active_edge.nodes[1], id=self.active_edge[2])
            self.edge_id += 1
        self.active_edge = None
        self.canvas1.unbind("<B1-Motion>")  # Unbind mouse motion after releasing the button
        self.displayGraph()
        return self

    def dbl_clk_b1(self,event):
        for i in self.graph.edges:
            print("edges:",i[0].node_id,i[1].node_id)
        current_time = time.time()
        if current_time - self.last_click_time < self.click_delay:
            return  # Ignore subsequent clicks within the delay period
        else:
            p = self.proximal(event)
            if p==0:
                self.last_click_time = current_time  # Update last click time
                node = Node(self.node_id, event.x, event.y)
                self.node_id += 1
                self.graph.add_node(node)
            elif isinstance(p,Node):
                self.graph.remove_node(p)
            self.displayGraph()

        self.last_click_time = 0
        return self
    
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
            for node in self.graph.nodes():
                file.write(f"{node.node_id},{node.x},{node.y}\n")

            # Write edges to the file
            file.write("\nEdges:\n")
            for i in self.graph.edges():
                print("saving edges",i[0].node_id,i[1].node_id)
                #file.write(f"{label},{s},{e}\n")
            
            # Write edges to the file
            file.write("\nMatchings:\n")
            #for edge in self.graph.matchings:
                #file.write(f"{edge.obj_id}\n")
            

        print(f"Graph data saved to {filename}")


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
        inputGraphGUI = InputGUI()

        # Run the Tkinter application
        inputGraphGUI.run()
    def uploadTool(self,file):
        # Create an instance of the GraphGUI class
        
        uploadGraphGUI = Edmonds(file)

        # Run the Tkinter application
        uploadGraphGUI.run()

    def run(self):
        self.root1.mainloop()

home_gui = HomeGui()
home_gui.run()