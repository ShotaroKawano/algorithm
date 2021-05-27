
// #プール #オブジェクト指向

// ================================================================================
// 得票数を整数で割って、議席を割り振る



// ================================================================================
process.stdin.resume();
process.stdin.setEncoding('utf8');
// 自分の得意な言語で
// Let's チャレンジ！！
var lines = [];
var reader = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});
reader.on('line', (line) => {
  lines.push(line);
});
reader.on('close', () => {
    
    // 方針
    // 得票数÷整数のプールを作成 [2100, 1200, 600, 300]
    // プールでもっと大きな数値の党に議席を与え、その数を次の整数で割って再びプールする [1050, 1200, 600, 300]
    // (どの政党か、議席数、プール値、割る数の状態管理が必要)
    // (同じ場合は議席数が多い政党に議席を与える)
    // 議席数がなくなるまで繰り返す
  
    class Party {
        constructor(partyNo, numOfVotes) {
            this.PARTY_NO = partyNo
            this.numOfSeats = 0
            this.NUM_OF_VOTES = numOfVotes
            this.divisor = 1
        }

        get poolValue() {
            return this.NUM_OF_VOTES / this.divisor
        }
    }
    
    // main処理
    const [numOfParties, numOfTotalSeats] = lines[0].split(" ").map(Number);
    let currentNumOfTotalSeats = numOfTotalSeats;
    
    // partyプール
    const partyPool = [];
    for (let i = 0; i < numOfParties; i++) {
        // 0 行目は政党数と議席数   
        const party = new Party(i, lines[i + 1])
        partyPool.push(party)
    }
    
    while(currentNumOfTotalSeats > 0) {
        partyPool.sort((a, b) => {
            if (a.poolValue != b.poolValue) return b.poolValue - a.poolValue
            if (a.numOfSeats != b.numOfSeats) return b.numOfSeats - a.numOfSeats
            // コピペした後、poolValueのままだった たまたま全問正解したな
            // if (a.numOfSeats != b.numOfSeats) return b.poolValue - a.poolValue
            return 0
        })
        const theParty = partyPool[0]
        theParty.numOfSeats++
        theParty.divisor++
        currentNumOfTotalSeats--
    }
    
    // 元の順番に並び替える
    partyPool.sort((a, b) => a.PARTY_NO - b.PARTY_NO)
    for (let i = 0; i < numOfParties; i++) {
        console.log(partyPool[i].numOfSeats)
    }
    
});



// ================================================================================
// 学んだこと
// コピペすると書き換え間違えるので変数はコピペOKだが、ロジックはコピペしないようにしよう
// 最大でもトータルの議席数まででしか割ることはない
// オブジェクト思考で冗長に書くメリット
// - 行数は増えるがロジックが単純になり読みやすいコードになる
// - 自然言語的に記述できて、コメントを不要にできる
// sort 対 index はsortの方が楽だが、ドメイン駆動的には余計なid的なものは保持したくはない
// 定数は大文字で
// poolValueのような計算できる値はgetterで取得する