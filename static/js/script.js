/* ページの自動更新 */
setTimeout(function(){
    location.reload();
}, 60000);

/* データの更新 */
const updateExist = async(url, element) => {
    const sensorData = await fetch(url)
    .then(response => response.text())
    const target = document.getElementById(element)
    target.innerHTML = `<h3>${sensorData}</h3>`
    }

/* 出席時にSlackへ投稿 */


/* 更新 */
function foo(){
    updateExist('/exist', 'data');
}


/* Slack投稿ボタン */
function slack() {
    const url = '';
    const strData = {
        text: 'いつも頑張っているね！えらいぞ！'
    };
    const xml = new XMLHttpRequest();
    xml.open("POST", url, false);
    xml.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xml.send(`payload=${JSON.stringify(strData)}`)
}

