# python3.8
# %%
import argparse
import io
import os
# Value for the credentials json Path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials/google_cred.json"


def video_detect_text(path, topn: int):
    """Detect text in a local video."""
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    video_context = videointelligence.VideoContext()

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": input_content,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    # Use list comprehension to get the text and the number of frames
    top_phrases = sorted([(text_annotation.text, len(text_annotation.segments[0].frames))
                         for text_annotation in annotation_result.text_annotations], key=lambda x: x[1], reverse=True)[:topn]

    # Print results
    print("\nLas frases que más aparecen en el video son:")
    for phrase in top_phrases:
        print(f"{phrase[0]}: x{phrase[1]} frames")


def select_video(vid):
    import glob
    import os
    list_of_files = glob.glob(f'./videos/{vid}.*')
    return None if not list_of_files else max(list_of_files, key=os.path.getctime)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-vid', '--vid', help='video_id')
    parser.add_argument('-top', '--top', help='top n fragments')
    args = parser.parse_args()
    print(f"video_id: {args.vid}, top: {args.top}")
    video_file = select_video(args.vid)
    if video_file:
        print(f'More recent file: {video_file}')
        video_detect_text(video_file, int(args.top))
    else:
        print(f'No videos with name: {video_file}')

# %%


if __name__ == '__main__':
    main()
