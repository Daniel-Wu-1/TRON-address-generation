# TRON-number-generation
## TRON靓号生成/波场靓号生成/USDT钱包靓号生成器/可以完全离线运行/完全免费
- 可生成完全自定义的开头和结尾，例如：TNT.....Love
### 下载链接：
https://github.com/Daniel-Wu-1/TRON-number-generation/releases/download/Tron%E9%9D%93%E5%8F%B7%E7%94%9F%E6%88%90%E5%99%A8/default.exe

- 技术交流：飞机Telegram[@jiutong9999](https://t.me/jiutong9999)

> 偶然发现一件事，也就是当已生成数量超过2,147,483,647次后会显示负数，这只是个显示错误，实际并不影响软件运行效果，原因是当前计数器使用了32位有符号整数，所以当生成地址数量超过2,147,483,647次时会发生溢出。可以改用64位有符号整数类型，解决方式是将源代码中的counter = Value('i', 0)替换为counter = Value('q', 0)，这样最大值就会提高到9,223,372,036,854,775,807，因为不影响实际功能所以懒得改了，完美主义者可自行修改代码
