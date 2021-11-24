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
  if (Object.keys(req.body).length) {
    const body = req.body;
    fs.writeFileSync("music_cat.json", JSON.stringify(body));
    runPython("./pyprog/mongoPLCat.py", () => {
      const data = fs.readFileSync("./music_pl.txt", { encoding: "utf-8" });
      if (data.length === 0) {
        res.send({ success: false, result: data, message: "Out Of Range" });
      } else {
        const music_result_arr = data.split("\n");
        let music_result_json = [];
        music_result_arr.map((item) => {
          music_result_json.push(JSON.parse(item));
        });
        res.send({ success: true, result: music_result_json });
      }
      fs.unlink("./music_pl.txt", (err) => {
        if (err) throw err;
      });
    });
  } else {
    res.send({ errmsg: "request Body为空,检查是否包含请求体或者是否设置请求头" }).status(404);
    next();
  }
});

router.post("/random", async (req, res, next) => {
  try {
    const musicDB = await connectMusicDB();
    const allMusicCollection = await musicDB.collection("MusicByTags");
    const musicData = await allMusicCollection.aggregate([{
      $sample: { size: 12 },
    }]).toArray();
    res.send({ success: true, musics: musicData });
  } catch (error) {
    res.send({ success: false }).status(404);
  }
});

module.exports = router;
