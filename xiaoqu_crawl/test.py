import re
ss="https://chongqing.anjuke.com/map/sale/?from=commtitle#l1=29.662608&l2=106.562848&l3=18&commid=555864&commname=%E8%9E%8D%E7%A7%91%E9%87%91%E6%B9%96%E6%B9%BE"
print(re.findall(r'\d+\.\d+',ss))

ss2="https://m.anjuke.com/cq/community/994309/"
print(re.findall(r'\d+',ss2))
ll=[1,2,3,4]
print(ll[1:])
