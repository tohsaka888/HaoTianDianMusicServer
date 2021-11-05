const express = require("express");
const router = express.Router();
const connectMusicDB = require("../components/mongoConnection");
const cors = require('cors')
var fs = require("fs")
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
        // const targetUser = await collectMusicCollection.find({ "userId": collectData.musicId })
        // fs.writeFileSync("tmp_data_userId.json", JSON.stringify(targetUser))
        const insertResult = await collectMusicCollection.updateOne({
          userId: collectData.userId,
          musicId: collectData.musicId,
          tags: collectData.tags,
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
