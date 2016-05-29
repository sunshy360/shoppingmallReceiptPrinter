# coding:utf-8
import json
import os,sys
import time
import Image, ImageFont, ImageDraw
#设置编码
reload(sys) 
sys.setdefaultencoding('utf-8') 

#接收命令行参数 分别为:商品文件路径,折扣文件路径,折扣信息转换表路径,购物清单路径
commoditypath = sys.argv[1]
discountpath = sys.argv[2]
discountConvertpath = sys.argv[3]
shoppinglistpath = sys.argv[4]

#读取购物信息
shoppingFile = open(shoppinglistpath,"rb")
shoppingStr = shoppingFile.read()
shoppingFile.close()

#初始化购物列表,与总价列表[总价,总折扣]
shoppingList = shoppingStr.replace('\'','').replace(' ','').split('[')[1].split(']')[0].split(',')
shoppingSum = [0.0,0.0]

#读取商品信息
commodityFile = open(commoditypath,"rb")
commodityStr = commodityFile.read()
commodityJson = json.loads(commodityStr)
commodityFile.close()

#统计购物单中每样商品数量
shoppingAmountDic = {}
for item in shoppingList:
	tmpList = item.split('-')
	#论个数的商品
	if len(tmpList)==1:
		item = tmpList[0]
		if item in shoppingAmountDic:
			shoppingAmountDic[item] += 1
		else:
			shoppingAmountDic[item] = 1
	#称斤的商品
	else:
		item = tmpList[0]
		noIntAmount = tmpList[1]
		if item in shoppingAmountDic:
			shoppingAmountDic[item] += float(noIntAmount)
		else:
			shoppingAmountDic[item] = float(noIntAmount)

#读取折扣信息
discountFile = open(discountpath,"rb")
discountStr = discountFile.read()
discountJson = json.loads(discountStr)
discountFile.close()

#读取折扣信息转换表
convertFile = open(discountConvertpath,"rb")
convertStr = convertFile.read()
convertJson = json.loads(convertStr)
convertFile.close()

#统计购物单中每样折扣情况
discountDic = {}
for item in shoppingAmountDic.keys():
	for key,value in discountJson.items():
		#此商品正在打折,记录下折扣情况
		if item in value['barcodes']:
			discountDic[item] = convertJson[key]
			break

#设置打印格式
height = 100+len(shoppingAmountDic)*100
width = 800
im = Image.new("RGB", (800, height), (255, 255, 255))
dr = ImageDraw.Draw(im)
font1 = ImageFont.truetype(os.path.join("fonts", os.getcwd()+"/方正准雅宋.ttf"), 30)
font2 = ImageFont.truetype(os.path.join("fonts", os.getcwd()+"/方正准雅宋.ttf"), 25)
font3 = ImageFont.truetype(os.path.join("fonts", os.getcwd()+"/方正准雅宋.ttf"), 20)
#整理小票信息
headline = u"*<ThoughtWorks Shop>购物清单*\n"
ISOTIMEFORMAT = "%Y-%m-%d %X"
curtime = u"时间:"+time.strftime(ISOTIMEFORMAT, time.localtime( time.time())) 
stuff = u"	收银员:001\n"
divide = "-------------------------------------------------------------------------\n"
commodityLineList = []
#计算并打印每样商品的价格
for item,amount in shoppingAmountDic.items():
	#有折扣的商品
	if item in discountDic.keys():
		finalReceiptLine = u"名称：" + commodityJson[item]['name'].encode('utf8') + "，"
		finalReceiptLine += "数量：" + str(amount) + commodityJson[item]['unit'].encode('utf8') + "，"
		finalReceiptLine += "单价：" + str(commodityJson[item]['price']) + "(元)，"
		finalReceiptLine += "小计：" + str(amount*commodityJson[item]['price']*discountDic[item][0]) + "(元)，"
		finalReceiptLine += "优惠：" + str(amount*commodityJson[item]['price']*(1-discountDic[item][0])) + "(元)\n"
		commodityLineList.append(finalReceiptLine)
		shoppingSum[0] += amount*commodityJson[item]['price']*discountDic[item][0]
		shoppingSum[1] += amount*commodityJson[item]['price']*(1-discountDic[item][0])
	#无折扣的商品
	else:
		finalReceiptLine = u"名称：" + commodityJson[item]['name'].encode('utf8') + "，"
		finalReceiptLine += "数量：" + str(amount) + commodityJson[item]['unit'].encode('utf8') + "，"
		finalReceiptLine += "单价：" + str(commodityJson[item]['price']) + "(元)，"
		finalReceiptLine += "小计：" + str(amount*commodityJson[item]['price']) + "(元)\n"
		commodityLineList.append(finalReceiptLine)
		shoppingSum[0] += amount*commodityJson[item]['price']

#整理折扣信息
discountInfo = u"单品打折商品："
for item,itemValue in discountDic.items():
	discountItem = "名称：" + commodityJson[item]['name'].encode('utf8')
	discountItem += " 折扣：" + discountDic[item][1].encode('utf8')
	discountInfo += discountItem + " | "
discountInfo += "\n"

#整理总价信息
sumInfo= u"总计：" + str(shoppingSum[0]) + "(元) 节省：" + str(shoppingSum[1]) + "(元)\n"

#打印小票信息
finalReceipt = headline
finalReceipt += curtime
finalReceipt += stuff
finalReceipt += divide
for item in commodityLineList:
	finalReceipt += item
finalReceipt += divide
finalReceipt += discountInfo
finalReceipt += divide
finalReceipt += sumInfo
finalReceipt += divide
print finalReceipt

#输出小票图片
dr.text((160, 10), headline, font=font1, fill="#000000")
dr.text((40, 50), curtime, font=font2, fill="#000000")
dr.text((550, 50), stuff, font=font2, fill="#000000")
dr.text((0, 75), divide, font=font2, fill="#000000")
for i,item in enumerate(commodityLineList):
	dr.text((30, 100+i*30), item, font=font3, fill="#000000")
newcursor = 100+len(commodityLineList)*30
dr.text((0, newcursor), divide, font=font2, fill="#000000")
dr.text((30, newcursor+25), discountInfo, font=font3, fill="#000000")
dr.text((0, newcursor+50), divide, font=font2, fill="#000000")
dr.text((200, newcursor+75), sumInfo, font=font3, fill="#000000")
dr.text((0, newcursor+100), divide, font=font2, fill="#000000")
 
im.show()
im.save("receipt.png")






'''
print commodityJson[buy]['price']
print str(count)+commodityJson[buy]['unit']
'''
'''
while line:
	line = line.replace('barcode','"barcode"')
	line = line.replace('name','"name"')
	line = line.replace('unit','"unit"')
	line = line.replace('category','"category"')
	line = line.replace('subCategory','"subCategory"')
	line = line.replace('price','"price"')
	print line
	info = json.dumps(line)
	info = json.loads(info)
	print info['name']
	line = commodityFile.readline()
'''	
