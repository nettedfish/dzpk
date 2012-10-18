关于德州扑克筹码计算公式
=======

* 安装:
git clone https://github.com/nettedfish/dzpk.git  
或者直接拷贝dzpk.py info.cfg这两个文件到某个文件夹下  
用windows系统的同学,需要先安装python,最好是python2.6或以上的版本  

*修改配置文件info.cfg  
每次活动结束后,修改info.cfg的chouma section下的内容即可.  
输入每位参赛人的姓名和最终的筹码数,运行本工具,即可看到最终的结果.  

* 运行:  
./dzpk.py

* 计算方法说明:  
例如某人甲活动结束后剩下1000筹码,筹码会先进行打折,这里默认是0.6,因此实际的人民币是1000*0.6=600  
然后纳税起点为300,税率为0.5 因此,甲需要纳税: (600-300)*0.5=150 因此甲的1000筹码实际收益为600-150=450  
    所有税收收入都会计入补贴池,首先支付本次活动的饭钱:套餐,零食,啤酒,场地费用等  
    然后按照输家输钱的比例,全部补贴给输家  

通过上述配置,可以把输赢控制在非常合理的范围内,例如超过300的部分纳税90%等等策略.

友谊第一,比赛第二
=====
enjoy yourself!
=====
