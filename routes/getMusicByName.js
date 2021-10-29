var express = require("express");
var router = express.Router();
const { spawn } = require("child_process");
var fs = require("fs");

// 模糊查询歌曲名
router.post("/", (req, res, next) => {
  // 判断POST请求是否包含请求体
  if (req.body) {
    const body = req.body;
    fs.writeFileSync("music_name.txt", body.musicName);
    // 控制台执行python脚本
    const data = spawn("python3", ["mongoFind.py"]);
    // 监听控制台输出
    data.stdout.on("data", (data) => {
      console.log(data.toString())
    });
    // 监听python脚本执行完成
    data.stdout.on('close', () => {
      const data = fs.readFileSync('./data_music.txt',{encoding: 'utf-8'})
      const music_result_arr = data.split('\n')
      let music_result_json = []
      music_result_arr.map(item => {
        music_result_json.push(JSON.parse(item))
      })
      // 发送JSON
      res.send({success: true, result: music_result_json})
    })
  } else {
    res.send({ errmsg: "request Body为空" }).status(404);
    next();
  }
});

module.exports = router;
