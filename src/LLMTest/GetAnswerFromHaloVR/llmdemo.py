import openai

# 设置API密钥

openai.api_key = 'your_api_key'


def generate_score(question, correct_answer, system_answer):
    prompt = f'''  

你将收到一个问题、正确答案和模型回答。 

你的任务是通过将模型回答与正确答案进行比较，判断模型回答的准确程度，给出准确程度accuracy。 

其中，accuracy的范围为0-5，模型回答越接近标准答案分数越高。 

评价标准和步骤如下： 

-1.详细阅读提交的问题。 

-2.思考这个问题，并阅读给定的正确答案，确保理解了问题的内容以及正确答案的含义。 

-3.阅读模型的回答。 

-4.比较模型的回答与正确答案，理解模型回答中的信息和正确答案的相似程度以及不同之处。 

-5.评价模型的回答，给出accuracy。如果模型的回答完全正确，无误差，给5分。如果模型的回答部分正确，但有一些信息缺失，可以给予3分。如果模型的回答小部分正确，大部分错误，可以给予1分。如果模型的回答完全错误，或者与给定的正确答案无关，可以给0分。 

-6.根据我的示例对待打分的问答对打分。 

-7.不要给出思考过程，直接给出结果accuracy。 

我的示例如下: 

问题：空间站多功能光学设施的主要任务是什么？ 

正确答案：空间站多功能光学设施的主要任务是大规模天文巡天。空间站多功能光学设施是我国载人航天工程规划建设的大型空间天文望远镜，口径2米，兼具大视场和高像质的优异性能，并具备在轨维护升级的能力。其观测模式包括位置切换观测模式和OTF观测模式，其中OTF观测模式主要用于大面积天区的高效成图观测。 

模型回答：空间站多功能光学设施的主要任务是大规模天文巡天。 

accuracy：3 

待打分的问答对： 

问题:{question} 

正确答案:{correct_answer} 

模型回答:{system_answer} 

模型结果： 

-accuracy： 

'''

    response = openai.ChatCompletion.create(

        model="gpt-3.5-turbo",

        messages=[{"role": "user", "content": prompt}]

    )

    return response['choices'][0]['message']['content']