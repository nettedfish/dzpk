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

chouma_discount = 0.6

##税率 税率为50%，超过征税起点的部分，将拿出50%补贴给输家
tax_ratio = 0.5

##征税的起点，为200元
tax_start_point = 200

chouma_origin = {}
chouma = {}

###############只需要修改如下的部分  如果某人没有参与游戏，就不要出现在下面。因为吃饭的钱是按照人头来计算的
chouma_origin["qipan"] = 1010
 
chouma_origin["jiangdong"] = -540+40
chouma_origin["zhikai"] = -260+40

 
chouma_origin["zefeng"] = -1315+45

chouma_origin["yinggang"] = 980


food_for_free = 120

###############只需要修改上面的部分

total_chouma = 0

####对筹码打折，现在的折扣是0.6
for key, value in chouma_origin.items():
        ####原始的筹码，输的总数和赢的总数相加，总和应该为0，否则筹码清点有误
        total_chouma = total_chouma + chouma_origin[key]
        chouma[key] = chouma_origin[key] * chouma_discount

if total_chouma != 0:
        print "筹码总和为%s，实际应该为0，请重新清点筹码！" % (total_chouma)
        sys.exit(0)
else:
        print "筹码总数为0，没有问题！"

#总的奖金池，一开始为0
total_bonus = 0

#在没有补贴之前，所有输家一共输掉的钱
total_loser = 0

##赢家
winner = {}
#输家
loser = {}

for key,value in chouma.items():
        #如果赢的钱大于征税的起点，那么就要按照税率来纳税
        if value >= tax_start_point:
                #完税的钱，加到奖金池里面
                total_bonus = total_bonus + (value-tax_start_point)*tax_ratio*1.0
                #完税之后，赢家的钱已经可以准确计算出来
                winner[key] = tax_start_point + (value-tax_start_point)*(1-tax_ratio)*1.0
        #如果赢的钱在0到征税起点之间，那么就不用纳税，钱可以直接计算出来
        elif value >=0 and value < tax_start_point:
                winner[key] = value
        ##剩下的情况是输家，要等奖金池的钱计算出来后，才能计算每个输家最终该支付的钱.这里把所有玩家一共输掉的钱计算出来，
        ####便于之后计算补贴的比例
        else:
                total_loser = -value + total_loser

print "在没有补贴的情况下，一共输掉了: %s" % total_loser

#默认情况下，我们都有免费的晚餐。而且晚餐的费用从总的奖金池中扣除.但是如果扣除晚餐后，奖金池为负数，那么晚餐将由各位自己支付
food_is_free = 1

if total_bonus < food_for_free:
        total_bonus_for_dispatch = total_bonus
        ####此时不再是免费的晚餐
        food_is_free = 0
else:
        total_bonus_for_dispatch = total_bonus - food_for_free

if food_is_free:
        print "总共扣掉的税为： %2d, food is free! 实际可以派发的奖金为：%2d" % (total_bonus,total_bonus_for_dispatch)
else:
        print "总共扣掉的税为：%2d, 不足于支付吃饭的钱 %2d，因此各位需要自己付吃饭的钱！" % (total_bonus, food_for_free)


for key,value in chouma.items():
        if value < 0:
                ##输家获得的补贴，按照比例计算。
                bonus_for_loser = (-value*1.0/total_loser)*total_bonus_for_dispatch
                loser[key] = chouma[key] + bonus_for_loser
                print "loser %s got bonus: %2d. should pay: %2d" % (key, bonus_for_loser,loser[key])
                
##到现在为止，赢家和输家的钱已经计算出来了，但是不包括晚餐:

print "\n\n==========totally==========="
print "筹码的折扣为 %s, 征税的起点为 %s, 税率为 %s " % (chouma_discount,tax_start_point,tax_ratio)

check_winner = 0
check_loser = 0

if food_is_free:
        print "food is free. %2d" % (food_for_free)
        for key,value in winner.items():
                print "winner: %s, chouma is： %2d --> %2d, should get: +%2d" % (key, chouma_origin[key], chouma[key], value)
                check_winner = check_winner + value
        for key,value in loser.items():
                print "loser: %s, chouma is： %2d --> %2d, should get: %2d" % (key, chouma_origin[key],chouma[key], value)
                check_loser = check_loser + value
else:
        ##晚餐是自费的情况下，每人都要减去晚餐的钱
        print "food is not free. %2d" % (food_for_free)
        food_per_person = 1.0*food_for_free/len(chouma)
        for key,value in winner.items():
                print "winner: %s, chouma is： %2d --> %2d, should get: +%2d" % (key, chouma_origin[key],chouma[key], value-food_per_person)
                check_winner = check_winner + value-food_per_person
        for key,value in loser.items():
                print "loser: %s, chouma is： %2d --> %2d, should get: %2d" % (key, chouma_origin[key],chouma[key], value-food_per_person)
                check_loser = check_loser + value-food_per_person                
