## mongoDB连接组件使用实例
### 以POST请求为例
```javascript
const express = require("express")
const router = express.Router()
const connectMusicDB = require("../components/mongoConnection")

router.post('/', async(req, res, next) => {
  try {
    // 测试MongoDB连接
    // 获取到DB
    const MusicDB = await connectMusicDB();
    // 获取到Collection
    const musicCollection = await MusicDB.collection('MusicByArtists');
    // 获取到数据(Array类型)
    const data = await musicCollection.find({}).toArray()
    console.log(data)
    
  } catch (error) {
    console.log(error)
    next()
  }
})

module.exports = router
```