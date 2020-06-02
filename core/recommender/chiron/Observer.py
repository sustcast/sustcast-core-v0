import importlib.util
import time
import random

spec = importlib.util.spec_from_file_location("CsvUtils", "../../utils/CsvUtils.py")
CsvUtils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CsvUtils)

spec = importlib.util.spec_from_file_location("YoutubeUtils", "../../utils/YoutubeUtils.py")
YoutubeUtils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(YoutubeUtils)

music_list_csv_path = "../../database/dataset/chiron-dataset/music_list.csv"
music_view_csv_path = "../../database/dataset/chiron-dataset/music_views.csv"

TAG = ">> OBSERVER <<"


def observe():
    music_list = CsvUtils.readDataFromCsv(music_list_csv_path)

    updated_dataset = music_list
    updated_dataset[0]["view"] = ""
    updated_dataset[0]["time"] = ""
    updated_dataset[0]["yt_id"] = ""

    i = 0
    l = len(music_list)

    print(TAG),
    print("started observing " + str(l) + " musics.........")

    while i < l:
        music = music_list[i]
        yt_id = YoutubeUtils.getYtIdFromMusicName(music['artist'] + " - " + music["title"])

        if len(yt_id) > 0:
            yt_view, yt_duration = YoutubeUtils.getDuration_n_ViewsFromId(yt_id)

            updated_dataset[i]["view"] = yt_view
            updated_dataset[i]["time"] = yt_duration
            updated_dataset[i]["yt_id"] = yt_id

        time.sleep(random.random())
        i += 1

    CsvUtils.writeDataToCsv(music_view_csv_path, updated_dataset)

    print(TAG),
    print("completed")


observe()
