#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: nettedfish@qq.com
# function: dzpk 筹码计算公式
# date: 2012-03-02

import os
import sys
import logging
import logging.handlers
import ConfigParser
import datetime

log_level = logging.DEBUG
logger_name = "_dzpk"
log_filename = os.path.dirname(__file__) + "/" + logger_name + ".log"
logger = logging.getLogger(logger_name)
logger.setLevel(log_level)
handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1000000, backupCount=0)
formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - [%(name)s/%(filename)s: %(lineno)d] - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

config = ConfigParser.RawConfigParser()
config.read(os.path.dirname(__file__) + "/info.cfg")

chouma_origin = {}
chouma = {}

chouma_discount = config.getfloat("meta", "chouma_discount")
tax_ratio = config.getfloat("meta", "tax_ratio")
tax_start_point = config.getfloat("meta", "tax_start_point")
food_fee = config.getfloat("meta", "food_fee")
comments = config.get("meta", "comments")
logger.debug("筹码折扣率为: %s 征税起点为: %s 征税税率为: %s 食物费用为: %s 其他信息: %s" % (chouma_discount, tax_start_point, tax_ratio, food_fee, comments))
for key, value in config.items("chouma"):
    chouma_origin[key] = float(value)
logger.debug("筹码原始信息为: %s" % (chouma_origin))

total_chouma = 0
####对筹码打折
for key, value in chouma_origin.items():
    ####原始的筹码,输的总数和赢的总数相加,总和应该为0,否则应该重新清点筹码
    total_chouma = total_chouma + chouma_origin[key]
    chouma[key] = chouma_origin[key] * chouma_discount

if total_chouma != 0:
    print "筹码总和为%s,实际应该为0,请重新清点筹码！" % (total_chouma)
    sys.exit()
else:
    print "筹码总数为0,没有问题！"

#总的纳税额,一开始为0
total_tax = 0

#在没有补贴之前,所有输家一共输掉的
total_loser = 0

##赢家
winner = {}
#输家
loser = {}

for key, value in chouma.items():
    #如果赢的大于征税的起点,那么就要按照税率来纳税
    if value >= tax_start_point:
        #纳税的钱,加到补贴池里面
        total_tax = total_tax + (value-tax_start_point)*tax_ratio*1.0
        #纳税之后,赢家的钱已经可以准确计算出来
        winner[key] = tax_start_point + (value-tax_start_point)*(1-tax_ratio)*1.0
    #如果赢的钱在0到征税起点之间,那么就不用纳税,钱可以直接计算出来
    elif value >=0 and value < tax_start_point:
        winner[key] = value
    ##剩下的情况是输家,要等补贴池的钱计算出来后,才能计算每个输家最终该支付的钱.这里把所有玩家一共输掉的钱计算出来, 便于之后计算补贴的比例
    else:
        total_loser = -value + total_loser

print "在没有补贴的情况下,一共输掉了: %s" % total_loser

#默认情况下,我们都有免费的晚餐。而且晚餐的费用从总的补贴池中扣除.但是如果扣除晚餐后,奖金池为负数,那么晚餐将由各位自己支付
food_is_free = 1

if total_tax < food_fee:
    total_subsidy_for_dispatch = total_tax
    logger.debug("纳税总和不足与支付食物费用,请各位自己支付. 总共纳税: %s 食物费用: %s" % (total_tax, food_fee))
    #此时不再是免费的晚餐
    food_is_free = 0
else:
    total_subsidy_for_dispatch = total_tax - food_fee

if food_is_free:
    print "总共扣掉的税为: %2d, food is free! 食物费用为: %s 可以补贴给输家的金额为: %2d" % (total_tax, food_fee, total_subsidy_for_dispatch)
else:
    print "总共扣掉的税为: %2d, 不足于支付吃饭的钱 %2d, 因此各位需要自己付吃饭的钱!" % (total_tax, food_fee)

for key, value in chouma.items():
    if value < 0:
        ##输家获得的补贴,按照比例计算。
        subsidy_for_loser = (-value*1.0/total_loser)*total_subsidy_for_dispatch
        loser[key] = chouma[key] + subsidy_for_loser
        print "loser: %s 得到的补贴为: %s" % (key, int(subsidy_for_loser))
                
#到现在为止,赢家和输家的钱已经计算出来了,但是不包括晚餐:
print "==========totally==========="

if food_is_free:
    print "food is free. %2d" % (food_fee)
    for key,value in winner.items():
        print "winner: %s, chouma is: %2d 折扣后为: %2d, should get: %2d" % (key, chouma_origin[key], chouma[key], value)
    for key,value in loser.items():
        print "loser: %s, chouma is: %2d 折扣后为: %2d, should get: %2d" % (key, chouma_origin[key],chouma[key], value)
else:
    ##晚餐是自费的情况下,每人都要减去晚餐的钱
    print "food is not free. %2d" % (food_fee)
    food_per_person = 1.0*food_fee/len(chouma)
    for key,value in winner.items():
        print "winner: %s, chouma is: %2d 折扣后为 %2d, should get: %2d" % (key, chouma_origin[key],chouma[key], value-food_per_person)
    for key,value in loser.items():
        print "loser: %s, chouma is: %2d 折扣后为 %2d, should get: %2d" % (key, chouma_origin[key],chouma[key], value-food_per_person)

print comments
print "team building 日期: ", datetime.date.today()
