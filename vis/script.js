const svg = d3.select("#memoryVisualization");
const width = 900,
  height = 500;

const virtualX = 150,
  physicalX = 500,
  pageTableX = 320;
const blockHeight = 40,
  numBlocks = 6;

let processCount = 0;
const colors = d3.scaleOrdinal(d3.schemePastel2);

function drawMemoryLabels() {
  svg
    .append("text")
    .attr("x", virtualX)
    .attr("y", 40)
    .attr("class", "font-bold text-lg")
    .text("Virtual Memory");

  svg
    .append("text")
    .attr("x", physicalX)
    .attr("y", 40)
    .attr("class", "font-bold text-lg")
    .text("Physical Memory");

  svg
    .append("text")
    .attr("x", pageTableX)
    .attr("y", 40)
    .attr("class", "font-bold text-lg")
    .text("Page Table");

  svg
    .append("text")
    .attr("x", 720)
    .attr("y", 400)
    .attr("class", "font-bold text-lg")
    .text("Swap File");
}

function drawStaticMemory() {
  drawMemoryLabels();

  // Virtual Memory
  svg
    .selectAll(".virtualBlock")
    .data(d3.range(numBlocks))
    .enter()
    .append("rect")
    .attr("x", virtualX)
    .attr("y", (d) => 60 + d * blockHeight)
    .attr("width", 100)
    .attr("height", blockHeight)
    .attr("class", "memory-block virtual");

  // Physical Memory
  svg
    .selectAll(".physicalBlock")
    .data(d3.range(numBlocks))
    .enter()
    .append("rect")
    .attr("x", physicalX)
    .attr("y", (d) => 60 + d * blockHeight)
    .attr("width", 100)
    .attr("height", blockHeight)
    .attr("class", "memory-block physical");

  // Page Table
  svg
    .selectAll(".pageTable")
    .data(d3.range(numBlocks))
    .enter()
    .append("rect")
    .attr("x", pageTableX)
    .attr("y", (d) => 60 + d * blockHeight)
    .attr("width", 60)
    .attr("height", blockHeight)
    .attr("class", "memory-block page-table");

  // Swap Disk
  svg
    .append("ellipse")
    .attr("cx", 780)
    .attr("cy", 420)
    .attr("rx", 60)
    .attr("ry", 25)
    .attr("class", "memory-block swap");
}

drawStaticMemory();

document.getElementById("processForm").addEventListener("submit", (e) => {
  e.preventDefault();

  const name = document.getElementById("processName").value.trim();
  const priority = document.getElementById("priority").value;
  const critical = document.getElementById("critical").checked;

  if (!name) return;

  const color = colors(processCount);
  const process = { name, priority, critical, color };
  processCount++;

  addProcess(process);
  e.target.reset();
});

function addProcess(process) {
  const virtualIndex = Math.floor(Math.random() * numBlocks);
  const physicalIndex = Math.floor(Math.random() * numBlocks);

  const virtualY = 60 + virtualIndex * blockHeight + blockHeight / 2;
  const physicalY = 60 + physicalIndex * blockHeight + blockHeight / 2;

  const line = svg
    .append("line")
    .attr("x1", virtualX + 100)
    .attr("y1", virtualY)
    .attr("x2", pageTableX)
    .attr("y2", virtualY)
    .attr("stroke", process.color)
    .attr("stroke-width", 2)
    .attr("opacity", 0);

  const line2 = svg
    .append("line")
    .attr("x1", pageTableX + 60)
    .attr("y1", virtualY)
    .attr("x2", physicalX)
    .attr("y2", physicalY)
    .attr("stroke", process.color)
    .attr("stroke-width", 2)
    .attr("opacity", 0);

  svg
    .append("rect")
    .attr("x", virtualX)
    .attr("y", 60 + virtualIndex * blockHeight)
    .attr("width", 100)
    .attr("height", blockHeight)
    .attr("fill", process.color)
    .attr("class", `memory-block ${process.critical ? "critical" : ""}`)
    .attr("opacity", 0)
    .transition()
    .duration(800)
    .attr("opacity", 1);

  svg
    .append("rect")
    .attr("x", physicalX)
    .attr("y", 60 + physicalIndex * blockHeight)
    .attr("width", 100)
    .attr("height", blockHeight)
    .attr("fill", process.color)
    .attr("class", `memory-block ${process.critical ? "critical" : ""}`)
    .attr("opacity", 0)
    .transition()
    .delay(1000)
    .duration(800)
    .attr("opacity", 1);

  line.transition().duration(800).attr("opacity", 1);
  line2.transition().delay(1000).duration(800).attr("opacity", 1);

  // Tooltip
  svg
    .append("text")
    .attr("x", virtualX - 10)
    .attr("y", virtualY)
    .attr("text-anchor", "end")
    .attr("fill", process.color)
    .attr("font-size", "12px")
    .text(`${process.name} (${process.priority})`);
}
