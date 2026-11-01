# Academic English Mastery

基于 LaTeX 编写的学术英语教材项目，正文采用模块化章节组织，并提供词汇、语法、篇章论证、段落写作蓝图、修改案例和范文选编。

## 构建 PDF

需要 XeLaTeX 及项目所用的中英文字体。运行：

```sh
make pdf
```

生成的文件为项目根目录下的 `academic_english_book.pdf`，中间文件写入 `build/`。运行 `make clean` 可删除这些构建产物。

## 目录

- `main.tex`：主文档，载入各章节。
- `chapters/`：教材正文，共六部分。
- `style/`：页面样式、颜色和练习排版命令。
- `assets/`：配套训练资料及其原始数据。
- `tests/`：结构、边界和应用场景检查脚本。
- `academic_english_training.zip`、`academic_paragraph_and_essay_mastery.zip`：原始资料包。

更详细的项目记录见 [PROJECT.md](PROJECT.md)。
