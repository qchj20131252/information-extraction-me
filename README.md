# 信息提取基线系统-InfoExtractor
## 摘要
InfoExtractor是一个基于Schema约束知识提取数据集（SKED）的信息提取基线系统。 InfoExtractor采用具有p分类模型和so-labeling模型的流水线架构，这些模型都使用PaddlePaddle实现。 p分类模型是多标签分类，其使用具有最大池网络的堆叠Bi-LSTM来识别给定句子中涉及的谓词。 然后在这样的标记模型中采用BIEO标记方案的深Bi-LSTM-CRF网络，以标记主题和对象提及的元素，给出在p分类模型中区分的谓词。 InfoExtractor在开发集上的F1值为0.668。

## 开始
### 环境要求
Paddlepaddle v1.2.0 <br />
Numpy <br />
内存要求10G用于训练，6G用于推断

### Step 1: 安装paddlepaddle
目前我们只在PaddlePaddle Fluid v1.2.0上进行了测试，请先安装PaddlePaddle，然后在[PaddlePaddle主页]((http://www.paddlepaddle.org/))上查看有关PaddlePaddle的更多详细信息。

### Step 2: 下载训练数据，开发数据和schema文件
请从[竞赛网站](http://lic2019.ccf.org.cn/kg)下载训练数据，开发数据和架构文件，然后解压缩文件并将它们放在./data/文件夹中。
```
cd data
unzip train_data.json.zip 
unzip dev_data.json.zip
cd -
```
### Step 3: 获取词汇表文件
从训练和开发数据的字段“postag”中获取高频词，然后将这些高频词组成词汇表。
```
python lib/get_vocab.py ./data/train_data.json ./data/dev_data.json > ./dict/word_idx
```
### Step 4: 训练p分类模型
首先，训练分类模型以识别句子中的谓词。 请注意，如果您需要更改默认的超参数，例如 隐藏层大小或是否使用GPU进行训练（默认情况下，使用CPU训练）等。请修改```/ conf / IE_extraction.conf```中的特定参数，然后运行以下命令：
```
python bin/p_classification/p_train.py --conf_path=./conf/IE_extraction.conf
```
经过训练的p分类模型将保存在文件夹```./ model / p_model```中。

### Step 5: 训练so-labeling模型
在获得句子中存在的谓词之后，训练序列标记模型以识别对应于出现在句子中的关系的s-o对。 <br />
在训练这样的标记模型之前，您需要准备符合训练模型格式的训练数据，以训练如此标记的模型。
```
python lib/get_spo_train.py  ./data/train_data.json > ./data/train_data.p
python lib/get_spo_train.py  ./data/dev_data.json > ./data/dev_data.p
```
要训​​练这样的标签模型，您可以运行：
```
python bin/so_labeling/spo_train.py --conf_path=./conf/IE_extraction.conf
```
经过训练的so-labeling模型将保存在文件夹```./ model / spo_model```中。

### Step 6: 用两个经过训练的模型进行推断
训练结束后，您可以选择经过训练的预测模型。以下命令用于使用最后一个模型进行预测。您还可以使用开发集来选择最佳预测模型。要使用带有演示测试数据的两个训练模型进行推理（在```/。/ data / test_demo.json```下），请分两步执行命令：
```
python bin/p_classification/p_infer.py --conf_path=./conf/IE_extraction.conf --model_path=./model/p_model/final/ --predict_file=./data/test_demo.json > ./data/test_demo.p
python bin/so_labeling/spo_infer.py --conf_path=./conf/IE_extraction.conf --model_path=./model/spo_model/final/ --predict_file=./data/test_demo.p > ./data/test_demo.res
```
预测的SPO三元组将保存在文件夹```./ data / test_demo.res```中。

## 评估
精度、召回率和F1分数是衡量参与系统性能的基本评价指标。在获得模型的预测三元组之后，可以运行以下命令。<br />
考虑到数据安全性，我们不提供别名字典。
```
zip -r ./data/test_demo.res.zip ./data/test_demo.res
python bin/evaluation/calc_pr.py --golden_file=./data/test_demo_spo.json --predict_file=./data/test_demo.res.zip
```

## 讨论
如果您有任何问题，可以在github上提交一个问题，我们会定期回复您。 </br>

##版权和许可
版权所有2019 Baidu.com，Inc。保留所有权利 <br />
根据Apache许可证2.0版（“许可证”）获得许可; 除非符合许可，否则您不得使用此文件。 您可以在此处获得许可副本 <br />
http://www.apache.org/licenses/LICENSE-2.0 <br />
除非适用法律要求或书面同意，否则根据许可证分发的软件将按“原样”分发，不附带任何明示或暗示的担保或条件。 有关管理许可下的权限和限制的特定语言，请参阅许可证。

##附录
在发布的数据集中，句子的字段postag表示句子的分割和词性标注信息。词性标注(PosTag)的缩略语及其对应的词性意义见下表。<br />
此外，数据集的给定分段和词性标注仅是参考，可以用其他分段结果替换。<br />

|POS| Meaning |
|:---|:---|
| n |common nouns|
| f | localizer |
| s | space |
| t | time|
| nr | noun of people|
| ns | noun of space|
| nt | noun of tuan|
| nw | noun of work|
| nz | other proper noun|
| v | verbs |
| vd | verb of adverbs|
| vn |verb of noun|
| a | adjective |
| ad | adjective of adverb|
| an | adnoun |
| d | adverbs |
| m | numeral |
| q | quantity|
| r | pronoun |
| p | prepositions |
| c | conjunction |
| u | auxiliary |
| xc | other function word |
| w | punctuations |


