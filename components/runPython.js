const { spawn } = require("child_process");

const runPython = (pythonFilePath, callback) => {
  // 控制台执行python脚本
  const data = spawn("python3", [pythonFilePath]);
  // 监听控制台输出
  data.stdout.on("data", (data) => {
    console.log(data.toString())
  });
  // 监听python脚本执行完成
  data.stdout.on('close', callback)
}

module.exports = runPython