const id = document.getElementById("id").getAttribute("data-json");
const editor = ace.edit("editor");
const output_msg = document.getElementById("output-msg");
const submit_btn = document.getElementById("submit");
const reset_btn = document.getElementById("reset");

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
  let url = "http://localhost:8000/interface/requests/evaluate";
  let csrftoken = Cookies.get("csrftoken");

  let data = {
    id: id,
    code: editor.getValue(),
    key: "TechFestOC",
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
