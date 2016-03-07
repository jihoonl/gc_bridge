
def create_feature_list(name, max_result=10):
    f = []
    if type(name) is str:
        f = [{"type":name, "maxResults": max_result}]
    elif type(name) is list:
        if type(max_result) is list:
            f = [{"type":n,"maxResults":m} for n, m in zip(name, max_result)]
        else:
            f = [{"type":n,"maxResults":max_result} for n in name]
    return f
