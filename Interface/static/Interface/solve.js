// Written by harish - lead dev, OC member
// Not for distibution

const id = document.getElementById("id").getAttribute("data-json");
const editor = ace.edit("editor");
const output_msg = document.getElementById("output-msg");
const submit_btn = document.getElementById("submit");
const reset_btn = document.getElementById("reset");
const timer = document.getElementById("stopwatch");

let time = 0,
  interval;

editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");
editor.setShowPrintMargin(false);
editor.session.setTabSize(2);
editor.session.setUseSoftTabs(true);
editor.resize();
document.getElementById("editor").style.width = "80vw";
document.getElementById("editor").style.fontSize = "20px";

submit_btn.addEventListener("click", async () => {
  editor.session.setValue(editor.getValue());
  let url = window.location.origin + "/interface/requests/evaluate";
  let csrftoken = Cookies.get("csrftoken");

  let data = {
    id: id,
    code: editor.getValue(),
    key: "TechFestOC",
    timeTaken: time,
  };

  let options = {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json;charset=utf-8",
      "X-CSRFToken": csrftoken,
    },
  };

  output_msg.innerText = "";
  await fetch(url, options)
    .then((res) => res.json())
    .then((d) => {
      console.log();
      if (d?.request === "error") {
        output_msg.style.color = "red";
      } else if (d?.request === "Wrong") {
        output_msg.style.color = "coral";
      } else if (d?.request === "passed") {
        output_msg.style.color = "green";
        submit_btn.style.display = "none";
        stopTimer();
      }

      output_msg.innerText = d?.msg;
    });
});

reset_btn.addEventListener("click", () => {
  editor.session.setValue(
    document.getElementById("userCode").getAttribute("data-json")
  );
  output_msg.innerText = "";
});

editor.session.setValue(
  document.getElementById("userCode").getAttribute("data-json")
);

const showTime = () => {
  time = parseInt(localStorage.getItem("time"));
  time += 1;
  timer.innerHTML = toHHMMSS(time);
  localStorage.setItem("time", time);
};

const start = () => {
  let timeStorage = localStorage.getItem("time");
  if (timeStorage == null) {
    localStorage.setItem("time", time);
  }
  interval = setInterval(showTime, 1000);
};

const stopTimer = () => {
  clearInterval(interval);
  interval = null;
  time = 0;
  timer.innerHTML = toHHMMSS(time);
  localStorage.setItem("time", time);
};

const toHHMMSS = (time) => {
  let hours = Math.floor(time / 3600);
  let minutes = Math.floor((time - hours * 3600) / 60);
  let seconds = time - hours * 3600 - minutes * 60;

  hours = `${hours}`.padStart(2, "0");
  minutes = `${minutes}`.padStart(2, "0");
  seconds = `${seconds}`.padStart(2, "0");

  return hours + ":" + minutes + ":" + seconds;
};

const setTimeCounter = () => {
  const timeStorage = localStorage.getItem("time");
  if (timeStorage != null) {
    timer.innerHTML = toHHMMSS(parseInt(timeStorage));
  }
};

setTimeCounter();
start();
