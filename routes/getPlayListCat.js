var express = require("express");
var router = express.Router();
const { spawn } = require("child_process");
var fs = require("fs");
const cors = require('cors')
const connectMusicDB = require("../components/mongoConnection");
// const runPython = require("../components/runPython");

router.use(express.json())
router.use(express.urlencoded({ extended: false }))
router.use(cors())

// 模糊查询歌曲名
router.post("/", async (req, res, next) => {
    // 判断POST请求是否包含请求体
    if (Object.keys(req.body).length) {
      const body = req.body;
        // 连接数据库
      const MusicDB = await connectMusicDB();
        // 数据库操作需要异步
      const catchPLByCat = await MusicDB.collection("MusicPlayList");
      let collectData = await catchPLByCat.aggregate(
        [ 
          {$match: {tags:{ $all: [body.tags]}}},
          {$sample: {size: 90}},
          {$sort:{tags:-1}}       
        ]).toArray();
      if (collectData.length) {
          res.send({ success: true, data: collectData}).status(200)
        } else {
          res.send({ success: false, data: "",message: "对象不存在"}).status(200)
        }
      } else {
            res.send({ errmsg: "request Body为空" }).status(404);
        next();
    }
});

module.exports = router;
