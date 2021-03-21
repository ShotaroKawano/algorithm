// ================================================================================
// 吉島さんのやり方

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
    // [カウンターの数, 並ぶ人の人数]
    const [numOperator, numGuest] = lines[0].split(" ").map(Number)

    // 各カウンターの処理時間の配列 -> 昇順に並び替える
    // ("複数のカウンターが空いたとき、処理時間が少ない方のカウンターを使う"という条件の実装のため)
    const opeTimes = lines.slice(1).map(Number).sort((a, b) => { return (a < b ? -1 : 1) })

    // カウンター情報 { id: index#, opeTime: 処理時間, time: 現在の処理の終了時間(初期値 = 処理の所要時間) } をまとめた配列
    let operators = opeTimes.map((ele, index) => { return { id: index, opeTime: ele, time: ele } })

    // 並んでいる全ての人の処理が完了する時間を計算する
    const calcCompTime = (numOperator, numGuest, opeInfo) => {
      // 列に並んでいる人数
        let waitingGuest = numGuest - numOperator

        while (waitingGuest > 0) {
            // 「一番早く空くカウンターはどこか？」
            // 各カウンターの"現在の処理の終了時間"から一番早い(=値が小さい)ものを探す
            // [方法1]
            // let arry = opeInfo.map( ele => ele["time"] )
            // let min = Math.min(...arry) // Min.min() 最小値が複数ある場合はよりindex#の小さいものを返す
            // let id = arry.indexOf(min)
            // [方法2]
            let minId = opeInfo.reduce((acc, curr) => (acc.time <= curr.time) ? acc : curr).id

          // 「列に並んでいる先頭の人が開いたカウンターに並ぶ」
          // 見つけた一番早い"終了時間"にそのカウンターの"処理時間"を加算して、"終了時間"を更新する
          opeInfo[minId]["time"] += opeInfo[minId]["opeTime"]
          // 「先頭の人が進んだ分、待っている人数は一人少なくなる」
          waitingGuest--
      }
        // 「そして誰もいなくなった」
        // 各カウンターの保持している"終了時間"のうち、値が最大のものを返す
        return Math.max(...opeInfo.map(ele => ele["time"]))
    }

    const completeTime = calcCompTime(numOperator, numGuest, operators)
    console.log(completeTime);
});



// ================================================================================
// TDさんのやり方

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
    // chaserクラスを作ってそれらをcasherControllerクラスで操作する
    // タスクがあるかないか確認する
    // すべてのキャッシャーが作業中かどうか判断する
    // タスクがあるなら作業中でないキャッシャーにタスクを割り振る
    // すべてのキャッシャーのプロセス時間を更新する
    // タスクがすべて終わっている && キャッシャーがすべて停止している状態なら時間を出力する
    // そうでなければ以上をくり返す

    // casherクラス
    // 作業にかかる時間・現在のタスクにかかっている時間・作業中かどうかの状態を持つ
    // 現在のタスクにかかっている時間を更新する処理

    class Casher {
        constructor(props){
            this.processCompleteTime = props.processCompleteTime
            this.processingTime = 0
            this.inProcess = false
        }

        startProcess(){
            this.inProcess = true
        }

        finishProcess(){
            this.inProcess = false
        }

        get isInProcess(){
            return this.inProcess === true
        }

        get isSleeping(){
            return this.inProcess === false
        }

        update(){
            this.processingTime = (this.processingTime + 1) % this.processCompleteTime
            this.processingTime === 0 && this.finishProcess()
        }

    }

    // CasherController クラス
    // キャッシャーのインスタンス・タスク・現在の時間の状態を持つ
    // 時間を更新するメソッド キャッシャーを更新するメソッドを持つ
    class CahserController {
        constructor(props){
            this.cashers = props.cashers
            this.taskLength = props.taskLength
            this.time = 0
        }

        get hasTask(){
            return this.taskLength > 0
        }

        get hasntTask(){
            return this.taskLength === 0
        }

        get isEveryCasherSleeping(){
            return this.cashers.every(casher => casher.isSleeping)
        }

        get isAllComplete(){
            return this.hasntTask && this.isEveryCasherSleeping
        }

        setTask(){
            if(this.hasntTask) return
            this.cashers
                .filter(casher => casher.isSleeping)
                .forEach(casher => this.hasTask && (casher.startProcess(), this.taskLength--))
        }

        updateCashers(){
            this.cashers
                .filter(casher => casher.isInProcess)
                .forEach(casher => casher.update())
        }

        exec(){
            this.setTask()
            this.updateCashers()
            this.time++
            this.isAllComplete ? this.printResult() : this.exec()
        }

        printResult(){
            console.log(this.time)
        }
    }

    const [N, taskLength] = lines[0].split(' ').map(Number)
    const cashers = lines
        .slice(1)
        .sort((a, b) => a - b)
        .map(completeTime => new Casher({ processCompleteTime:  Number(completeTime) }))

    const casherController = new CahserController({
        cashers,
        taskLength
    })

    casherController.exec()

});
