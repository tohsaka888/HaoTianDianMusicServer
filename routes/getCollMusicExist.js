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
        // fs.writeFileSync("music_colle_existence.json", JSON.stringify(body));
        // runPython("./pyprog/mongoCheckColle.py", () => {
        //     const data = fs.readFileSync('./music_colle_existence.txt', { encoding: 'utf-8' })
        //     const music_result_arr = data.split('\n')
        //     let music_result_json = {}
        //     music_result_arr.map(item => {
        //         music_result_json = JSON.parse(item)
        //     })
        //     // 发送JSON
        //     res.send({ success: true, existence: music_result_json.existence })
        //     fs.unlink('./music_colle_existence.txt', (err) => {
        //         if (err) throw err;
        //     });
        // })
        const MusicDB = await connectMusicDB();
        const collectMusicCollection = await MusicDB.collection("CollectMusic");
        let collectData = []
        collectData = await collectMusicCollection.find({ musicId: body.musicId, userId: body.userId }).toArray()
        if (collectData.length) {
            res.send({ success: true, existence: true }).status(200)
        } else {
            res.send({ success: true, existence: false }).status(200)
        }
    } else {
        res.send({ errmsg: "request Body为空" }).status(404);
        next();
    }
});

router.post('/random', async (req, res, next) => {
    try {
        const musicDB = await connectMusicDB();
        const allMusicCollection = await musicDB.collection("MusicByTags")
        const musicData = await allMusicCollection.aggregate([{ $sample: { size: 12 } }]).toArray()
        res.send({ success: true, musics: musicData })
    } catch (error) {
        res.send({ success: false }).status(404)
    }
})

module.exports = router;
