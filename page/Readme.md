## 文件说明
`page.py` 为模拟查询页表的程序，`physical_addr_content.txt` 为物理地址的数据，`output.txt` 为输出文件
## 写代码的时候犯的错误
1. 取 PDE contents 和 PTE contents 的时候忘了把有效位抹去
2. 对移位操作符和按位与操作符的优先级不熟悉，也没加括号