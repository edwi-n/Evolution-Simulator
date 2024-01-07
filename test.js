const canvas = document.getElementById("simulation-grid");
const ctx = canvas.getContext("2d");
const slider = document.getElementById("slider");

var scaleX = 0.8;
var scaleY = 0.8;
ctx.scale(scaleX, scaleY);
ctx.font = "9px FontAwesome";
ctx.strokeStyle = "black";

var data = JSON.parse("{{data | tojson | safe}}");
var iteration = 0;
var step = 1;
var iterationCount = data.iterationCount;
var populationSize = data.populationSize;
var uniqueId = data.id;
var simulationType = data.simulationType;
var paused = false;
data.organismsInIteration = [[]];
for (let i = 0; i < iterationCount; i++) {
  data.organismsInIteration.push([]);
}

if (simulationType == 1) {
  data.iterations = [[]];
  for (let i = 0; i < iterationCount; i++) {
    data.iterations.push([]);
  }
  document.getElementById("iterationPrev").style.display = "none";
  document.getElementById("iterationNext").style.display = "none";
}
var genomes = {};
var currGenome = 0;
var highlighted = {};
const locations = new Array(101).fill(-1).map(() => new Array(101).fill(-1));
// lower the simulation speed value, the faster the simulation
var simulationSpeed = 1;
ctx.fillStyle = "white";
ctx.fillRect(0, 0, 1000, 1000);

if (simulationType == 1) {
  chain = fetch("/get/" + uniqueId)
    .then((response) => {
      return response.json();
    })
    .then((dat) => {
      data.iterations[0] = data.movement.concat(dat.movement);
      data.organisms = data.organisms.concat(dat.organisms);
      return loop();
    });

  for (let i = 1; i < iterationCount; i++) {
    chain = chain
      .then((a) => {
        return fetch("/get/" + uniqueId);
      })
      .then((response) => {
        return response.json();
      })
      .then((dat) => {
        data.iterations[i] = dat.movement;
        data.organisms = data.organisms.concat(dat.organisms);
        return loop();
      });
  }
  chain.then(() => {
    document.getElementById("simulation-navigation").innerHTML = "";
  });
} else {
  oldSimLoop().then(() => {
    document.getElementById("simulation-navigation").innerHTML = "";
  });
}

slider.oninput = function () {
  simulationSpeed = 1 / (this.value / 50);
  document.getElementById("sliderValue").innerHTML = this.value / 50 + "x";
};

function getCursorPosition(canvas, event) {
  const rect = canvas.getBoundingClientRect();
  // add to rect.left and rect.top the values of padding left and padding top
  const x = Math.floor((event.clientX - rect.left) / (10 * scaleX));
  const y = Math.floor((event.clientY - rect.top) / (10 * scaleY));
  return [x, y];
}

function convertNumberToHex(number) {
  hex = number.toString(16);
  if (hex.length == 1) {
    return "0" + hex;
  } else {
    return hex;
  }
}

canvas.addEventListener("mousedown", function (e) {
  position = getCursorPosition(canvas, e);
  x = position[0];
  y = position[1];
  let organismId = -1;
  if (x >= 0 && y >= 0 && x <= 100 && y <= 100) {
    organismId = locations[x][y];
  }
  if (organismId != -1) {
    for (let id in highlighted) {
      if (id in prev) {
        var red = genomes[id][0] + genomes[id][1] + genomes[id][2];
        var green = genomes[id][3] + genomes[id][4] + genomes[id][5];
        var blue = genomes[id][6] + genomes[id][7];
        ctx.fillStyle = `rgb(
          ${Math.floor(255 - 60 * red)},
          ${Math.floor(255 - 60 * green)},
          ${Math.floor(255 - 100 * blue)}`;
        ctx.fillText(
          "\uf7fa",
          prev[id][0] * 10 + 1,
          (prev[id][1] + 1) * 10 - 2,
          8
        );
      }
    }
    highlighted = {};
    highlighted[organismId] = true;
    ctx.fillStyle = `rgb(
${0},
${0},
${0}`;
    ctx.fillText("\uf7fa", x * 10 + 1, (y + 1) * 10 - 2, 8);
    let organismParents = data.organisms[organismId][2];
    shortGenome = [];
    for (let i = 0; i < 8; i++) {
      shortGenome.push(genomes[organismId][i].toFixed(1));
    }
    var red =
      genomes[organismId][0] + genomes[organismId][1] + genomes[organismId][2];
    var green =
      genomes[organismId][3] + genomes[organismId][4] + genomes[organismId][5];
    var blue = genomes[organismId][6] + genomes[organismId][7];
    var rgb =
      convertNumberToHex(Math.floor(255 - 60 * red)) +
      convertNumberToHex(Math.floor(255 - 60 * green)) +
      convertNumberToHex(Math.floor(255 - 100 * blue));
    tree = makeTree(organismId);
    drawTree(tree);
    document.getElementById("organism-image").innerHTML =
      '<i id="icon" class="fa-solid fa-disease fa-spin fa-5x" style="color: #' +
      rgb +
      ';"></i>';
    document.getElementById("organism-id").innerHTML = "ID: " + organismId;
    document.getElementById("organism-genome").innerHTML =
      "Genome: " + shortGenome;

    if (organismParents[0] == -1 || organismParents[1] == -1) {
      document.getElementById("organism-parents").innerHTML = "Parents: N/A";
    } else {
      document.getElementById("organism-parents").innerHTML =
        "Parents: " + organismParents;
    }
  } else {
    document.getElementById("organism-id").innerHTML = "ID:";
    document.getElementById("organism-genome").innerHTML = "Genome:";
    document.getElementById("organism-parents").innerHTML = "Parents:";
    document.getElementById("organism-image").innerHTML = "";
    const organismTree = document.getElementById("organism-tree");
    const treeCtx = organismTree.getContext("2d");
    treeCtx.clearRect(0, 0, organismTree.width, organismTree.height);
  }
});

function resetLocations() {
  for (let i = 0; i < 101; i++) {
    for (let j = 0; j < 101; j++) {
      locations[i][j] = -1;
    }
  }
}

function checkEnd() {
  if (data.iterations[iteration].length != 0) {
    iteration += 1;
  }
  data.iterationCount = iteration;
  paused = true;
  var dataToSend = JSON.stringify(data);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/updateEntireData/" + uniqueId);
  xhr.setRequestHeader("Content-Type", "application/json");
  finalData = JSON.stringify(dataToSend);
  xhr.send(finalData);
  xhr.onreadystatechange = function () {
    window.location = "/end/" + uniqueId;
  };
}

function goBack() {
  if (simulationType == 1) {
    window.location = "/start";
  } else {
    window.location = "/open";
  }
}

async function loop() {
  resetLocations();
  prev = {};
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, 1000, 1000);
  while (currGenome < data.organisms.length) {
    genomes[data.organisms[currGenome][0]] = data.organisms[currGenome][1];
    currGenome += 1;
  }
  let totalSteps = data.iterations[iteration].length;
  for (step = 1; step < totalSteps; step++) {
    if (paused) {
      await new Promise((r) => setTimeout(r, 10));
      step--;
      continue;
    }
    if (
      step % Math.ceil(populationSize / simulationSpeed) == 0 ||
      step == totalSteps - 1
    ) {
      document.getElementById("progressBar").style.width =
        ((totalSteps * iteration + step) / (totalSteps * iterationCount)) *
          100 +
        "%";
      var image = new Image();
      image.id = "pic";
      image.src = canvas.toDataURL();
      image.height = 100;
      image.width = 100;
      document.getElementById("canvas-image").innerHTML = "";
      document.getElementById("canvas-image").appendChild(image);
      await new Promise((r) => setTimeout(r, 10));
    }
    ctx.fillStyle = "white";
    let organismId = data.iterations[iteration][step][0];
    let organismX = data.iterations[iteration][step][1][1];
    let organismY = data.iterations[iteration][step][1][0];
    let organismParents = data.organisms[organismId][2];
    if (organismId in prev) {
      ctx.fillRect(prev[organismId][0] * 10, prev[organismId][1] * 10, 10, 10);
      locations[prev[organismId][0]][prev[organismId][1]] = -1;
    } else {
      data.organismsInIteration[iteration].push(organismId);
    }
    var red =
      genomes[organismId][0] + genomes[organismId][1] + genomes[organismId][2];
    var green =
      genomes[organismId][3] + genomes[organismId][4] + genomes[organismId][5];
    var blue = genomes[organismId][6] + genomes[organismId][7];
    ctx.fillStyle = `rgb(
${Math.floor(255 - 60 * red)},
${Math.floor(255 - 60 * green)},
${Math.floor(255 - 100 * blue)}`;
    if (
      highlighted[organismParents[0]] ||
      highlighted[organismParents[1]] ||
      highlighted[organismId]
    ) {
      // ctx.strokeText("\uf7fa", organismX * 10 + 2, (organismY + 1) * 10 - 1, 5);
      // ctx.strokeText("\uf7fa", organismX * 10 + 1, (organismY + 1) * 10 - 2, 8);
      // ctx.strokeText("\uf7fa", organismX * 10 + 1, (organismY + 1) * 10 - 2, 7);
      ctx.fillStyle = `rgb(
${0},
${0},
${0}`;
      highlighted[organismId] = true;
    }
    ctx.fillText("\uf7fa", organismX * 10 + 1, (organismY + 1) * 10 - 2, 8);
    locations[organismX][organismY] = organismId;
    prev[organismId] = [organismX, organismY];
    document.getElementById("simulation-progress").innerHTML =
      iteration + 1 + " / " + data.iterationCount;
  }
  iteration += 1;
}

async function oldSimLoop() {
  while (iteration < iterationCount) {
    await loop();
  }
}

function iterationPrev() {
  if (simulationType != 1) {
    if (iteration > 0) {
      iteration -= 1;
      step = 1;
      prev = {};
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, 1000, 1000);
      document.getElementById("simulation-progress").innerHTML =
        iteration + 1 + " / " + data.iterationCount;
      document.getElementById("progressBar").style.width =
        ((data.iterations[iteration].length * iteration) /
          (data.iterations[iteration].length * iterationCount)) *
          100 +
        "%";
    }
  }
}

function iterationPause() {
  paused = !paused;
  if (paused) {
    document.getElementById("iterationPause").innerHTML =
      '<i id="iterationPauseState" value="a" class="fa fa-play"></i>';
  } else {
    document.getElementById("iterationPause").innerHTML =
      '<i id="iterationPauseState" value="a" class="fa fa-pause"></i>';
  }
}

function iterationNext() {
  if (simulationType != 1) {
    if (iteration < iterationCount - 1) {
      iteration += 1;
      step = 1;
      prev = {};
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, 1000, 1000);
      document.getElementById("simulation-progress").innerHTML =
        iteration + 1 + " / " + data.iterationCount;
      document.getElementById("progressBar").style.width =
        ((data.iterations[iteration].length * iteration) /
          (data.iterations[iteration].length * iterationCount)) *
          100 +
        "%";
    }
  }
}

var TreeNode = (function () {
  function TreeNode(data, left, right) {
    if (left == void 0) {
      left = null;
    }
    if (right == void 0) {
      right = null;
    }
    this.data = data;
    this.left = left;
    this.right = right;
  }
  return TreeNode;
})();

function makeTree(organismId, depth) {
  if (depth == void 0) {
    depth = 1;
  }
  let organismParents = data.organisms[organismId][2];
  if (organismParents[0] == -1 || organismParents[1] == -1 || depth == 5) {
    return new TreeNode(organismId);
  } else {
    return new TreeNode(
      organismId,
      new makeTree(organismParents[0], depth + 1),
      new makeTree(organismParents[1], depth + 1)
    );
  }
}

function treeHeight(root, depth) {
  if (depth == void 0) {
    depth = 0;
  }
  var left = root.left;
  var right = root.right;
  var depthLeft = depth;
  var depthRight = depth;
  if (left != null) {
    depthLeft = treeHeight(left, depth + 1);
  }
  if (right != null) {
    depthRight = treeHeight(right, depth + 1);
  }
  return Math.max(depthLeft, depthRight);
}

function drawLineLeftChild(ctx, x, y, quadrantWidth, levelHeight, font_size) {
  x += 10;
  ctx.beginPath();
  ctx.moveTo(x, y + 10);
  ctx.lineTo(x - quadrantWidth / 4, y + levelHeight / 2 - font_size);
  ctx.lineWidth = 2;
  ctx.stroke();
}
function drawLineRightChild(ctx, x, y, quadrantWidth, levelHeight, font_size) {
  x += 10;
  ctx.beginPath();
  ctx.moveTo(x, y + 10);
  ctx.lineTo(x + 1 + quadrantWidth / 4, y + levelHeight / 2 - font_size);
  ctx.lineWidth = 2;
  ctx.stroke();
}
function drawNode(node, xDepth, yDepth, treeHeight) {
  var font_size = 60 / (1.2 * (yDepth + 1));
  var canvas = document.getElementById("organism-tree");
  var ctx = canvas.getContext("2d");
  var width = canvas.getBoundingClientRect().width;
  var height = canvas.getBoundingClientRect().height;
  var quadrantWidth = width / Math.pow(2, yDepth);
  var levelHeight = 1;
  if (treeHeight > 0) {
    levelHeight = height / treeHeight;
  }
  var quadrantHeight = yDepth * levelHeight;
  var x = quadrantWidth * xDepth + quadrantWidth / 2;
  var y = quadrantHeight / 2 + font_size;
  ctx.font = font_size + "px serif";
  ctx.fillText(node.data, x, y);
  if (node.left) {
    drawLineLeftChild(ctx, x, y, quadrantWidth, levelHeight, font_size);
    drawNode(node.left, 2 * xDepth, yDepth + 1, treeHeight);
  }
  if (node.right) {
    font_size = 60 / (1.2 * (yDepth + 1));
    drawLineRightChild(ctx, x, y, quadrantWidth, levelHeight, font_size);
    drawNode(node.right, 2 * xDepth + 1, yDepth + 1, treeHeight);
  }
}

function drawTree(root) {
  var canvas = document.getElementById("organism-tree");
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  var height = treeHeight(root);
  drawNode(root, 0, 0, height);
}
