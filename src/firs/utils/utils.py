import math

def chunk_based_on_number(lst, chunk_numbers):
    n = math.ceil(len(lst) / chunk_numbers)

    chunks = []
    for x in range(0, len(lst), n):
        each_chunk = lst[x: n + x]

        #if len(each_chunk) < n:
        #    each_chunk = each_chunk + [None for y in range(n - len(each_chunk))]
        chunks.append(each_chunk)

    return chunks


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
