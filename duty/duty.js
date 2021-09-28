const {readFileSync, writeFile} = require('fs');

var dutyList = JSON.parse(readFileSync('./duty/duty.json'));

function increase(id, maxVal){
    return (id + 1 <= maxVal) ? id + 1: 0;
}

module.exports.increase = increase;

module.exports.dutyReply = function(){
    let today = parseInt(new Date(Date.now()).getDay()),
        id = dutyList.id,
        dutyDate = dutyList.date,
        students = dutyList.students;
    if(today != dutyDate && today != 0){
        id = increase(id, 12);
        dutyList.id = id;
        dutyList.date = today;
        writeFile('./duty/duty.json', JSON.stringify(dutyList), (err) => {});
    }
    return `Доску сегодня трут: *${students.group1[id]}* и *${students.group2[id]}*`;
}