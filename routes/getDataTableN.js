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

router.post("/", async (req, res, next) => {
  const body = req.body;
  const MusicDB = await connectMusicDB();
  // 数据库操作需要异步
  const catchPLByCat = await MusicDB.collection("DataAnalyse");
  let collectData = await catchPLByCat.aggregate(
    [
      { $project: { name: 1, _id: 0 } },
    ],
  ).toArray();
  if (collectData.length) {
    res.send({ success: true, data: collectData }).status(200);
  } else {
    res.send({ success: false, data: "", message: "对象不存在" });
  }
});

module.exports = router;
