import copy
import cflw网络设备 as 设备
import cflw网络地址 as 地址
from 网络设备.思科_常量 import *
def f接口字符串(a接口: 设备.S接口)->str:
	s = g接口名称[a接口.m名称]
	for i in range(len(a接口.m序号) - 1):
		s += str(a接口.m序号[i]) + '/'
	s += a接口.m序号[-1]
	if a接口.m子序号:
		s += '.' + str(a接口.m子序号)
	return s
def f接口字符串_复杂(a接口: 设备.S接口)->str:	#支持连续地址
	def f连续(a字符串: str, a范围: range):
		#返回'f0/0.1-f0/0.100'这样子的字符串
		#字符串:'f0/0.',范围:range(1,101)
		v前 = a字符串 + str(a范围.start)
		v后 = a字符串 + str(a范围.stop - 1)
		return v前 + '-' + v后
	#S接口
	s = g接口名称[a接口.m名称]
	for i in range(len(a接口.m序号) - 1):
		s += str(a接口.m序号[i]) + '/'
	if type(a接口.m序号[-1]) == range:	#最后一段是连续的
		return f连续(s, a接口.m序号[-1])
	else:
		s += a接口.m序号[-1]
		if a接口.m子序号:
			if type(a接口.m子序号) == range:	#子序号是连续的
				return f连续(s + '.', a接口.m子序号)
			else:
				s += '.' + str(a接口.m子序号)
		return s
def f路由协议_执行接口命令(a路由, a接口, a命令):	#在路由模式中调用,在接口执行命令
	v命令 = str(a命令)
	v接口类型 = type(a接口)
	if v接口类型 == 设备.I接口配置模式:	#接口是一个模式对象,直接切换模式
		a接口.f切换到当前模式()
		a接口.m设备.f执行命令(v命令)
	elif v接口类型 == 设备.S接口:	#构造模式对像并切换
		v接口 = a路由.m模式栈[1].f模式_接口配置(a接口)
		a接口.f切换到当前模式()
		a接口.m设备.f执行命令(v命令)
	else:
		raise TypeError("无法识别 a接口 的类型")
def f执行模式操作命令(a父模式, a模式, a操作):
	v命令 = ""
	if a操作 == 设备.E操作.e删除:
		if a模式.fg删除命令 != 设备.I模式.fg删除命令:
			v命令 = a模式.fg删除命令()
		else:
			v命令 = a模式.fg进入命令()
	elif a操作 == 设备.E操作.e重置:
		if a模式.fg进入命令 != 设备.I模式.fg进入命令:
			v命令 = a模式.fg进入命令()
	f执行命令操作命令(a父模式, v命令, a操作)
def f执行命令操作命令(a模式, a命令, a操作):
	if not a命令:
		return
	v前面添加 = ""
	if a操作 == 设备.E操作.e删除:
		v前面添加 = c不
	elif a操作 == 设备.E操作.e重置:
		v前面添加 = c默认
	v命令 = copy.copy(a命令).f前面添加(v前面添加)
	a模式.f执行当前模式命令(v命令)
def f生成地址4或接口(a):
	v类型 = type(a)
	if v类型 == str:
		if a.count(".") == 3:	#地址
			return 地址.S网络地址4.fc自动(a)
		elif "/" in a:	#接口
			pass
def f生成地址和掩码4(a地址):
	v地址 = 地址.S网络地址4.fc自动(a地址)
	return "%s %s" % (v地址.fg地址s(), v地址.fg掩码s())
def f生成地址和前缀长度6(a地址):
	v地址 = 地址.S网络地址6.fc自动(a地址)
	return "%s /%d" % (v地址.fg地址s(), v地址.fg前缀长度())
