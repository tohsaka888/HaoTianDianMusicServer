var express = require("express");
var router = express.Router();
// const { spawn } = require("child_process");
// var fs = require("fs");
const cors = require('cors')
const connectMusicDB = require("../components/mongoConnection");
const runPython = require("../components/runPython");

router.use(express.json())
router.use(express.urlencoded({ extended: false }))
router.use(cors())

// 获取上一曲or下一曲
router.post("/next", async (req, res, next) => {
  try {
    // 判断POST请求是否包含请求体
    if (Object.keys(req.body).length) {
      const body = req.body;
      if (body.playlistId) {
        // 有歌单取歌单当前歌曲的上一首或下一首
        const MusicDB = await connectMusicDB();
        const playlistCollection = await MusicDB.collection('MusicPlayList');
        const this_playlist = await playlistCollection.find({ id: body.playlistId }).toArray()
        const musics = this_playlist[0].tracks
        let currentIndex = -1
        if (body.musicId) {
          musics.map((item, index) => {
            if (item.id === body.musicId) {
              currentIndex = index
            }
          })
          if (currentIndex === -1) {
            res.send({ success: false, errmsg: '当前歌单内无此歌曲' })
          }
          // 如果为最后一首,循环此歌单
          if (currentIndex === musics.length - 1) {
            currentIndex = 0
          } else {
            currentIndex++
          }
          res.send({ music: musics[currentIndex], success: true })
        } else {
          res.send({ success: false, errmsg: '没有musicID' })
        }
      } else {
        // 随机取一首
        const musicDB = await connectMusicDB();
        const allMusicCollection = await musicDB.collection("MusicByTags")
        const musicData = await allMusicCollection.aggregate([{ $sample: { size: 1 } }]).toArray()
        res.send({ music: musicData, success: true })
      }
    } else {
      res.send({ errmsg: "request Body为空" }).status(404);
      next()
    }
  } catch (error) {
    res.send({ success: false, errmsg: error.name + error.message })
    next()
  }
});

// 上一首
router.post("/previous", async (req, res, next) => {
  try {
    // 判断POST请求是否包含请求体
    if (Object.keys(req.body).length) {
      const body = req.body;
      if (body.playlistId) {
        // 有歌单取歌单当前歌曲的上一首或下一首
        const MusicDB = await connectMusicDB();
        const playlistCollection = await MusicDB.collection('MusicPlayList');
        const this_playlist = await playlistCollection.find({ id: body.playlistId }).toArray()
        const musics = this_playlist[0].tracks
        let currentIndex = -1
        if (body.musicId) {
          musics.map((item, index) => {
            if (item.id === body.musicId) {
              currentIndex = index
            }
          })
          if (currentIndex === -1) {
            res.send({ success: false, errmsg: '当前歌单内无此歌曲' })
          }
          // 如果为最后一首,循环此歌单
          if (currentIndex === 0) {
            currentIndex = musics.length - 1
          } else {
            currentIndex--
          }
          res.send({ music: musics[currentIndex], success: true })
        } else {
          res.send({ success: false, errmsg: '没有musicID' })
        }
      } else {
        // 随机取一首
        const musicDB = await connectMusicDB();
        const allMusicCollection = await musicDB.collection("MusicByTags")
        const musicData = await allMusicCollection.aggregate([{ $sample: { size: 1 } }]).toArray()
        res.send({ music: musicData, success: true })
      }
    } else {
      res.send({ errmsg: "request Body为空" }).status(404);
      next()
    }
  } catch (error) {
    res.send({ success: false, errmsg: error.name + error.message })
    next()
  }
});

module.exports = router;
