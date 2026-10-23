---
name: wechat-channels-video
slug: wechat-channels-video
displayName: 微信视频号发布
version: 1.0.0
summary: 用 ego-browser 在微信视频号助手发布视频：上传视频、描述/话题/短标题/位置/封面/声明原创/活动关联，保存为草稿
license: MIT
description: 用 ego-browser 在微信视频号助手发布视频：上传视频文件、填描述/短标题/话题/位置/封面（waitForFileChooser 拦截原生选文件），声明原创、关联活动，保存为草稿。默认终点是“保存草稿”——发表需扫码，留给人完成。内置 11 期实战避坑清单。
---

# 微信视频号发视频（ego-browser）

用 ego-browser（Ego Lite Chromium）在 channels.weixin.qq.com 视频号助手完成视频发布，终点为**保存草稿**。不点“发表”——那是扫码人工环节，结束前 `handOff()` 把浏览器停在草稿箱交给用户。

> 2026-09 起本 skill 从腾讯 BrowserSkill（bsk CLI 驱动 Chrome Agent Window）整体迁移到 ego-browser，EP037 全流程实测通过（49MB 竖版上传 → 填表 → 草稿落盘验证）。

## 调用方式与 API 速查

每次 `ego-browser nodejs` 调用都是一个新 Node 进程；TaskSpace、Page 标签跨调用持久，JS 变量不持久。

```bash
# 多行脚本用 heredoc；一两行用 ego-browser nodejs -e '...'
ego-browser nodejs <<'EOF'
const task = await taskSpace("publish epXXX to wechat channels");
console.log({ spaceId: task.spaceId });   // 记下 spaceId，后续轮次 taskSpace(<id>) 复用
const page = task.page("p1");             // 首个页面就是 p1，用 goto 复用，别另开 Page
await page.goto("https://channels.weixin.qq.com");
await page.waitForTimeout(3000);
console.log(await page.snapshot());
EOF
```

| API | 说明 |
| --- | --- |
| `taskSpace(name)` / `taskSpace(id)` | 建 / 复用任务空间；一个用户目标只用一个 space |
| `task.page("p1")` / `task.userPage()` | 托管页 / 用户正拿着的页（unmanaged 需 `task.adopt()`） |
| `page.goto / waitForTimeout / waitForSelector` | 导航与等待 |
| `page.snapshot()` | 语义树，能看穿 open shadow root；用于**观察** |
| `page.evaluate(fn, arg)` | 页面内执行；**只收一个 JSON 可序列化参数**（长文案用它传，避免 shell 转义） |
| `page.click / fill / press` | 常规 DOM 可用；wujie 内会报 “\<wujie-app\> intercepts pointer events” |
| `page.mouse.click(x, y)` / `move / wheel` | 坐标级真实点击；**wujie 内的弹层靠它** |
| `page.screenshot({ path })` | 视觉确认（弹层状态、表单终态），用读图工具看 |
| `task.handOff()` | 交给用户（扫码发表等人工环节），结束本轮 |
| `task.finish({ keep: ["p1"] })` | 收尾；`keep: []` 全关，需用户接着操作就别 finish |

**关键差异**：snapshot 看得穿 wujie 的 shadow root，但 ref/text 点击进不去（wujie-app 拦截指针事件）。wujie 内的动作一律两条路：`evaluate` 里 DOM 查询后 `.click()`，或 `getBoundingClientRect` 取坐标后 `page.mouse.click(x, y)`。

**恢复**：space 出异常先在原 space 里重探（`taskSpace(<id>)` + 重新 snapshot/evaluate），不要开新 space；Page 卡死救不回来就 `page.close()` 后 `task.newPage()`。登录态存在 Ego 浏览器 profile 里，这些操作都不丢登录。

## 前置条件

- ego-browser 已装（`ego-browser --version`）。
- 视频文件在本机磁盘（mp4；视频号竖版 1080×1920）。
- 视频号助手已登录。未登录：goto https://channels.weixin.qq.com 后 `await task.handOff()`，请用户在可见浏览器窗口扫码（ego 的浏览器窗用户一直看得见，比任何浮层都直接），确认账号无误后等用户回话，`taskSpace(<id>)` 接着干。**登录页“加载失败，点击重试”是红鲱鱼**：那是“微信快捷登录”探本地微信客户端（`localhost.weixin.qq.com:13015` 等）失败，二维码本身在跨域 iframe 里、点重试救不了。注意升级 ego lite（如 Chromium 大版本更新）后登录态可能被刷新，开工先看 URL 是否跳到 login.html。

## AIPCast 系列目录约定（061 起）

新系列素材在 `~/CascadeProjects/ai-podcast/aipcast/<期号>/`，每期自带全套物料，**文案不用自己写**：

- `aipcast-XXX-9x16.mp4` 或期名命名 mp4 — 视频（1080×1920，多为 60–120 秒短条）
- `cover-3x4.png` — 封面（1080×1440，PNG 可直接传）
- `发布文案.md` — 含**标题（≤20 字）、描述、话题**三个「复制」块，描述里常带博客链接
- `访谈文字版.md` — 博客图文版原文

要点：

- **描述/话题直接用文件里的「描述」「话题」块**，不要套旧栏目的长段落风格；话题追加在描述末尾另起一行。
- **短标题从「标题」块改写**：自带标题里的 `|`、`#` 不在符号白名单，取主句（如「一封邮件断全网\|听懂AI#061」→「一封邮件断全网」）。
- 文案里写的文件路径（如 `final/xxx.mp4`）可能与实际目录有出入，**以 `ls` 实际文件为准**。
- 活动仍按「AI科普」搜索轮换选用（六个活动池子转圈）。

## 流程

### 0. 路由到发表页（坑：直接 URL 白屏）

视频号助手是 **wujie 微前端**：所有表单 DOM 都在 `document.querySelector('wujie-app').shadowRoot` 里，外层 document 查询一律为空。创作面板是懒加载的，**直接 goto /platform/post/create 会白屏**。必须走 UI 路径：

```
首页 → 左栏“内容管理” → “视频” → 页面右侧“发表视频”按钮
```

首页 snapshot 里“发表视频”是普通可点元素（不在 wujie 拦截范围内），直接 `page.click("@<ref>")`。发表页就绪标志（evaluate 探 wujie）：inner text 出现“视频描述”“短标题”，隐藏 input 与“保存草稿”都在。

```js
const state = await page.evaluate(() => {
  const app = document.querySelector('wujie-app');
  if (!app || !app.shadowRoot) return { wujie: false };
  const t = app.shadowRoot.textContent || '';
  return {
    wujie: true,
    hasDesc: t.indexOf('视频描述') >= 0,
    hasShort: t.indexOf('短标题') >= 0,
    hasUpload: !!app.shadowRoot.querySelector('input[type=file][accept*="video"]'),
    hasSave: t.indexOf('保存草稿') >= 0,
  };
});
```

### 1. 上传视频（本地 CORS 服务 + DataTransfer）

文件大（几十到上百 MB）进不了 base64，起本地服务让页面自己 fetch：

```bash
# 后台 job 运行；端口 18765，file 换实际路径
node -e '
const http = require("http"); const fs = require("fs");
const file = "<视频绝对路径>";
http.createServer((req, res) => {
  res.writeHead(200, {"Access-Control-Allow-Origin":"*","Content-Type":"video/mp4","Content-Length": fs.statSync(file).size});
  fs.createReadStream(file).pipe(res);
}).listen(18765,"127.0.0.1",() => console.log("serving :18765"));'
```

https 页面 fetch `http://127.0.0.1` 不算 mixed content（localhost 是可信来源）。上传 input 是**隐藏**的 `input[type=file][accept*="video"]`，DataTransfer 注入有效（视频上传组件没做 isTrusted 加固——封面组件做了，见“封面”节）：

```js
const r = await page.evaluate(async () => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const input = root.querySelector('input[type=file][accept*="video"]');
  const resp = await fetch('http://127.0.0.1:18765/video.mp4');
  const dt = new DataTransfer();
  dt.items.add(new File([await resp.blob()], 'video.mp4', { type: 'video/mp4' }));
  input.files = dt.files;
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
  return 'injected ' + dt.files[0].size;
});
```

**验证**：轮询 wujie inner text，出现“转发/赞/评论”预览统计卡、进度百分比停在 100% 不再变化即完成。⚠️ ego-browser 没有 bsk network，而 `performance.getEntriesByType('resource')` **抓不到这次上传 POST**（实测 49MB 传完后 resource 里只有静态资源）——DOM 状态是唯一可靠信号。上传期间不要开始填表（布局会位移）。

### 1.5 检查点：立即存一次草稿

上传完成 → **立刻**用第 5 节脚本点一次“保存草稿”，把昂贵的视频上传先落盘，再回去填描述/短标题/位置，最后再存一次。会话中途出任何意外，都不至于重传大文件。

### 2. 填描述（坑：不是 contenteditable，是自定义编辑器）

描述框是 `.input-editor` 的 div，**没有** textarea/contenteditable 语义，`page.fill` 打不进去。用 execCommand；文案从 evaluate 的**第二参数**传入，别塞进脚本字面量：

```js
const desc = "……长文案……";
const tags = "#话题1 #话题2";
const head = await page.evaluate((p) => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const ed = root.querySelector('.input-editor');
  ed.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('delete', false, null);
  document.execCommand('insertText', false, p.desc);
  return ed.textContent.slice(0, 40);
}, { desc });
const tail = await page.evaluate((p) => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const ed = root.querySelector('.input-editor');
  ed.focus();
  document.execCommand('insertParagraph');
  document.execCommand('insertText', false, p.tags);
  const out = ed.textContent;
  ed.blur();
  return out.slice(-60);
}, { tags });
```

核对 head/tail（tail 必须含话题行才算成功）。

### 3. 短标题（真 input，native setter）

短标题是普通 `<input type=text>`（placeholder 含“短标题”），要走 native setter 否则框架不认：

```js
const v = await page.evaluate(() => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const inp = root.querySelector('input[placeholder*="短标题"]');
  const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  setter.call(inp, '<短标题>');
  inp.dispatchEvent(new Event('input', { bubbles: true }));
  inp.dispatchEvent(new Event('change', { bubbles: true }));
  return inp.value;
});
```

返回 `inp.value` 核对。**注意 innerText 永远不含 input 的值**——整页 innerText 验证短标题会误报失败，必须读 `input.value` 本身。

**短标题硬限制（EP038/EP042 实测）**：≤16 字（「GPT-6.1 Sol能当主力吗？」17 字会被拒）；符号白名单只有书名号、引号、冒号、加号、问号、百分号、摄氏度——**全角逗号要换空格，版本号里的小数点也不行**（「GPT-6.1」触发特殊字符警告，改「GPT新模型」这类说法）。填完检查输入框下方有没有红字警告。

### 4. 位置（默认带城市，改“不显示位置”）

**实测最稳路径**（`element.click()` 会让弹层开开关关不渲染；`page.click('text=…')` 又被 wujie 拦截报 “intercepts pointer events”）：

1. 先截图定位“位置”行下拉框坐标（表单右列），`page.mouse.click(x, y)` 点开。
2. `waitForTimeout(900)` 后 `page.snapshot()`——弹层里应出现“搜索附近位置”输入框和“不显示位置”。
3. evaluate 取“不显示位置”（textContent 精确等于且可见）的中心坐标，`page.mouse.click` 点它。
4. evaluate 验证位置字段文案已变为“不显示位置”。

**重要（EP044 教训）**：evaluate 找到的“不显示位置”元素坐标可能是过期/隐藏层，点下去不生效（症状：字段文案没变、弹层关了）。**点完必须回读字段值验证**；不生效就改成「弹层开着截图 → 按截图上的可见坐标直接 mouse.click」，截图引导法百分百命中。触发器太靠近视口底部时弹层可能没空间展开，先把该行滚到视口上部再点开。

```js
const pos = await page.evaluate(() => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const els = Array.from(root.querySelectorAll('div, span, li, p')).filter(el =>
    el.childElementCount === 0 && el.textContent.trim() === '不显示位置' && el.offsetParent !== null);
  if (!els.length) return null;
  const r = els[0].getBoundingClientRect();
  return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
});
await page.mouse.click(pos.x, pos.y, { label: "select 不显示位置" });
```

### 5. 保存为草稿（终点，不要发表）

```js
const save = await page.evaluate(() => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const els = Array.from(root.querySelectorAll('button, div, span, a')).filter(el =>
    el.offsetParent !== null && el.childElementCount <= 2 && el.textContent.trim() === '保存草稿');
  if (!els.length) return 'NOT_FOUND';
  els[els.length - 1].click();
  return 'save-clicked';
});
```

保存成功的信号（**没有 toast 也别慌**）：inner text 顶部出现“**已保存**”状态，底部“保存草稿/手机预览”按钮变灰（无未保存更改）。保存后**必须回草稿箱验证**：goto `https://channels.weixin.qq.com/platform/post/draftListManager`，wujie inner text 应含新草稿描述开头和当前时间戳，再截图确认。**草稿确认落盘（草稿箱可见）之前绝不导航离开编辑器**——未保存时去 create 页会开出全新空编辑器，已传视频和已填内容全丢，只能整个重做（EP024 实测代价：多传一遍 182MB）。

### 5.5 声明原创 / 活动（可选，按用户要求）

- **声明原创**：点表单里“声明原创”勾选框 → 弹出“原创权益”弹层 → 勾“我已阅读并同意《原创声明须知》…”（复合文本节点，evaluate 找不到叶子，直接按截图坐标点勾选框）→ 橙色“声明原创”按钮激活后点击 → 主表单勾选框变选中。保存后生效。
- **活动**：下拉默认只有“不参与活动”（默认城市每期可能不同：广州市/新加坡都出现过，按实际文案定位触发器），选项要靠搜索框搜出来。**搜索词用 native setter + input 事件写入，别用 keyboard.insertText**——后者依赖焦点，会间歇性失败，失焦时 Cmd+A 还会全选整页（实测 AI/人工智能/科技/海报 无结果，“设计”只搜到家装类，“AI科普”能搜到一批 AI 主题活动，按期轮换选用）。没有内容对口的就保持“不参与活动”，别强行关联。

### 6. 编辑已有草稿（补封面等人工后续之前）

草稿箱条目没有可用的 ref 时，用 TreeWalker 按文本定位再点“编辑”：

```js
const r = await page.evaluate(() => {
  const root = document.querySelector('wujie-app').shadowRoot;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let node, target = null;
  while ((node = walker.nextNode())) { if (node.textContent.indexOf('<草稿描述片段>') >= 0) { target = node.parentElement; break; } }
  if (!target) return 'NOTEXT';
  const item = target.closest('.post-draft-item') || target.parentElement.parentElement;
  const btn = Array.from(item.querySelectorAll('button, span, a, div')).find(el =>
    el !== item && el.offsetParent !== null && el.childElementCount <= 2 && el.textContent.trim() === '编辑');
  if (!btn) return 'NOBTN';
  btn.click();
  return 'EDIT_CLICKED';
});
```

等编辑器就绪（inner text 出现“保存草稿”）再操作。

## 封面：用 waitForFileChooser 拦截原生选文件（EP037 实测可行）

封面组件确实做了 isTrusted 加固，以下路径全部实测失败且**大多静默无错**：`input.files` 赋值 + change 事件（含 composed）、直调事件监听、合成 drag/drop 带 DataTransfer、`page.setInputFiles`、可信点击后 AppleScript 驱动 OS 文件框（中文输入法吃路径 + cmd+shift+G 误开浏览器查找栏）。

**但 ego-browser 的 `page.waitForFileChooser()` 是唯一可行路径**（bsk/Playwright 没有等价能力，所以旧方案栽在这）：它走 CDP 拦截**浏览器原生文件选择框**，文件由浏览器自己写入、事件全部原生可信，页面侧无从分辨；且不弹 OS 文件框，绕开了 AppleScript 输入法坑。

```js
// 1. 进编辑器 → 点封面预览上的“编辑”打开“编辑封面”弹层
// 2. 布防必须先于点击；坐标从 evaluate getBoundingClientRect 取，wujie 内 ref 点不动
const chooserPromise = page.waitForFileChooser({ timeout: 12000 });
await page.mouse.click(uploadBoxX, uploadBoxY, { label: "click 上传封面" });
const chooser = await chooserPromise;
await chooser.setFiles("/绝对路径/cover-3x4.jpg");   // 3:4 竖版，JPG 更小更稳
// 3. 弹层里点“确认”（同坐标法）→ 顶部 toast“封面已更新”→ 表单封面预览变为新图
// 4. 再点一次“保存草稿”，回草稿箱核对缩略图
```

流程入口：草稿箱 → 该草稿“编辑” → 封面预览下方“编辑” → “上传封面”(+) → 确认。上传后右侧“个人主页卡片预览/分享卡片预览”会即时变图，是直观的成功信号。

**封面可能上传失败（EP046 实测）**：大视频刚传完就传封面，可能弹「封面上传失败，请检查网络后刷新重试」——弹层内直接再点一次“上传封面”重传即可，无需刷新。**点“确认”后按钮会转圈表示正在上传，必须等它转完、弹层自行关闭再继续**；确认过早会静默回退成默认帧（症状：弹层关了但表单“封面预览”变回模糊截帧）——发现回退就重开封面编辑器再传一次，成功后表单预览持续显示新封面。

## 清理

- kill 掉 18765 本地文件服务 job（端口会挡下次）。
- 结尾 `task.handOff()` 把浏览器停在草稿箱（用户要补封面/发表）；确认彻底结束再 `task.finish({ keep: [] })`。
- /tmp 的临时脚本是垃圾，可留可删。

## 避坑清单（实测代价换来的）

1. **wujie shadow DOM** → 一切查询从 `document.querySelector('wujie-app').shadowRoot` 开始；外层查不到元素不是“页面没加载”。
2. **直接 URL 白屏** → /platform/post/create 懒加载不渲染，必须 首页→内容管理→视频→发表视频 走 UI。
3. **wujie 内 ref/text 点击进不去** → 报 “\<wujie-app\> intercepts pointer events”；动作走 evaluate DOM `.click()` 或坐标 `page.mouse.click`，snapshot 只用来观察。
4. **长文案从 evaluate 第二参数传入** → 别把中文文案塞进 heredoc 字面量，转义地狱；一个 evaluate 只收一个 JSON 参数。
5. **描述框非 contenteditable** → `.input-editor` + focus + execCommand insertText；话题另起 insertParagraph 一行。
6. **短标题要 native setter** → 直接 `.value=` 框架不认，必须 `Object.getOwnPropertyDescriptor(...).set` + input/change 事件。
7. **位置弹层两段式坐标点击** → element.click() 幽灵切换（DOM 在、弹层不渲染），page.click 被拦截；先 mouse.click 开弹层，再 evaluate 取坐标 mouse.click 选“不显示位置”，最后读字段文案验证。
8. **位置默认带城市** → 每次都要显式选“不显示位置”。
9. **封面上传只有一条路** → 合成注入全静默失败；唯一可行是 `waitForFileChooser()` + 可信点击“上传封面”（EP037 实测），见“封面”节。
10. **innerText 不含 input 值** → 短标题验证必须读 `input.value`，整页 innerText 会误报失败。
11. **上传验证只看 DOM** → “转发/赞/评论”预览卡 + 100% 稳定；`performance` resource 抓不到上传 POST，别白费劲。
12. **上传后立即检查点保存** → 大文件落盘后再填表，最后再存一次；出意外不重传。
13. **草稿确认落盘前绝不导航离开编辑器** → 未保存就去 create 页 = 全部重来。
14. **大文件上传中页面可能重渲染** → `wujie-app` 短暂为 null、evaluate 报 CDP 类错误时等 20 秒再探，**绝对不要刷新标签**——会毁掉进行中的上传；恢复后视频预览卡还在即成功。
15. **保存成功的信号是“已保存”+按钮变灰** → 不一定有 toast；最终以草稿箱可见为准。
16. **发表是人工终点** → 只点“保存草稿”，结尾 `handOff()` 停在草稿箱；发表链路（扫码验证）不属于本 skill。
17. **登录页“加载失败”是红鲱鱼** → 本地微信客户端探活失败而已；二维码在跨域 iframe 里，handOff 请人扫即可，别点“重试”。
