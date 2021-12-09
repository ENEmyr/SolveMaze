function getArgs() {
  const args = {};
  process.argv
    .slice(2, process.argv.length)
    .forEach(arg => {
      // long arg
      if (arg.slice(0, 2) === '--') {
        const longArg = arg.split('=');
        const longArgFlag = longArg[0].slice(2, longArg[0].length);
        const longArgValue = longArg.length > 1 ? longArg[1] : true;
        args[longArgFlag] = longArgValue;
      }
      // flags
      else if (arg[0] === '-') {
        const flags = arg.slice(1, arg.length).split('');
        flags.forEach(flag => {
          args[flag] = true;
        });
      }
    });
  return args;
}

let endPoint = [];
let direction = 0;
let size = 13

function stringToMap(str) {
  let map = [];
  let row = [];
  for (var i = 0; i < str.length; i++) {
    if (str.charAt(i) == '\n') {
      map.push(row);
      row = [];
    } else {
      row.push(str.charAt(i));
    }
  }
  return map;
}

function getInitDir(map2D) {
  for (let i = 0; i < map2D.length; i++) {
    for (let j = 0; j < map2D[i].length; j++) {
      if (map2D[i][j] == 's') {
        if (i == 0) return 2;
        else if (i == map2D[i].length - 1) return 3;
        else if (j == 0) return 1;
        else return 0;
      }
    }
  }
}

function mapToString(map2D) {
  let str = '';
  for (let i = 0; i < map2D.length; i++) {
    for (let j = 0; j < map2D[i].length; j++) {
      str += map2D[i][j];
    }
    str += '\n';
  }
  return str;
}

function mapToTree(map2D, startPoint) {
  let point = startPoint;
  let queueOfPoint = [point];
  let path = [];
  for (let i = 0; i < size; i++) {
    path.push([]);
    for (let j = 0; j < size; j++) {
      path[i].push(null);
    }
  }
  while (queueOfPoint.length > 0) {
    point = queueOfPoint.shift();
    map2D[point[1]][point[0]] = '2';
    let around = [map2D[point[1] - 1][point[0]], map2D[point[1]][point[0] + 1], map2D[point[1] + 1][point[0]], map2D[point[1]][point[0] - 1]];
    for (let i = 0; i < around.length; i++) {
      if (around[i] == '0' || around[i] == 'f') {
        let pointTemp
        if (i == 0) {
          pointTemp = [point[0], point[1] - 1];
          path[point[0]][point[1] - 1] = point
        } else if (i == 1) {
          pointTemp = [point[0] + 1, point[1]];
          path[point[0] + 1][point[1]] = point
        } else if (i == 2) {
          pointTemp = [point[0], point[1] + 1];
          path[point[0]][point[1] + 1] = point
        } else if (i == 3) {
          pointTemp = [point[0] - 1, point[1]];
          path[point[0] - 1][point[1]] = point
        }
        if (around[i] == '0') queueOfPoint.push(pointTemp);
      }
      if (around[i] == 'f') {
        if (i == 0) {
          endPoint[0] = point[0];
          endPoint[1] = point[1] - 1;
        } else if (i == 1) {
          endPoint[0] = point[0] + 1;
          endPoint[1] = point[1];
        } else if (i == 2) {
          endPoint[0] = point[0];
          endPoint[1] = point[1] + 1;
        } else if (i == 3) {
          endPoint[0] = point[0] - 1;
          endPoint[1] = point[1];
        }
      }
    };
  }
  transpose = m => m[0].map((x, i) => m.map(x => x[i]))
  path = transpose(path)
  return path;
}

function getRoute(map2DArray, path, endPoint) {
  mapRouteNum = [];
  let pathList = [];
  for (let i = 0; i < size; i++) {
    mapRouteNum.push([]);
    for (let j = 0; j < size; j++) {
      mapRouteNum[i].push('  ')
    }
  }
  let point = [endPoint[0], endPoint[1]];
  let count = 0;
  while (true) {
    if (!point || !point[0] || !point[1] || map2DArray[point[1]][point[0]] == 's') {
      break;
    }
    pathList.push(point);
    mapRouteNum[point[1]][point[0]] = 'o ';
    count++;
    point = path[point[1]][point[0]];

  }
  pathList = pathList.reverse();
  return pathList;
}

function getCommands(pathList, map2D) {
  let commands = [];
  direction = getInitDir(map2D);
  let k = direction;
  for (let i = 1; i < pathList.length; i++) {
    xc = pathList[i - 1][0] - pathList[i][0];
    yc = pathList[i - 1][1] - pathList[i][1];
    if (yc == -1) {
      if (k != 0) {
        if (k == 3) commands.push('cw');
        else if (k == 1) commands.push('ccw');
        k = 0;
      }
    }
    if (yc == 1) {
      if (k != 2) {
        if (k == 1) commands.push('cw');
        else if (k == 3) commands.push('ccw');
        k = 2;
      }
    }
    if (xc == -1) {
      if (k != 3) {
        if (k == 2) commands.push('cw');
        else if (k == 0) commands.push('ccw');
        k = 3;
      }
    }
    if (xc == 1) {
      if (k != 1) {
        if (k == 0) commands.push('cw');
        else if (k == 2) commands.push('ccw');
        k = 1;
      }
    }
    commands.push('forward');
  }
  return commands;
}

const args = getArgs();
const maze = args['maze'] + '\n';
const entrance = (args['entrance'].split(',')).map(x => parseInt(x));
const maze2DArray = stringToMap(maze)
const path = mapToTree(maze2DArray, entrance);
const pathList = getRoute(maze2DArray, path, endPoint);
const commands = getCommands(pathList, maze2DArray);
console.log(commands.toString())
