var express = require("express");
var router = express.Router();
const { spawn } = require("child_process");
var fs = require("fs");
const cors = require("cors");
const connectMusicDB = require("../components/mongoConnection");
const runPython = require("../components/runPython");

router.use(express.json());
router.use(express.urlencoded({ extended: false }));
router.use(cors());

// 模糊查询歌曲名
router.post("/", (req, res, next) => {
  // 判断POST请求是否包含请求体
  runPython("./pyprog/mongoDataCCl.py", () => {
    let data = fs.readFileSync("./music_table.txt", { encoding: "utf-8" });
    const music_result_arr = data.split("\n");
    let music_result_json = [];
    music_result_arr.map((item) => {
      music_result_json.push(JSON.parse(item));
    });
    res.send({ success: true, result: music_result_json });
    // fs.unlink("./music_pl.txt", (err) => {
    //   if (err) throw err;
    // });
  });
});

module.exports = router;
