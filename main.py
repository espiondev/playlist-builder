import scrapetube
import yt_dlp


def search_yt(query, limit):
    videos = scrapetube.get_search(
        query=query,
        limit=limit,
        sort_by="relevance",
        results_type="video",
    )
    return videos


def count_non_null(list) -> int:
    c = 0
    for i in list:
        if i != None:
            c += 1
    return c


max_duration_mins = 8
# number of search results to get
# if no result meets the duration criteria,
# that search will be skipped.
num_results = 10

skipped_videos = []
output = {"urls": [], "titles": []}
with open("./titles.txt") as vids:
    data = vids.readlines()

counter = 1
for i in data:
    print(f"Searching for {i[:-1]}")
    videos = search_yt(i[:-1], num_results)

    search_results = {"id": [], "title": []}
    for video in videos:
        search_results["id"].append(video["videoId"])
        search_results["title"].append(video["title"]["runs"][0]["text"])

    results_num = len(search_results["id"])

    if results_num == 0:
        print("No results were found")
        skipped_videos.append(i)
        continue

    print(f"Found {results_num} results")

    for v in range(len(search_results["id"])):
        print(
            f"Getting information for result #{counter} (id={search_results['id'][v]}) with yt-dlp"
        )
        print("\n" + "=" * 15)
        with yt_dlp.YoutubeDL() as ydl:
            video_info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={search_results['id'][v]}",
                download=False,
            )
        print("=" * 15 + "\n")
        # check video length

        if video_info["is_live"]:
            print("Video skipped, it is a live stream")
            search_results["id"][v] = None
            search_results["title"][v] = None
            counter += 1
            continue

        if int(video_info["duration"]) > int(max_duration_mins * 60):
            print(
                f"Video skipped: result #{counter} was too long ({video_info['duration']} > {max_duration_mins*60})"
            )
            search_results["id"][v] = None
            search_results["title"][v] = None

        else:
            output["urls"].append(search_results["id"][v])
            output["titles"].append(search_results["title"][v])
            print(f"Video #{counter} added to output")
            break
        counter += 1

    if count_non_null(search_results["id"]) == 0:
        print(f"No valid results for {i} were found")
        skipped_videos.append(i)
    counter = 1
print(
    f"Finished searching for {len(data)} videos | {len(skipped_videos)} searches were skipped"
)

# write results to text files
if len(skipped_videos):
    print(f"Writing {len(skipped_videos)} skipped results to ./results_skipped.txt")
    with open("results_skipped.txt", "w") as skipped:
        for i in skipped_videos:
            skipped.write(i + "\n")

print(f"Writing {len(output['titles'])} titles to ./titles.txt")
with open("results_titles.txt", "w") as titles:
    for i in output["titles"]:
        titles.write(i + "\n")

print(f"Writing {len(output['titles'])} video IDs to ./results_urls.txt")
with open("results_urls.txt", "w") as urls:
    for i in output["urls"]:
        urls.write(i + "\n")
print("Done")
