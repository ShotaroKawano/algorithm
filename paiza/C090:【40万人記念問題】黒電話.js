// #辞書 #文字列 #1文字ずつ #標準入力 #標準出力
// ================================================================================

process.stdin.resume();
process.stdin.setEncoding('utf8');

var lines = [];
var reader = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});
reader.on('line', (line) => {
  lines.push(line);
});
reader.on('close', () => {

  // 電話番号からハイフンを取り除く
  const numbers = lines[0].replace(/-/g, '')
  // 番号とフックまでの距離の辞書
  const dict_dist = {
      0: 12,
      1: 3,
      2: 4,
      3: 5,
      4: 6,
      5: 7,
      6: 8,
      7: 9,
      8: 10,
      9: 11
  }
  // 総距離
  let sum = 0

  Array.from(numbers).forEach(num => {
      // フックまでの距離の2倍(往復)を総距離に足していく
      sum += dict_dist[parseInt(num)] * 2;
  })
  console.log(sum)
});
