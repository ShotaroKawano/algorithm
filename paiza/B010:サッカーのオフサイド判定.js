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
    
    const offence = lines[0].split(" ")[0];
    const passerNum = lines[0].split(" ")[1];
    const teamA = lines[1].split(" ").map((pos, index) => {
        return { number: (index + 1), position: Number(pos) };
    });
    const teamB = lines[2].split(" ").map((pos, index) => {
        return { number: (index + 1), position: Number(pos) };
    });
    
    const [offenceTeam, defenseTeam] = 
        offence == 'A' 
            ? [teamA, teamB]
            : [teamB, teamA];
    const passerPosition = offenceTeam[passerNum - 1].position;
    const sortedDefenseTeam = 
        offence == 'A'
            // 降順（110に近い方が先）
            ? teamB.sort((a, b) => a.position > b.position ? -1 : 1)
            // 昇順（0に近い方が先）
            : teamA.sort((a, b) => a.position > b.position ? 1 : -1);
    const offsideLine = sortedDefenseTeam[1].position;

//   次の4つの条件を満たした選手は、オフサイドと判定されます。 
//   (実際のサッカーではもう少しルールが複雑ですが、今回は以下の条件のみを考慮してください)
//   1. 味方チームの選手からのパスを受け取る。
//   2. パスを受け取る選手が敵チームの陣にいる。
//   3. 「パスを出した選手」よりも、敵チームのゴールラインの近くにいる。
// 　  　(パスを出した選手とx座標が同じなら、オフサイドにならない)
//   4. 「敵チームのゴールラインから2人目の敵チームの選手」よりも、敵チームのゴールラインの近くにいる。
// 　　  (2番目の選手とx座標が同じなら、オフサイドにならない)

    const judgeOffside = player => {
        if (offence == 'A') {
            if (player.position >= 55 
            && player.position > passerPosition 
            && player.position > offsideLine) {
                return true;
            } else {
                return false;
            }
        } else {
            if (player.position <= 55 
            && player.position < passerPosition 
            && player.position < offsideLine) {
                return true;
            } else {
                return false;
            }
        }
    };
    
    const offsidePlayers = offenceTeam.filter(judgeOffside);  
    if (offsidePlayers.length === 0) {
        console.log('None');
    } else {
        offsidePlayers.map(p => console.log(p.number));
    }

});



// ================================================================================
// 相対値パターン （0-110 → -55-55）自陣をマイナスと定義する
// ロジックが少し簡略になる

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
    
    const offence = lines[0].split(" ")[0];
    const passerNum = lines[0].split(" ")[1];
    const teamA = lines[1].split(" ").map((pos, index) => {
        return { number: (index + 1), position: (Number(pos) - 55) };
    });
    const teamB = lines[2].split(" ").map((pos, index) => {
        return { number: (index + 1), position: - (Number(pos) - 55) };
    });
    
    const [offenceTeam, defenseTeam] = 
        offence == 'A' 
            ? [teamA, teamB]
            : [teamB, teamA];
    const passerPosition = offenceTeam[passerNum - 1].position;
    const sortedDefenseTeam = defenseTeam.sort((a, b) => a.position > b.position ? 1 : -1);
    const offsideLine = - sortedDefenseTeam[1].position;

//   次の4つの条件を満たした選手は、オフサイドと判定されます。 
//   (実際のサッカーではもう少しルールが複雑ですが、今回は以下の条件のみを考慮してください)
//   1. 味方チームの選手からのパスを受け取る。
//   2. パスを受け取る選手が敵チームの陣にいる。
//   3. 「パスを出した選手」よりも、敵チームのゴールラインの近くにいる。
// 　  　(パスを出した選手とx座標が同じなら、オフサイドにならない)
//   4. 「敵チームのゴールラインから2人目の敵チームの選手」よりも、敵チームのゴールラインの近くにいる。
// 　　  (2番目の選手とx座標が同じなら、オフサイドにならない)

    const judgeOffside = player => {
        if (player.position >= 0 
        && player.position > passerPosition 
        && player.position > offsideLine) {
            return true;
        } else {
            return false;
        }
    };
    
    const offsidePlayers = offenceTeam.filter(judgeOffside);  
    if (offsidePlayers.length === 0) {
        console.log('None');
    } else {
        offsidePlayers.map(p => console.log(p.number));
    }

});



// ================================================================================
// 学んだこと
// return { number: (index + 1), position: Number(pos) }; の行、
//  Numberなくても入力例は動くが、テストケースは失敗する 文字列の比較で失敗している可能性あり
// getter setterの定義の仕方
// - https://jsprimer.net/basic/class/#class-accessor-property




