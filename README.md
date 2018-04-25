进度汇总：

1.已完成的内容
	a)	实现page_object模式，主要页面已的方法已封装完成，脚本中没有单独的driver方法，增进脚本代码的灵活性，以防页面代码变动带来的极大的维护成本。
	b)	测试报告result展示及优化：抬头信息加入测试人/浏览器，增加错误截图，增加数据统计图表	
	c)	增加邮件自动发送功能
	d)	打包成exe包，但目前只能在自己的环境上运行
	e)	完成规范的脚本多个，涉及主要界面和主要功能
	f)	测试用例参数化,完成参数化脚本61个，设备类型页面的所有测试（除用户设备）
	g)	生成规范的文档
	h)	加入日志系统
2.待优化项目：
	a)	截图放入公共服务器

时间：20170809

内容整理：
lib
	__init__.py
		库标志文件
	data.py
		测试数据，及配置数据
	func.py
		功能类方法，与excel、csv、数据库进行交互
	gen_db.py
		执行该文件生成plms.db数据库文件，并创建表，且从csv文件读取数据插入相应表中
	log.py
		记录日志，在result/log目录生成log.txt文件
	mytest.py
		继承unittest，所有脚本的父类，包含类setUpClass方法和tearDownClass。其他脚本均继承该类
	page.py
		三江智慧云页面的方法封装
	result.py
		生成测试报告，截图，发送邮件
	snatch.py
		执行该脚本可从三江智慧云重新爬取最新数据，并存入csv文件，再执行gen_db.py可生成数据库，并包含这些表，表中的数据从csv导入
result
	存放测试报告
	log
		存放日志
	screenshot
		存放截图
testcase
	存放测试脚本
docs
	bak
		备份
	export
		导出文件的存放的目录
	import
		需要导入的文件存放的目录
	img
		需要上传的图片存放的目录
	plms_data
		从网页中爬取下来的配置数据
		testcase.csv:
			参数化测试的数据
		rights.csv：
			对应页面：系统配置->PLMS权限管理->权限
		resource.csv:
			对应页面：系统配置->PLMS权限管理->资源
		device_type.csv
			对应页面：系统配置->设备类型管理
		classification.csv
			对应页面：系统配置->系统分类管理
	testcase.py
		参数化测试数据