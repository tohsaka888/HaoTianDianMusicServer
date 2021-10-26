var express = require("express");
var router = express.Router();
var fs = require("fs")

// 模糊查询歌曲名
router.post("/",(req, res, next) => {
  if (req.body) {
    const body = req.body;
    fs.writeFileSync('music_name.txt', body.musicName)
    res.send(body.musicName)
  } else {
    res.send({ errmsg: "request Body为空" }).status(404);
    next();
  }
});

module.exports = router;
