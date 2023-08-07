//any global variables in python are accessible in JavaScript at PyScript.interpreter.globals.get('my_variable_name')
// TO DO: add texture to cells or image as background
var liveColor = "#212121";
var deadColor = "#fff";
var svg;
var grid;
var row;
var column;
var pointerposition; // track multitouch positions to update its position
var cellUpdates = new Set(); // avoid flickering when manually drawing cells on the grid
var e, x, y, id, cell, val;
var initSVG = () => {
    data = game_py.old_grid.toJs();
    grid = d3.select("#grid")
        .append("svg")
        .attr("class", "svg")
        .attr("width", game_py.width * game_py.cell_size)
        .attr("height", game_py.height * game_py.cell_size);
    rows = grid.selectAll("g")
        .data(data)
        .join("g")
        .attr("class", "row")
        .attr("transform", (d, i) => `translate(0, ${i * game_py.cell_size})`);

    cells = rows.selectAll("rect")
        .data((d, i) => d.map((val, j) => ({
            val,
            row: i,
            col: j
        }))) // Here we create an array of objects for each row
        .join("rect")
        .attr("class", "cell")
        .attr("fill", d => d.val === 0 ? deadColor : liveColor)
        .attr("width", game_py.cell_size - 0.2)
        .attr("height", game_py.cell_size - 0.2)
        .attr("state", d => d.val)
        .attr("y", 0)
        .attr("x", (d, j) => j * game_py.cell_size)
        .attr("id", d => `${d.row}-${d.col}`)
        .on('click', function(event, d) {
            if (pointerposition) return;
            const cell = d3.select(event.currentTarget);
            game_py.toggle_cell_state(d.row, d.col);
            cell
                .datum({
                    val: game_py.old_grid.toJs()[d.row][d.col],
                    row: d.row,
                    col: d.col
                })
                .style("fill", d => d.val === 0 ? deadColor : liveColor)
                .attr("state", d => d.val);
        })
        .on("pointerdown", function(event, d) {
            event.preventDefault();
            pointerposition = true // signal to mousemove to change cells
        })
        .on("pointermove", function(event, d) {
            if (!pointerposition) return; // mousemove with the mouse up
            e = event.currentTarget;
            id = e.getAttribute('id');
            if (!cellUpdates.has(id)) {
                cellUpdates.add(id);
                toggleCell(e);
            }
        })
        .on("pointerup", function(event) {
            pointerposition = null; // signals mouse up
        })

    updateGenPop()
}

function toggleCell(event) {
    [x, y] = event.getAttribute('id').split('-').map(i => parseInt(i))
    cell = d3.select(event)
    game_py.toggle_cell_state(x, y)
    val = game_py.old_grid.toJs()[x][y]
    cell.style("fill", val === 0 ? deadColor : liveColor)
    cell.attr("state", val)
}


var evolve = () => {
    var rows = d3.selectAll('.row')
    rows.data(game_py.old_grid.toJs())
    rows.selectAll('.cell')
        .data((d, i) => d.map((val, j) => ({
            val,
            row: i,
            col: j
        })))
        .transition()
        .duration(game_py.delay * 0.3)
        .style("fill", function(d) {
            return d.val == 0 ? deadColor : liveColor;
        })
        .attr("state", d => d.val)

}

var redraw = () => {
    updateGenPop()
    evolve()
}

d3.interval(() => {
    cellUpdates.clear();
}, 800);