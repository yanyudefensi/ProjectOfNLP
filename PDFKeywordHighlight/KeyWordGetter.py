# coding:utf-8
import re

from textrank4zh import TextRank4Keyword
from gensim.models import Word2Vec, KeyedVectors


class KeywordGetter:
    def __init__(self, stop_words_file = 'Datas/停用词表.txt', wordVecFilePath = r"/Users/junjiexie/Downloads/Tencent_AILab_ChineseEmbedding_Min.txt"):
        '''
        关键词获取工具
        :param stop_words_file: 自定义关键词列表，未指定则使用默认的关键词列表
        '''
        self.tr4k = TextRank4Keyword(stop_words_file)
        self.word2vec = KeyedVectors.load_word2vec_format(wordVecFilePath, binary=False)
        self.word2vec.init_sims(replace=True)

    def get(self, content: str, num=6, word_min_len=1, window = 2, isContainsSimilarWord = True):
        '''
        获取关键字
        :param content: 文章
        :param num: 希望获取关键字的数量
        :param word_min_len: 允许的关键字最大长度
        :param window: textrank算法的超参数，移动窗口的大小 >=2
        :return: 关键字列表
        '''
        content = self.filter(content)
        self.tr4k.analyze(text=content, window = window)
        keywords = self.tr4k.get_keywords(num=num, word_min_len=word_min_len)
        keywords = [kw['word'] for kw in keywords]

        if isContainsSimilarWord:
            similarWords = []
            words = set([kw['word'] for kw in self.tr4k.keywords])
            for keyword in keywords:
                if keyword in self.word2vec:
                    sws = [sw for (sw, weight) in self.word2vec.similar_by_word(keyword)]
                    sws = [sw for sw in sws if sw in words]
                    similarWords += sws
            keywords += similarWords
        return set(keywords)

    def filter(self, content):
        return '  '.join(re.findall('[\u4e00-\u9fa5]+', content))


if __name__ == "__main__":
    articles = [
        """据专家分析，水马是涡振诱因，虎门大桥结构安全，相关抑振措施正在研究实施中。
相关报道：
虎门大桥竖向位移最大达44.61厘米
中新网北京5月8日电 (记者 孙自法)记者8日从中国地震局获悉，广东省地震局利用强震动监测系统分析“5.5”虎门大桥振动事件，初步结果表明，虎门大桥箱梁主体
结构在本次事件中未受到明显影响。
虎门大桥强震动监测系统测点位置示意图。广东省地震局 供图
5月5日下午，虎门大桥悬索桥桥面发生明显振动，桥面振幅过大影响行车舒适性和交通安全，当晚再次发生异常抖动。广东省地震局布设在虎门大桥上的强震动监测系
统完整记录到此次振动事件中大桥加速度值的变化情况。该局随后迅速组织行业相关单位整理强震动监测系统观测数据，从加速度、位移和结构频谱三个方面，开展大
桥地震安全与健康状况分析评估。
强震动监测系统观测数据显示，从当日13时开始，大桥箱梁竖向加速度和位移监测数据出现较为显著的变化，达到日常振动幅值约2-6倍，竖向位移最大达到44.61厘
米，至当天19时后振动明显减小；从加速度功率谱的变化情况看，大桥箱梁结构主要自振频率在事件前后未发生明显改变，事件过程中振动能量主要集中于0.362赫兹
(Hz)。初步分析结果表明，大桥箱梁主体结构在此次振动事件中未受到明显影响。
强震动监测系统已应用于14项重点工程。广东省地震局 供图
据了解，虎门大桥强震动监测系统是广东省地震局下属单位受广东虎门大桥有限公司委托，于2010年建成，共17测点36通道，测站分别位于桥墩基础、桥塔、主梁等
桥梁关键部位。强震动监测系统装备有自主研发的重大工程地震安全监测与评估软件系统，实现地震、撞击、振动等突发事件的实时报警，并快速判断大桥结构运行健
康状况，服务于重大工程的抗震研究、震(振)后快速评估和日常维护加固。目前，该强震动监测系统已在港珠澳大桥、虎门大桥、新丰江水库大坝、深圳地王大厦等
14项重大工程上示范应用。(完)"
""",

        """韩国N号房创建人godgod被警方逮捕
网易娱乐5月11日报道 据韩媒报道，庆北地方警察厅11日表示，以涉嫌违反《儿童青少年保护法》等，申请了韩国N号房创建人A某的逮捕令。
本月9日，警方对A某进行了传唤调查。调查结果，A某承认自己就是godgod，于是警方对其进行了紧急逮捕。警方表示“目前正在调查中，详细情况会在逮捕令下发后
进行说明。”据悉，A某godgod为24岁男性，以包括未成年人在内的女性为对象，制作性剥削视频，并且在telegram聊天室中进行传播。
        """,

        """
        尹正提礼品袋现身蒋梦婕家 路边打电话向保安问路
2020年05月11日 09:34:31
来源：娱情记事本
0人参与0评论
5月11日，有媒体爆料，近日，尹正穿着低调戴着口罩现身蒋梦婕居住的小区。他手中提着红色礼品袋，边打着电话边疾走，在小区门口还向保安问路后边大步走进小
区。
尹正手提一个红色礼品袋，看起来走得挺着急，一会左看右看，一会原地转圈，还边走边打电话。走到小区门口，尹正好像还向门口的保安打听了一下路线，然后大步
流星走进了小区。
不久前有曾媒体报道，蒋梦婕下飞机直奔尹正家，随后还拿了快递，疑似已经同居。当天蒋梦婕现身机场后，和助理一行人在门口打车。令人意外的是车子居然直奔到
尹正居住的地方，停在了尹正公寓所在小区附近。之后蒋梦婕和助理非常熟练地来到小区保安亭进行登记，期间蒋梦婕还不忘拿一下寄放在保安这里的快递，操作非常
熟练。
        """,

        """新冠检测均阳性！纽约州85名儿童感染不明综合征3人死亡 “隐匿”约6周才有症状
分享到： Evelyn Zhang • 2020-05-11 10:35:41　来源：前瞻网　E513G0
安德鲁·库莫（Andrew Cuomo）最新表示，纽约州发现85例儿童感染“炎症综合征”，症状与中毒性休克综合征和川崎病相似，被怀疑与新冠病毒有关。
更可怕的是，该病症已致3名儿童死亡。科莫也因此指出，这这可能预示着儿童面临大流行病的风险。
而且，这种病症的致死性似乎破显“隐匿”。大多数患病的孩子并未表现出新冠肺炎典型症状，但他们的新冠病毒或抗体检测均呈阳性。医生说，在某些情况下，孩子在
接触病毒后最多需要6周的时间才会出现这种疾病的症状。
起初，纽约先是报告了15例患有罕见病的儿童，这些疾病被怀疑与新冠病毒有关联。孩子们的年龄分布在2-15岁，在4月29日至5月3日期间均已住院。
纽约市卫生部门在一份声明中补充说：“所有患者均主观或测得发烧，超过一半的人报告有皮疹、腹痛、呕吐或腹泻。”
所有15名儿童均接受了新冠检测，其中10人确诊阴性。
当局说，这种综合症类似于川崎病，是一种血管发炎性疾病——儿童发高烧，背部、胸部和腹部出现皮疹，眼睛有血迹，出现手脚肿胀、淋巴腺肿胀以及口唇周围肿胀。
川崎病很罕见。每年大约有3000名儿童被诊断出患有这种疾病。而在美国，有7400万未满18岁的儿童。
川崎病的病因尚不清楚，尽管一些研究论文将其触发因素与病毒感染联系在一起。据美国心脏协会称，它于1960年代首次在日本儿童中被诊断出来，似乎没有传染性
或遗传性。
纽约市卫生部门命令所有那些发现病例的儿科医生对所有15岁以下的患者立即报告病例。卫生部门还敦促儿科医生将患者转介给传染病专家或风湿病学家。
上报的标准是——这些患者发烧持续四天或更长时间，症状与川崎病一致或与中毒性休克综合症相似的症状。
他们希望确保所有其他州都关注该综合征，并密切了解其他一些类似的儿童感染综合征。
尚不清楚该疾病可能与引起新冠肺炎的病毒有什么联系，但目前这种症状在美国纽约州中引起了很多家长孩子的重视。纽约州称，将与纽约基因组研究中心和洛克菲勒
大学合作，以确定病因。
尽管儿童可以传播冠状病毒，但他们感染冠状病毒的可能性要小得多，并且对他们的影响相对较小。英国儿科重症监护协会此前在警告炎症性疾病时说：“ 新冠肺炎
导致的严重疾病在儿童中似乎仍然非常罕见。”
但是，自大流行以来，医生注意到患有川崎病的患者也患有新冠肺炎的情况。已知的最早病例是在加利福尼亚州的一个六个月大的婴儿，他入院时被认为是患上川崎
病，但还被诊断出患有新冠肺炎。该病例报告经过同行评审，预计将发表在《医院儿科》（Hospital Pediatrics）杂志上。
        """,

        """
        肖战最新更博五句话，直言，“我不需要应援”，请过好自己的生活
奶茶娱乐七分甜
发布时间：05-1023:50娱乐达人，优质创作者
追星，要建立在过好自己的生活的基础上，这样的追星才更有意义！
肖战最新更博中，用五句话，六十多个字再次和大家直言了，这次他说，“请你们再一次认真听我说！希望所有人把学业、工作、生活，都放在追星前面。好好学习，认
真工作。尽好自己的责任和义务，遵守职业规范和行业底线。我不需要应援。”
一个感叹号，听他说！而不是听别人说，听他说过好自己的生活，把自己放在首要位置！四个句号，四句话，是他相对他的粉丝说的话，所有人要把自己的学业，工作，
生活放在追星前面，这是他希望我们做到的。
的确，过好自己的“三次元”生活，先爱国家，爱自己，爱家人，好好经营好自己的人生，才是正确的生活之道，只有在过好自己的生活之后，才能更好地去追星。
“尽好自己的责任和义务，遵守职业规范和行业底线”，这句话想必是在对所有人说的，每个人都应该认真履行自己的义务，正确行使自己的权利，这样，我们生活的社
会才会更加有爱，更加和谐。追星并不需要你去做什么违法的，不符合社会秩序的事情，追星是一件快乐的事情，是一件可以给自己带来动力的事情。
肖战这一次直接用六十多个字，五句话来强调自己不需要应援，想必是和之前发生的事情有关，他希望他的粉丝能够理智，能够真正地在过好自己的生活之后再去喜欢
他，有能力再去消费。
肖战一直在告诉他的粉丝要好好学习，好好过好自己的生活，然后再去追星。不过之前是在各种采访和视频中提到，并没有直接更博去说，这一次，他直接说了，希望
所有所有喜欢他的人，想让他更好的人可以真的听进去，真的好好地在过好自己的生活之后，再去喜欢他。
这一次，肖战经历了长达两个多月的黑暗，终于迎光而归，希望他可以更好。希望他就像他所唱的《竹石》中传达出来的精神一般，如翠竹般屹立不倒，更加挺拔。
喜欢他的人，真的要听肖战说，不是听别人说，听他的话，去喜欢他，让大家变得更好。
热爱可抵岁月漫长，彼此保护不是说说而已。希望大家都可以变得更好，和喜欢的肖战一样，既是自己的光，也可以成为别人的光～
        """,
    ]

    keywordGetter = KeywordGetter()     # 使用TextRank4zh自己的默认停用词
    keywordGetter2 = KeywordGetter("Datas/停用词表.txt")

    for i, article in enumerate(articles):
        print(article)
        for win in range(2, 8):
            keywords = keywordGetter.get(article, num = 20, window=win)
            print(i," window =", win, " 关键词:", ", ".join(keywords))
        print()
        for win in range(2, 8):
            keywords = keywordGetter2.get(article, num = 20, window=win)
            print(i," window =", win, " 关键词:", ", ".join(keywords))
        print()
        for win in range(2, 8):
            keywords = keywordGetter2.get(article, num=20, window=win, word_min_len=2)
            print(i, " window =", win, " 关键词:", ", ".join(keywords))
