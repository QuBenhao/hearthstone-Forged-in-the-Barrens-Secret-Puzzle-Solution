import sys
from collections import deque, defaultdict


def warrior():
    state = [3, 3, 0, 0, 0]
    goal = [0, 0, 3, 3, 1]
    changes = {(0, 1): '人', (0, 2): '人人', (1, 1): '猪人', (1, 0): '猪', (2, 0): '猪猪'}
    explored = set()
    pq = deque()
    pq.append((state, []))
    while pq:
        s, path = pq.popleft()
        if tuple(s) in explored:
            continue
        if s == goal:
            return path
        explored.add(tuple(s))
        for change, val in changes.items():
            if s[-1] == 0:
                t = tuple([s[0] - change[0], s[1] - change[1], s[2] + change[0], s[3] + change[1], 1 - s[-1]])
                p = list(path) + [val]
                if t not in explored and not (t[0] > t[1] != 0 or t[2] > t[3] != 0) \
                        and t[0] >= 0 and t[1] >= 0 and t[2] >= 0 and t[3] >= 0:
                    pq.append((list(t), p))
            else:
                t = tuple([s[0] + change[0], s[1] + change[1], s[2] - change[0], s[3] - change[1], 1 - s[-1]])
                p = list(path) + [val]
                if t not in explored and not (t[0] > t[1] != 0 or t[2] > t[3] != 0) \
                        and t[0] >= 0 and t[1] >= 0 and t[2] >= 0 and t[3] >= 0:
                    pq.append((list(t), p))


def rogue():
    state = [5, 1, 0, 2, 0, 5, 2]
    changes = [[1, 2, 1, -2, 2, 0, -3], [-2, 1, -2, -2, 3, -2, -2], [0, -2, 1, 1, 2, -2, -2], [0, 0, 1, 1, -2, 3, -3],
               [-3, 0, -1, 2, 1, -2, 3], [2, 3, 2, -3, 0, 1, 1], [-2, -2, -1, -3, 0, 3, 1]]
    explored = set()
    pq = deque()
    pq.append((state, []))
    while pq:
        s, path = pq.popleft()
        if tuple(s) in explored:
            continue
        if list.count(s, s[0]) == len(s):
            return path
        explored.add(tuple(s))
        for j, change in enumerate(changes):
            temp = [(s[i] + change[i]) % 10 for i in range(len(s))]
            p = list(path) + [j + 1]
            if tuple(temp) not in explored:
                pq.append((temp, p))
    return []


def druid():
    # 0向左，1向上，2向右，3向下
    # partially observable deterministic planning problem
    init_state, init_direct, init_pos = [9, 99, 999], 1, (0, 0)
    path = []
    curr_state = list(init_state)
    curr_direct = init_direct
    curr_pos = tuple(init_pos)

    # pos -> direct -> 通不通
    maze = defaultdict(dict)

    # Note: 需要一边玩一边填入面前是不是墙的信息，以及是否死亡重置
    while True:
        observation = int(input("请输入你现在观察到中路是否可以走? 0代表不行, 1代表可以, 2代表结束"))
        if observation:
            if observation == 2:
                return path
            maze[curr_pos][curr_direct] = True
        else:
            maze[curr_pos][curr_direct] = False

        print()
        print("当前坐标和方向:", curr_pos, curr_direct)
        print("当前迷宫:")
        print(maze)
        print()

        operator = int(input("请输入你选了哪个门? 0代表左,1代表中间,2代表右边"))
        if curr_state[0] == 0 or curr_state[1] == 0 or curr_state[2] == 0 or (not observation and operator == 1):
            if curr_state[0] and curr_state[1] and curr_state[2]:
                print("这是不可能被允许的操作，注意你的输入，重新开始")
            curr_state = list(init_state)
            curr_direct = init_direct
            curr_pos = tuple(init_pos)
        else:
            if operator == 0:
                path.append("左转")
                curr_direct = (curr_direct - 1) % 4
                curr_state[0] -= 1
            elif operator == 1:
                path.append("前进")
                curr_state[1] -= 1
                if curr_direct == 0:
                    curr_pos = curr_pos[0] - 1, curr_pos[1]
                elif curr_direct == 1:
                    curr_pos = curr_pos[0], curr_pos[1] + 1
                elif curr_direct == 2:
                    curr_pos = curr_pos[0] + 1, curr_pos[1]
                else:
                    curr_pos = curr_pos[0], curr_pos[1] - 1
            else:
                path.append("右转")
                curr_direct = (curr_direct + 1) % 4
                curr_state[2] -= 1


def hunter():
    # 这经典规划问题，完全可以使用经典规划器解决
    # 玩家起手只有10金币，要通过和上面一排的卖家进行各种交易，让下面一排的买家都买到自己想要的东西，到最后，你又刚好只剩下10金币。
    item_dict = {"coin": "金币", "zlys": "治疗药水", "hjjb": "黄金酒杯", "sf": "手斧", "fcdz": "翡翠吊坠", "ymbd": "亚麻绷带",
                 "lmzc": "联盟战锤", "bfcgl": "暴风城干酪", "tsyj": "天使饮剂", "kadwo": "可爱的玩偶", "jensbs": "吉尔尼斯匕首",
                 "aybs": "暗影宝石", "cwzhs": "宠物召唤哨", "hhyj": "活化药剂", "tzbs": "铁质匕首", "hbswg": "红宝石王冠",
                 "zhzq": "智慧之球", "yzyj": "夜之药剂", "zrhd": "侏儒护盾", "lbsmz": "蓝宝石魔杖", "asjz": "奥术卷轴",
                 "jzdmz": "精致的帽子", "fnsj": "愤怒水晶", "yrlz": "永燃蜡烛", "djyj": "地精渔具", "mhhf": "猛虎护符",
                 "dtdpx": "动听的排箫"}

    # 卖家:需要的东西 -> 需要的数量,售卖的东西
    sellers = [{"coin":(2,"zlys"),"sf":(5,"hjjb"),"ymbd":(2,"fcdz"),"bfcgl":(14,"lmzc"),
                "kadwo":(3,"tsyj"),"aybs":(2,"jensbs"),"hhyj":(4,"cwzhs")},
               {"coin":(1,"tzbs"),"bfcgl":(4,"fcdz"),"zlys":(4,"hjjb"),"sf":(22,"hbswg"),
                "yzyj":(4,"zhzq"),"zrhd":(3,"aybs"),"cwzhs":(2,"lbsmz")},
               {"coin":(2,"sf"),"ymbd":(5,"kadwo"),"jzdmz":(8,"asjz"),"fnsj":(1,"tsyj"),
                "fcdj":(5,"yzyj"),"djyj":(4,"yrlz"),"dtdpx":(5,"mhhf")},
               {"coin":(11,"dtdpx"),"hhyj":(1,"ymbd"),"zlys":(49,"jensbs"),"tzbs":(12,"zrhd"),
                "bfcgl":(13,"yzyj"),"asjz":(3,"mhhf"),"hjjb":(3,"lmzc"),},
               {"coin":(25,"asjz"),"sf":(2,"jzdmz"),"zlys":(7,"dtdpx"),"hhyj":(20,"fnsj"),
                "lbsmz":(2,"jensbs"),"hjjb":(10,"zhzq"),"bfcgl":(15,"lbsmz"),},
               {"coin":(3,"hhyj"),"sf":(4,"djyj"),"jzdmz":(5,"lbsmz"),"lmzc":(1,"yrlz"),
                "kadwo":(5,"fnsj"),"dtdpx":(3,"hbswg"),"hjjb":(9,"tsyj"),},
               {"coin":(2,"bfcgl"),"bfcgl":(5,"djyj"),"tzbs":(7,"cwzhs"),"hhyj":(9,"aybs"),
                "hbswg":(1,"jensbs"),"zrhd":(4,"mhhf"),"kadwo":(3,"lmzc"),}]

    # 买家:求购的东西 -> 求购的数量,找回的钱
    buyers = [{"sf":(6,10),"djyj":(2,18),"fnsj":(1,60),}]

    class State:
        def __init__(self, coin, buyers):
            self.buyers = buyers
            self.items = defaultdict(int)
            self.items["coin"] = coin


def main():
    print("战士的解密方法是: ", warrior())
    # print("盗贼的解密方式是: ", rogue())
    # print("德鲁伊的解密方式是: ", druid())
    print("猎人的解密方式是: ", hunter())
    pass


if __name__ == '__main__':
    main()
    sys.exit()
