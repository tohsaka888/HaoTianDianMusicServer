## 执行Python脚本组件使用说明

```javascript
// 第一个参数为Python文件路径,第二个参数为python脚本执行完成后的回调
// 第二个参数可直接传递一个匿名函数,如下所示,也可以单独传一个函数
runPython("mongoFind.py", () => {
  // 读文件
  const data = fs.readFileSync('./data_music.txt',{encoding: 'utf-8'})
  const music_result_arr = data.split('\n')
  let music_result_json = []
  // 将查询结果转换为JSON
  music_result_arr.map(item => {
    music_result_json.push(JSON.parse(item))
  })
  // 发送JSON
  res.send({success: true, result: music_result_json})
})
```