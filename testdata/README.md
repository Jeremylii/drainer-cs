O2T复制的测试环境准备
-----------
准备好一套DDL完整对应的Tidb和Oracle环境

表结构DDL准备的操作步骤
--------
- 从QA的测试环境通过mysqldump导出建表DDL和数据DML
- 将Mysql/Tidb语法的DDL转换为Oracle语法
- 使用Navicat工具的数据传输功能实施
- 将Oracle建表语句导出成SQL文本，方便后续环境部署
- 测试Drainer时，手工执行mysqldump导出的数据Insert SQL语句，验证Drainer复制
- 使用Sync-diff工具对比Tidb-Oracle端的数据一致性

现有测试数据种类
--------
- QA的coms测试库，2.9w张表，数据类型、表类型完整
- 杭银的测试库，5k张表
- Aurora的测试库，3张宽表，数据类型全覆盖
- 北银金融的findpt压测程序，模拟银行核心交易，测试事务、并发、交易连续性

