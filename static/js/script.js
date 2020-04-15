/* 更新ボタン */

const updateExist = async(url, element) => {
    const sensorData = await fetch(url)
    .then(response => response.text())
    const target = document.getElementById(element)
    target.innerHTML = `<h1>${sensorData}</h1>`
    }


/* Slack投稿ボタン */

function slack() {
    const url = 'https://hooks.slack.com/services/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';
    const strData = {
        text: 'good!!!!!'
    };
    const xml = new XMLHttpRequest();
    xml.open("POST", url, false);
    xml.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xml.send(`payload=${JSON.stringify(strData)}`)
}

