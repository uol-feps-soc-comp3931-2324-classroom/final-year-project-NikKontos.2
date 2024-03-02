<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Node and Edge Interaction</title>
  <script src="https://d3js.org/d3.v5.min.js"></script>
</head>
<body>

<script>
  // Initialize variables to keep track of nodes and edges
  let nodes = [];
  let edges = [];
  
  // Create an SVG container
  const svg = d3.select("body").append("svg")
    .attr("width", 500)
    .attr("height", 500);

  // Handle double-click to create nodes
  svg.on("dblclick", function() {
    const [x, y] = d3.mouse(this);

    // Create a circle (representing a node) at the clicked position
    const node = svg.append("circle")
      .attr("cx", x)
      .attr("cy", y)
      .attr("r", 15)
      .style("fill", "blue")
      .call(d3.drag().on("drag", dragNode));

    // Add the node to the list
    nodes.push({ id: nodes.length + 1, x, y, element: node });
  });

  // Function to handle dragging of nodes
  function dragNode(event, d) {
    d3.select(this)
      .attr("cx", d.x = event.x)
      .attr("cy", d.y = event.y);
    
    // Update edges when dragging a node
    updateEdges();
  }

  // Handle click-drag-release to create edges
  svg.on("mousedown", function() {
    const [x1, y1] = d3.mouse(this);

    // Create a line (representing an edge) starting from the clicked position
    const edgeLine = svg.append("line")
      .attr("x1", x1)
      .attr("y1", y1)
      .attr("x2", x1)
      .attr("y2", y1)
      .style("stroke", "red")
      .style("stroke-width", 2);

    // Function to handle dragging and releasing to complete the edge
    function dragEdge() {
      const [x2, y2] = d3.mouse(this);

      // Update the line's end position during the drag
      edgeLine.attr("x2", x2).attr("y2", y2);
    }

    // Function to handle releasing the mouse button to create the edge
    function releaseEdge() {
      const [x2, y2] = d3.mouse(this);

      // Find the nearest nodes to the starting and ending positions
      const startNode = findNearestNode(x1, y1);
      const endNode = findNearestNode(x2, y2);

      // Create an edge between the nearest nodes
      if (startNode && endNode) {
        edges.push({ source: startNode.id, target: endNode.id });
        updateEdges();
      }

      // Remove the temporary line
      edgeLine.remove();

      // Remove the drag and release event listeners
      svg.on("mousemove", null);
      svg.on("mouseup", null);
    }

    // Attach drag and release event listeners
    svg.on("mousemove", dragEdge);
    svg.on("mouseup", releaseEdge);
  });

  // Function to find the nearest node to a given position
  function findNearestNode(x, y) {
    let minDistance = Infinity;
    let nearestNode = null;

    nodes.forEach(node => {
      const distance = Math.sqrt((node.x - x) ** 2 + (node.y - y) ** 2);
      if (distance < minDistance) {
        minDistance = distance;
        nearestNode = node;
      }
    });

    return nearestNode;
  }

  // Function to update edges based on the current nodes
  function updateEdges() {
    svg.selectAll("line")
      .data(edges)
      .attr("x1", d => getNodeById(d.source).x)
      .attr("y1", d => getNodeById(d.source).y)
      .attr("x2", d => getNodeById(d.target).x)
      .attr("y2", d => getNodeById(d.target).y);
  }

  // Function to get a node by its ID
  function getNodeById(id) {
    return nodes.find(node => node.id === id);
  }
</script>

</body>
</html>
