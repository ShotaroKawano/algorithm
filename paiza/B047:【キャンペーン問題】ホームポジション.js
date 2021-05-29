process.stdin.resume();
process.stdin.setEncoding('utf8');
// 自分の得意な言語で
// Let's チャレンジ！！
var lines = [];
var reader = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});
reader.on('line', line => {
  lines.push(line);
});
reader.on('close', () => {
  const string = lines[0];
  //   const string = 'tyghbn'

  // 行データ
  const row1 = 'qwertyuiop';
  const row2 = 'asdfghjkl';
  const row3 = 'zxcvbnm';

  // 判定関数群
  const getPosition = char => {
    const col1 = row1.indexOf(char);
    const col2 = row2.indexOf(char);
    const col3 = row3.indexOf(char);
    if (col1 > -1) return [1, col1 + 1];
    if (col2 > -1) return [2, col2 + 1];
    if (col3 > -1) return [3, col3 + 1];
  };

  const isSameHnad = (prev, curr) => {
    const [prevRow, prevCol] = getPosition(prev);
    const [currRow, currCol] = getPosition(curr);
    if (prevRow === currRow && Math.abs(prevCol - currCol) <= 1) return true;
    if (prevCol === currCol && Math.abs(prevRow - currRow) <= 1) return true;
    return false;
  };

  const expectedHand = char => {
    const [row, col] = getPosition(char);
    return col <= 5 ? 'left' : 'right';
  };

  const isWrongHand = (char, actual) => {
    const expected = expectedHand(char);
    if (expected !== actual) return true;
    return false;
  };

  // main処理
  let count = 0;
  let currHand = '';
  for (let i = 0; i < string.length; i++) {
    if (i === 0) {
      currHand = expectedHand(string[i]);
      // console.log(currHand);
      continue;
    }
    if (!isSameHnad(string[i - 1], string[i])) {
      // ここでleftとrightを入れ替える処理にしてて失敗した
      currHand = expectedHand(string[i]);
    }
    // console.log(currHand);
    if (isWrongHand(string[i], currHand)) count++;
  }

  console.log(count);
});

// ================================================================================
// 一行データバージョン
process.stdin.resume();
process.stdin.setEncoding('utf8');
// 自分の得意な言語で
// Let's チャレンジ！！
var lines = [];
var reader = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});
reader.on('line', line => {
  lines.push(line);
});
reader.on('close', () => {
  const string = lines[0];
  //   const string = 'tyghbn'

  // キーボード
  const keyboard = '|qwertyuiop|asdfghjkl*|zxcvbnm***|';

  // 判定関数群
  const isSameHnad = (prev, curr) => {
    const prevPosition = keyboard.indexOf(prev);
    const currPosition = keyboard.indexOf(curr);
    // 左右隣か同じキー
    if (Math.abs(prevPosition - currPosition) <= 1) return true;
    // 上下隣のキー
    if (Math.abs(prevPosition - currPosition) === 11) return true;
    return false;
  };

  const expectedHand = char => {
    const charPosition = keyboard.indexOf(char);
    const pipePosition = keyboard.slice(0, charPosition).lastIndexOf('|');
    return Math.abs(pipePosition - charPosition) <= 5 ? 'left' : 'right';
  };

  const isWrongHand = (char, actual) => {
    const expected = expectedHand(char);
    if (expected !== actual) return true;
    return false;
  };

  // main処理
  let count = 0;
  let currHand = '';
  for (let i = 0; i < string.length; i++) {
    if (i === 0) {
      currHand = expectedHand(string[i]);
      // console.log(currHand);
      continue;
    }
    if (!isSameHnad(string[i - 1], string[i])) {
      // ここでleftとrightを入れ替える処理にしてて失敗した
      currHand = expectedHand(string[i]);
    }
    // console.log(currHand);
    if (isWrongHand(string[i], currHand)) count++;
  }

  console.log(count);
});

// ================================================================================
// 学び
// - 如何に短く書くかみたいことやってみると使ったことないアルゴリズムや関数を知れて面白い
