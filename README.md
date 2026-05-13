# archiveofourown-download-new

AO3文章下载工具，自动识别单章/多章文章

# 项目暂时不可用


由于ao3使用了cloudflare托管质询，没有办法绕过，即使手动通过验证，写入cookies也只能保持5分钟左右有效，但是ao3有速率限制五分钟并不能获取到多少内容，所以这个项目现在的情况是**不能用！！！**

## 使用方法

### 方式一：命令行参数（推荐）

```bash
python ao3download.py --url https://archiveofourown.org/works/123456
```

使用代理：
```bash
python ao3download.py --url https://archiveofourown.org/works/123456 --proxy http://127.0.0.1:11451
```

### 方式二：交互式输入

```bash
python ao3download.py
```
然后按提示输入网址

## 功能特点

- 自动识别单章/多章文章，无需切换脚本
- 支持命令行参数和交互式输入
- 可配置HTTP代理
- 自动清理文件名中的非法字符
- 多章文章包含章节标题

## 依赖

需要Python环境和bs4库：
```bash
pip install beautifulsoup4 requests
```

## Windows自动循环

修改 auto.bat 中的代码，然后运行即可循环下载

## QA

**Q: 遇到525错误怎么办？**
A: 525是Cloudflare的SSL错误，通常是因为AO3服务器最近一直被攻击导致的。建议稍后再试。

**Q: 遇到403错误怎么办？**
A: 403错误通常是因为代理IP太烂被Cloudflare拦截。建议更换代理IP，或直接使用本地IP访问。

**Q: 遇到429错误怎么办？**
A: 429表示请求太频繁，程序会自动睡眠60~90秒后退出，请稍后重新运行。
