# sqldesign

## class Depand
### __init__(relydict):
    输入初始依赖关系字典，缺省值为{}
### addrelys(keys,relys)
    新增key对relys的直接依赖关系。
    keys为字段名,可传入单个字段，或可迭代对象。
    relys为被依赖的字段名，可传入单个字段，或可迭代对象。
### delrelys(keys,relys)
    删除key对relys的直接依赖关系。
    keys为字段名,可传入单个字段，或可迭代对象。
    relys为被依赖的字段名，可传入单个字段，或可迭代对象。
### ifrely(key,relys)
    判断key是否可以依赖于relys中的全部或部分元素而确定。
    假如可以，那么返回完全依赖列表。
    否则返回None
### decomp()
    调用已实现的优化程度最高的关系表分解方案。
    当前为decompBC()
### decomp1()
    计算满足第一范式的关系表。
    关系表满足以下条件：
    1.主键字段内部没有递归依赖
### decomp2()
    计算满足第二范式的关系表。
    关系表满足以下条件：
    1.满足第一范式
    2.每个附属字段完全依赖于主键字段
### decomp3()
    计算满足第三范式的关系表。
    关系表满足以下条件：
    1.满足第二范式
    2.附属字段内部没有递归依赖
### decompBC()
    计算满足bc范式的关系表。
    关系表满足以下条件：
    1.满足第三范式
    2.主键字段不依赖于附属字段