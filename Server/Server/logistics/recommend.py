
def recommend(stu_id, exer_id):
    # 根据学情推荐

    # 若是当前题目做错，需要练习对应知识：
    # strategy 1：推荐当前题目关联知识的其他题目
    # strategy 2：推荐当前题目关联知识的题目（基础）

    # 若是当前题目做对，可以夯实基础：
    # strategy 3：推荐与stu_id做题记录相似的学生在当前知识上做错的题
    # strategy 4：推荐与stu_id做题记录相似的学生在当前题目关联知识的易错题目（基础）
    print (stu_id, exer_id)
