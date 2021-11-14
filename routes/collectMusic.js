const express = require("express");
const router = express.Router();
const connectMusicDB = require("../components/mongoConnection");
const cors = require('cors')
var fs = require("fs");
const { time } = require("console");
router.use(express.json())
router.use(express.urlencoded({ extended: false }))
router.use(cors())

router.post("/", async (req, res, next) => {

  try {
    if (req.body) {
      let collectData = req.body;
      if (collectData.musicId && collectData.userId) {
        const tT = Date.now()
        const musicDB = await connectMusicDB();
        const collectMusicCollection = await musicDB.collection("CollectMusic");
        // const targetUser = await collectMusicCollection.find({ "userId": collectData.musicId })
        // fs.writeFileSync("tmp_data_userId.json", JSON.stringify(targetUser))
        const isCollectMusic = await collectMusicCollection.find({ userId: collectData.userId, musicId: collectData.musicId }).toArray()
        let insertResult = null
        let deleteResult = null
        if (isCollectMusic.length) {
          deleteResult = await collectMusicCollection.deleteOne({
            userId: collectData.userId,
            musicId: collectData.musicId,
          });
          if (deleteResult.deletedCount) {
            res.send({ success: true, isCollect: false, message: '取消收藏成功' })
          } else {
            res.send({ success: false, isCollect: true, message: '取消收藏失败' })
          }
        } else {
          insertResult = await collectMusicCollection.insertOne({
            userId: collectData.userId,
            musicId: collectData.musicId,
            tags: collectData.tags,
            timestamp: tT
          });
          if (insertResult.insertedId) {
            res.send({ success: true, isCollect: true, message: '收藏成功' })
          } else {
            res.send({ success: false, isCollect: false, message: '收藏失败' })
          }
        }
      }
    }
  } catch (error) {
    res
      .send({ success: false, message: error.title + error.message })
      .status(404);
    next();
  }
});

module.exports = router;
