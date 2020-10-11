# GIL全局解释器锁

## 1 查看引用技术方法：

`sys.getrefcount(a)`

## 2 CPython引入GIL的主要原因

- 设计者为了规避类似内存管理这样复杂竞争风险问题(race condition)
- CPython大量使用C语言库，但大部分C语言库都不是线程安全的。

## 3 绕过GIL的两种思路

- 绕过CPython，使用JPython等别的实现
- 把关键性能代码放到其他语言中实现，比如C++。