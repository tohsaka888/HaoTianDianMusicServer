var { MongoSessionDaemon } = require("mongo-client-daemon");

// mongoDB连接组件
const connectMusicDB = async () => {
  const db = new MongoSessionDaemon(
    "mongodb://tohsaka888:swy156132264@81.68.113.218:27017/"
  ); //输入连接数据库的地址
  const getSession = await db.getSession();
  return await getSession.db("Music"); // 返回Music数据库
};

module.exports = connectMusicDB
