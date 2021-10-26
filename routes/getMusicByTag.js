var express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");

var router = express.Router();

router.post("/", async (req, res, next) => {
  let music_all_json = [];
  if (req.body) {
    console.log(req.body);
    const body = req.body;
    if (body.musicName) {
      const data = spawn("python3", ["connMongo_bak.py"]);
      let load = 0;
      data.stdout.on("data", () => {
        console.log(
          "===========loading=" + load.toFixed(1) + "%=============="
        );
        load += 100 / 1075;
      });
      data.stdout.on("close", () => {
        let data = fs.readFileSync("music_by_tags.txt", { encoding: "utf-8" });
        let music_all_string = data.toString();
        let music_all_array = music_all_string.split("\n");
        music_all_array = music_all_array.splice(0, music_all_array.length - 1);
        music_all_array.map((item) => {
          music_all_json.push(JSON.parse(item));
        });
        res.send(music_all_json.slice(0, 10));
      });
    }
  } else {
    res.send({ errmsg: "request Body为空" }).status(404);
    next();
  }
});

module.exports = router;
