// こっちの方が余計な計算が少ない分早い
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
  const numOfSnacks = lines[0].split(' ')[0];
  const budget = lines[0].split(' ')[1];
  // console.log(numOfSnacks);
  // console.log(budget);

  // classよりsnacksToBringPriceListで管理したほうがスッキリしてた
  class SnacksToBring {
    constructor() {
      this.priceList = [];
    }

    get totalPrice() {
      return this.priceList.reduce((prev, current) => prev + current, 0);
    }

    get count() {
      return this.priceList.length;
    }
  }

  const allSnacksPriceList = [];
  for (let i = 0; i < numOfSnacks; i++) {
    allSnacksPriceList.push(Number(lines[i + 1]));
  }
  allSnacksPriceList.sort((a, b) => a - b);
  // テストデータ
  // const allSnacksPriceList = [270, 310];
  // console.log(allSnacksPriceList);

  const snacksToBring = new SnacksToBring();

  // 小さい方から詰めていく（この段階でおかしの種類数は確定）
  for (let i = 0; i < allSnacksPriceList.length; i++) {
    const currPrice = allSnacksPriceList[i];
    if (snacksToBring.totalPrice + currPrice <= budget) {
      snacksToBring.priceList.push(currPrice);
    } else {
      break;
    }
  }
  allSnacksPriceList.splice(0, snacksToBring.count);
  // console.log(snacksToBring);

  // // 小さい方から詰めていかないとおつりが最大にならないかも
  // // 500を埋めるのに470を１つより240を2つの方がおつりが少なくなる
  // // 逆に500を埋めるのに200を2つより450を1つの方がおつりが少なくなることもある
  // // と思ったけど、このパターンは種類数が減るからやらない
  // // 大きい方から詰めるとすべてのパターンを試せていない
  // allSnacksPriceList.sort((a, b) => b - a);
  // // console.log(allSnacksPriceList);

  // for (let i = 0; i < allSnacksPriceList.length; i++) {
  //     const currPrice = allSnacksPriceList[i];
  //     // console.log(currPrice);

  //     // 自分で定義したのに snacksToBring.length していて時間を食った
  //     // snacksToBring.count or snacksToBring.priceList
  //     for (let j = 0; j < snacksToBring.count; j++) {
  //         // console.log(snacksToBring.priceList[j]);
  //         if ((currPrice - snacksToBring.priceList[j]) + snacksToBring.totalPrice <= budget) {
  //             snacksToBring.priceList.splice(j, 1);
  //             snacksToBring.priceList.push(currPrice);
  //             break;
  //         }
  //     }
  // }

  // 小さい方から詰めていくパターン
  // snacksToBringを元にループするとすべてのパターンを試せる
  for (let i = 0; i < snacksToBring.count; i++) {
    const currPrice = snacksToBring.priceList[i];
    // console.log(currPrice);

    // 自分で定義したのに snacksToBring.length していて時間を食った
    // snacksToBring.count or snacksToBring.priceList.length
    for (let j = 0; j < allSnacksPriceList.length; j++) {
      if (
        allSnacksPriceList[j] - currPrice + snacksToBring.totalPrice <=
        budget
      ) {
        snacksToBring.priceList.splice(i, 1);
        snacksToBring.priceList.push(allSnacksPriceList[j]);
        // i--;で改めて最初からループされるので移動した要素は消しておく
        allSnacksPriceList.splice(j, 1);
        // [120, 130]→[130, 150]とループ中に配列の中身が変わるのがエラーの原因
        // indexが0→1のときに130をスキップしてしまうので、indexを一つ戻すのがミソ
        i--;
        break;
      }
    }
  }
  // console.log(snacksToBring);
  // console.log(allSnacksPriceList);
  console.log(budget - snacksToBring.totalPrice);
});

// ================================================================================
// 組み合わせ利用パターン
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
  // 合計
  const totalPrice = priceList => {
    return priceList.reduce((prev, current) => prev + current, 0);
  };

  // 組み合わせ
  const combination = (arr, num) => {
    let result = [];
    if (arr.length < num) {
      return [];
    }
    if (num === 1) {
      // 要素を一つずつ抽出して返す
      for (let i = 0; i < arr.length; i++) {
        result[i] = [Number(arr[i])];
      }
    } else {
      for (let i = 0; i < arr.length - num + 1; i++) {
        // [1, 2, 3]から2つ選ぶ場合
        // row = arrの前からi+1まで除外した配列のnum-1のcombinationを再帰的に生成
        // i = 0 のとき [2, 3]から1つ選ぶcombination
        // i = 1 のとき [3]から1つ選ぶcombination
        let row = combination(arr.slice(i + 1), num - 1);
        for (let j = 0; j < row.length; j++) {
          // i = 0 [1].concat([2]), [1].concat([3])
          // i = 1 [2].concat([3])
          // で [1, 2], [1, 3], [2, 3]
          result.push([Number(arr[i])].concat(row[j]));
        }
      }
    }
    return result;
  };

  // main
  const numOfSnacks = lines[0].split(' ')[0];
  const budget = lines[0].split(' ')[1];
  // console.log(numOfSnacks);
  // console.log(budget);

  const allSnacksPriceList = [];
  for (let i = 0; i < numOfSnacks; i++) {
    allSnacksPriceList.push(Number(lines[i + 1]));
  }
  allSnacksPriceList.sort((a, b) => a - b);
  // console.log(allSnacksPriceList);

  // 小さい順に予算の範囲内で詰める
  const snacksPriceList = [];
  for (let i = 0; i < allSnacksPriceList.length; i++) {
    const currPrice = allSnacksPriceList[i];
    if (totalPrice(snacksPriceList) + currPrice <= budget) {
      snacksPriceList.push(currPrice);
    } else {
      break;
    }
  }
  // console.log(snacksPriceList);
  // console.log(snacksPriceList.length);

  priceCombinations = combination(allSnacksPriceList, snacksPriceList.length);
  // console.log(priceCombinations); // [ [ 150, 120 ], [ 150, 130 ], [ 120, 130 ] ]

  const totalPriceList = priceCombinations
    .map((pc, _) => totalPrice(pc))
    .filter(tp => tp <= budget);
  // console.log(totalPriceList);

  // よく展開し忘れるが、maxは配列ではなく引数をたくさん受け取る
  const maxTotalPrice = Math.max(...totalPriceList);
  console.log(budget - maxTotalPrice);
});
