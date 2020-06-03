def set_recommender(module):
    global Recommender
    Recommender = module


def shuffle():
    music = Recommender.recommend()
    return music