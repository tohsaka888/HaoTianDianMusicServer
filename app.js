var createError = require("http-errors");
var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
var cors = require("cors")

var indexRouter = require("./routes/index");
var musicTagRouter = require("./routes/getMusicByTag");
var musicNameRouter = require("./routes/getMusicByName");
var collectMusicRouter = require("./routes/collectMusic");
var getDefaultPlayListRouter = require("./routes/getDefaultPlayList");
var getDefaultMusicRouter = require("./routes/getDefaultMusic");
var getSimilarity = require("./routes/getSimilarity");
var getRecomendM = require("./routes/getRecomendM");
var getRecomendP = require("./routes/getRecomendP");
var getMusicHeatList = require("./routes/getMHL");
var getNextMusic = require("./routes/getNextMusic");

const { appendFile } = require("fs");
const { getDefaultSettings } = require("http2");
var app = express();

// view engine setup
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "jade");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
app.use(cors())

app.use("/", indexRouter);
app.use("/getMusicByTag", musicTagRouter);
app.use("/getMusicByName", musicNameRouter);
app.use("/collectMusic", collectMusicRouter);
app.use("/getDefaultPlayList", getDefaultPlayListRouter);
app.use("/getDefaultMusic", getDefaultMusicRouter);
app.use("/getSimilarity", getSimilarity);
app.use("/getRecomendM", getRecomendM);
app.use("/getRecomendP", getRecomendP);
app.use("/getHML", getMusicHeatList);
app.use("/getNextMusic", getNextMusic);
// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render("error");
});

// 生产环境 http://81.68.113.218:5555/
// 测试环境 http://81.68.113.218:5556/
// 测试完成后请将端口改为正式环境并重新使用pm2挂载后台服务
// 停止后台服务 pm2 stop app.js
// 挂载后台服务 pm2 start app.js
// 重启后台服务 pm2 restart app.js
app.listen("5555", () => {
  console.log("sever is on http://81.68.113.218:5555/");
});

module.exports = app;
