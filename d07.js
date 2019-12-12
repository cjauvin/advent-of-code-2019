// My puzzle input
const src = "3,8,1001,8,10,8,105,1,0,0,21,42,51,76,93,110,191,272,353,434,99999,3,9,1002,9,2,9,1001,9,3,9,1002,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,3,9,4,9,99,3,9,1002,9,4,9,101,5,9,9,1002,9,3,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,1002,9,5,9,101,3,9,9,102,5,9,9,4,9,99,3,9,1002,9,5,9,101,5,9,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99";

console.assert = function(cond, text) {
    if (cond) return;
    throw Error(text || "Assertion failed!");
};

function decodeInstruction(i) {
  let s = i + "";
  s = s.padStart(5, "0");
  return [parseInt(s.slice(-2)), parseInt(s[2]), parseInt(s[1]), parseInt(s[0])];
}

console.assert(JSON.stringify(decodeInstruction(1002)) === JSON.stringify([2, 0, 1, 0]));

function* execute(source) {
    let prog = source.split(',').map(s => parseInt(s));
    let i = 0;
    let opc, m1, m2, m3, p1, p2, p3, out;
    while (true) {
        [opc, m1, m2, m3] = decodeInstruction(prog[i]);

        if (opc === 1 || opc === 2) {
            console.assert(m3 === 0);
            p1 = m1 === 0 ? prog[prog[i + 1]] : prog[i + 1];
            p2 = m2 === 0 ? prog[prog[i + 2]] : prog[i + 2];
            prog[prog[i + 3]] = opc === 1 ? p1 + p2 : p1 * p2;
            i += 4;
        } else if (opc === 3) {
            console.assert(m1 === 0);
            prog[prog[i + 1]] = yield;
            i += 2;
        } else if (opc === 4) {
            out = m1 === 0 ? prog[prog[i + 1]] : prog[i + 1];
            yield out;
            i += 2;
        } else if (opc === 5 || opc === 6) {
            p1 = m1 === 0 ? prog[prog[i + 1]] : prog[i + 1];
            p2 = m2 === 0 ? prog[prog[i + 2]] : prog[i + 2];
            if (opc === 5 && p1 !== 0) {
                i = p2;
            }
            if (opc === 6 && p1 === 0) {
                i = p2;
            }
            if (i !== p2) {
                i += 3;
            }
        } else if (opc === 7 || opc === 8) {
            console.assert(m3 === 0);
            p1 = m1 === 0 ? prog[prog[i + 1]] : prog[i + 1];
            p2 = m2 === 0 ? prog[prog[i + 2]] : prog[i + 2];
            if (opc === 7) {
                prog[prog[i + 3]] = p1 < p2 ? 1 : 0;
            } else if (opc === 8) {
                prog[prog[i + 3]] = p1 === p2 ? 1 : 0;
            }
            i += 4;
        } else if (opc === 99) {
            return;
        } else {
            console.assert(false);
        }
        console.assert(i < prog.length);
    }
}

const permutations = function*(elements) {
  if (elements.length === 1) {
    yield elements;
  } else {
    let [first, ...rest] = elements;
    for (let perm of permutations(rest)) {
      for (let i = 0; i < elements.length; i++) {
        let start = perm.slice(0, i);
        let rest = perm.slice(i);
        yield [...start, first, ...rest];
      }
    }
  }
};

//const src = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"; // 43210
//const src = "3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0"; // 54321
//const src = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"; // 65210

let perms = permutations([0, 1, 2, 3, 4]);
let result = perms.next();
let maxSignal = Number.NEGATIVE_INFINITY;
while (!result.done) {
    let signal = 0;
    for (let phase of result.value) {
        let amp = execute(src);
        amp.next();
        amp.next(phase);
        signal = amp.next(signal).value;
    }
    maxSignal = signal > maxSignal ? signal : maxSignal;
    result = perms.next();
}

console.log('Part 1:', maxSignal);

//const src = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"; // 139629729
//const src = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"; // 18216

perms = permutations([5, 6, 7, 8, 9]);
result = perms.next();
maxSignal = Number.NEGATIVE_INFINITY;
while (!result.done) {
    let signal = 0;
    let amps = [];
    for (let phase of result.value) {
        let amp = execute(src);
        amps.push(amp);
        amp.next();
        amp.next(phase);
        signal = amp.next(signal).value;
    }

    let halted = false;
    while (!halted) {
        for (let amp of amps) {
            if (amp.next().done) {
                halted = true;
                break;
            }
            signal = amp.next(signal).value;
        }
        maxSignal = signal > maxSignal ? signal : maxSignal;
    }
    result = perms.next();
}

console.log('Part 2:', maxSignal);
