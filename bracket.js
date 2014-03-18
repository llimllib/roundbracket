// let's build a tournament tree
var round = 6;
var gid = 63;

var root = {
  gid: gid--,
  region: "south-east-west-midwest",
  round: round--,
  children: [],
};

var roundgames = {6: [root]};

function region(gid) {
  if ((gid >= 1 && gid <= 8) || (gid >= 33 && gid <= 36) ||
      (gid >= 49 && gid <= 50) || (gid == 57)) { return "south"; }
  if ((gid >= 9 && gid <= 16) || (gid >= 37 && gid <= 40) ||
      (gid >= 51 && gid <= 52) || (gid == 58)) { return "east"; }
  if ((gid >= 17 && gid <= 24) || (gid >= 41 && gid <= 44) ||
      (gid >= 53 && gid <= 54) || (gid == 59)) { return "west"; }
  if ((gid >= 25 && gid <= 32) || (gid >= 45 && gid <= 48) ||
      (gid >= 55 && gid <= 56) || (gid == 60)) { return "midwest"; }
  if (gid == 61) { return "south-east"; }
  if (gid == 62) { return "west-midwest"; }
  if (gid == 63) { return "south-east-west-midwest"; }

  // raise an error if we fall through
  throw new Error("undefined region for gid " + gid);
}

while (round > 0) {
  roundgames[round] = [];
  for (var i=0; i < roundgames[round+1].length; i++) {
    left = {
      gid: gid,
      region: region(gid),
      round: round,
      children: [],
    }
    gid--;

    right = {
      gid: gid,
      region: region(gid),
      round: round,
      children: [],
    }
    gid--;

    roundgames[round+1][i].children.push(left);
    roundgames[round+1][i].children.push(right);
    roundgames[round].push(left);
    roundgames[round].push(right);
  }
  round--;
}

var radius = 350, numRounds = 6, segmentWidth = radius / (numRounds + 1);

var partition = d3.layout.partition()
  .sort(null)
  .size([2 * Math.PI, radius]) // x maps to angle, y to radius
  .value(function(d) { return 1; }); //Important!

var arc = d3.svg.arc()
  .startAngle(function(d) { return d.x; })
  .endAngle(function(d) { return d.x + d.dx; })
  .innerRadius(function(d) { return d.y; })
  .outerRadius(function(d) { return d.y + d.dy; });

function trans(x, y) {
  return 'translate('+x+','+y+')';
}

var xCenter = radius, yCenter = radius;
var svg = d3.select('#bracket').append('svg').append('g').attr('transform', trans(xCenter,yCenter));

var chart = svg.append('g').attr("id", "chart");
chart.datum(root).selectAll('g')
  .data(partition.nodes)
  .enter()
  .append('g')
    .attr("class", "arc");

// Segments
d3.selectAll('.arc')
  .append('path')
  .attr('d', arc)
  .style("fill", "white")
  .style("stroke", "black");
  //.on('mouseover', playerHover);
