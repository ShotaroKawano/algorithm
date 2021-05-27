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
  // 最頻値関数
  const modeVote = votes => {
    const counter = {};
    votes.forEach(el => {
      if (counter[el]) {
        counter[el]++;
      } else {
        counter[el] = 1;
      }
    });
    const max = Math.max(...Object.values(counter));
    const candidate = Object.keys(counter)
      .map(Number)
      .find(key => counter[key] === max);
    return candidate;
  };

  // 投票関数
  const vote = (voteOrders, candidates) => {
    return voteOrders.map(voteOrder =>
      voteOrder.find(order => candidates.includes(order)),
    );
  };

  // 候補者データ
  const numOfCandidates = Number(lines[0]);
  const CandidatesInput = lines.slice(1, numOfCandidates + 1);
  const RepublicanCandidates = CandidatesInput.map((party, idx) => {
    if (party === 'Republican') return idx + 1;
  }).filter(Boolean);
  const DemocraticCandidates = CandidatesInput.map((party, idx) => {
    if (party === 'Democratic') return idx + 1;
  }).filter(Boolean);
  // console.log(numOfCandidates);
  // console.log(CandidatesInput);
  // console.log(RepublicanCandidates);
  // console.log(DemocraticCandidates);

  // 投票者データ
  const numOfVoteOrder = Number(lines[numOfCandidates + 1]);
  const VoteOrdersInput = lines.slice(
    numOfCandidates + 2,
    numOfCandidates + 2 + numOfVoteOrder,
  );
  const voteOrders = VoteOrdersInput.map(voteOrder =>
    voteOrder.split(' ').map(Number),
  );
  // console.log(numOfVoteOrder);
  // console.log(VoteOrdersInput);
  // console.log(voteOrders);

  // 予備選挙
  const RepublicanVotes = vote(voteOrders, RepublicanCandidates);
  const RepublicanRepresentative = modeVote(RepublicanVotes);
  // console.log(RepublicanVotes);
  // console.log(RepublicanRepresentative);

  const DemocraticVotes = vote(voteOrders, DemocraticCandidates);
  const DemocraticRepresentative = modeVote(DemocraticVotes);
  // console.log(DemocraticVotes);
  // console.log(DemocraticRepresentative);

  // 本選挙
  const generalCandidates = [
    RepublicanRepresentative,
    DemocraticRepresentative,
  ];
  const generalVotes = vote(voteOrders, generalCandidates);
  const generalRepresentative = modeVote(generalVotes);
  // console.log(generalCandidates);
  // console.log(generalVotes);
  console.log(generalRepresentative);
});

// ================================================================================
// 工夫点
// forとletを使わず、mapとconstで書く
//
// 学んだこと
// for文でiやjをpushしているので、linesから受け取った値もNumberでキャストした方が良い
// objectのkeyにNumberを入れると文字列にキャストされる
// Math.maxは配列を展開して渡す Math.max(...array)
// TDさんのpaizaの画面でconsole.logの結果を見せながら説明するのわかりやすい

// ================================================================================
// forとletを使ってるバージョン
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
  // 最頻値関数
  const modeVote = votes => {
    let counter = {};
    votes.forEach(el => {
      if (counter[el]) {
        counter[el]++;
      } else {
        counter[el] = 1;
      }
    });
    let candidate = 0;
    let max = 0;
    for (const [key, value] of Object.entries(counter)) {
      if (value > max) {
        candidate = Number(key);
        max = value;
      }
    }
    return candidate;
  };

  // 投票関数
  const vote = (voteOrders, candidates) => {
    return voteOrders.map(voteOrder =>
      voteOrder.find(order => candidates.includes(order)),
    );
  };

  // 候補者データ
  let RepublicanCandidates = [];
  let DemocraticCandidates = [];
  const numOfCandidates = Number(lines[0]);
  for (let i = 1; i <= numOfCandidates; i++) {
    if (lines[i] === 'Republican') {
      RepublicanCandidates.push(i);
    } else {
      DemocraticCandidates.push(i);
    }
  }
  // console.log(numOfCandidates);
  // console.log(RepublicanCandidates);
  // console.log(DemocraticCandidates);

  // 投票者データ
  let voteOrders = [];
  const numOfVoteOrder = Number(lines[numOfCandidates + 1]);
  for (
    let j = numOfCandidates + 2;
    j <= numOfCandidates + 1 + numOfVoteOrder;
    j++
  ) {
    voteOrders.push(lines[j].split(' ').map(Number));
  }
  // console.log(numOfVoteOrder);
  // console.log(voteOrders);

  // 予備選挙
  const RepublicanVotes = vote(voteOrders, RepublicanCandidates);
  const RepublicanRepresentative = modeVote(RepublicanVotes);
  // console.log(RepublicanVotes);
  // console.log(RepublicanRepresentative);

  const DemocraticVotes = vote(voteOrders, DemocraticCandidates);
  const DemocraticRepresentative = modeVote(DemocraticVotes);
  // console.log(DemocraticVotes);
  // console.log(DemocraticRepresentative);

  // 本選挙
  const generalCandidates = [
    RepublicanRepresentative,
    DemocraticRepresentative,
  ];
  const generalVotes = vote(voteOrders, generalCandidates);
  const generalRepresentative = modeVote(generalVotes);
  // console.log(generalCandidates);
  // console.log(generalVotes);
  console.log(generalRepresentative);
});
