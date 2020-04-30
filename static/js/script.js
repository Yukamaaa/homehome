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

const updateLog = async(url, element) => {
    const sensorData = await fetch(url)
    .then(response => response.text())
    const target = document.getElementById(element)
    target.innerHTML = `<h3>${sensorData}</h3>`
    }


/* リロードボタン */
function foo(){
    updateExist('/login', 'data');
    updateLog('/logout', 'data2');
}


/* Slack投稿ボタン */
function slack() {
    const url = 'services/T010V4PKESJ/B012M909PLY/177F8n5PrfYi6k8Mw0bga7o8';
    const strData = {
        text: 'いつも頑張っているね！えらいぞ！'
    };
    const xml = new XMLHttpRequest();
    xml.open("POST", url, false);
    xml.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xml.send(`payload=${JSON.stringify(strData)}`)
}

