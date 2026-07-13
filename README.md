# format-content

`format-content` 是一个可独立安装的 Agent Skill：把 Markdown 文章按固定的「红白色系」排成微信公众号兼容 HTML，并生成一份可直接复制富文本的浏览器预览页。

它只负责排版，不改写文章的实质内容，不选择或生成其他主题，也不会调用微信 API、创建草稿或自动发布。

## 安装

```bash
npx skills add https://github.com/BruceL017/format-content
```

## 支持范围

支持：

- 请求中直接提供的 Markdown；直接粘贴时固定使用输出文件名 `article`。
- 可读取、非空且扩展名为 `.md` 的单篇文章。

不支持：Word（`.doc`/`.docx`）、PDF、TXT、HTML/富文本、无结构纯文本、其他主题、普通网页生成、文章实质改写和微信公众号发布。

## 使用示例

```text
请使用 $format-content，把 /work/article.md 排成微信公众号 HTML。
```

Skill 会固定读取仓库中的红白主题和通用组件，解析文章结构，按文章类型选择组件配方，装配并校验干净正文，再生成预览页。

## 输出

输入 `/work/article.md` 时，成功执行只产生以下两个交付文件：

| 文件 | 用途 |
|---|---|
| `/work/article_排版_红白色系(red-white).html` | 纯 `<section>…</section>` 正文片段，用于校验和手动复制兜底 |
| `/work/article_排版_红白色系(red-white)_预览.html` | 完整浏览器预览页，右上角提供“复制到公众号”按钮 |

`.md` 文件使用去掉扩展名后的 basename；直接粘贴 Markdown 时使用默认 stem `article`，因此输出同样是上表中的两个文件名。

打开预览页，点击“复制到公众号”，再粘贴到微信公众号编辑器即可。复制目标只包含已经校验的正文片段，不包含预览页的按钮或脚本。

## 验证保证

Skill 在生成预览前必须对干净正文运行：

```bash
python3 /absolute/path/to/format-content/scripts/validate_gzh_html.py /work/article_排版_红白色系\(red-white\).html
```

只有校验输出同时达到 `ERROR × 0` 和 `WARNING × 0` 才会继续包装预览。校验脚本在只有 warning 时仍可能返回退出码 0，因此 Skill 还会检查诊断文本；不能清零时会停止，不会生成预览或宣称完成。

组件库本身可用以下命令检查：

```bash
python3 scripts/component_lint.py .
```

## 来源与许可

本项目是 [isjiamu/gzh-design-skill](https://github.com/isjiamu/gzh-design-skill) 的修改版精简提取，基于上游提交 `ba1f4175519b481cb3566616c9e5178705067904`，保留红白主题、通用组件、校验脚本和复制预览机制，并移除了非 Markdown 输入归一化、主题选择/生成及其他主题支持。

上游版权声明与 GNU Affero General Public License v3 or later 已保留。完整许可见 [LICENSE](LICENSE)，修改与保留文件说明见 [NOTICE](NOTICE)。
