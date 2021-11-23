// var express = require("express");
// var router = express.Router();
// const { spawn } = require("child_process");
// var fs = require("fs");
// const cors = require('cors')
// const connectMusicDB = require("../components/mongoConnection");
// const runPython = require("../components/runPython");

// router.use(express.json())
// router.use(express.urlencoded({ extended: false }))
// router.use(cors())

// // 模糊查询歌曲名
// router.post("/", (req, res, next) => {
//   // 判断POST请求是否包含请求体
//   if (Object.keys(req.body).length) {
//     const body = req.body
//     // 数据库随机取180个歌单
//     if (body.tag && body.page === 1) {

//     } else if ()
//   } else {
//     res.send({ errmsg: "request Body为空" }).status(404);
//     next();
//   }
// });

// module.exports = router;
