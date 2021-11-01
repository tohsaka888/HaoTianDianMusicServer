const express = require("express");
const router = express.Router();
const connectMusicDB = require("../components/mongoConnection");
const cors = require('cors')

router.use(express.json())
router.use(express.urlencoded({ extended: false }))
router.use(cors())

router.post("/", async (req, res, next) => {
  try {
    if (req.body) {
      let collectData = req.body;
      if (collectData.musicId && collectData.userId) {
        const musicDB = await connectMusicDB();
        const collectMusicCollection = await musicDB.collection("CollectMusic");
        const insertResult = await collectMusicCollection.insertOne({
          userId: collectData.userId,
          musicId: collectData.musicId,
        });
        if (insertResult.insertedId) {
          res.send({ success: true, message: "收藏成功！" }).status(200);
        } else {
          res.send({ success: false, message: "收藏失败！" }).status(300);
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
