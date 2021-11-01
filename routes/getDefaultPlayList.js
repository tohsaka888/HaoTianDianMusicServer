var express = require("express");
var router = express.Router();
const { spawn } = require("child_process");
var fs = require("fs");
const cors = require('cors')
const connectMusicDB = require("../components/mongoConnection");
const runPython = require("../components/runPython");

router.use(express.json())
router.use(express.urlencoded({ extended: false }))
router.use(cors())

// 模糊查询歌曲名
router.post("/", (req, res, next) => {
  // 判断POST请求是否包含请求体
  try {
    runPython("../pyprog/mongoRandomPlayList.py", () => {
      const data = fs.readFileSync('./random_playlist.txt', { encoding: 'utf-8' })
      const music_result_arr = data.split('\n')
      let music_result_json = []
      music_result_arr.map(item => {
        music_result_json.push(JSON.parse(item))
      })
      // 发送JSON
      res.send({ success: true, result: music_result_json })
    })
  } catch (error) {
    res.send({ success: false }).status(404);
    next();
  }
});

// router.post('/randomPlayList', async (req, res, next) => {
//   try {
//     const musicDB = await connectMusicDB();
//     const allMusicCollection = await musicDB.collection("MusicPlayList")
//     const musicData = await allMusicCollection.aggregate([{ $sample: { size: 20 } }]).toArray()
//     res.send({ success: true, musics: musicData })
//   } catch (error) {
//     res.send({ success: false }).status(404)
//   }
// })

module.exports = router;
