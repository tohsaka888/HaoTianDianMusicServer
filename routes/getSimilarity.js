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
    if (Object.keys(req.body).length) {
        const body = req.body;
        fs.writeFileSync("music_similarity.json", JSON.stringify(body));
        runPython("./pyprog/mongoSimilarity.py", () => {
            const data = fs.readFileSync('./music_similarity.txt', { encoding: 'utf-8' })

            const music_result_arr = data.split('\n')
            let music_result_json = []
            music_result_arr.map(item => {
                music_result_json.push(JSON.parse(item))
            })
            // 发送JSON
            if (music_result_json.length == 1) {
                res.send({ errmsg: "Not Found Music" }).status(404);
            } else {
                res.send({ success: true, result: music_result_json })
            }
            fs.unlink('./music_similarity.txt', (err) => {
                if (err) throw err;
            });
        })
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
