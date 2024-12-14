from flask import Flask, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Initialize the S3 client
s3_client = boto3.client('s3')
BUCKET_NAME = 'myreelsbucket'  # Replace with your bucket name


@app.route('/list_videos', methods=['GET'])
def list_videos():
    """
    List all video files in the S3 bucket and return their public URLs.
    """
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        if 'Contents' not in response:
            return jsonify({'videos': []})  # No objects in the bucket

        videos = []
        for obj in response['Contents']:
            video_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{obj['Key']}"
            videos.append(video_url)

        return jsonify({'videos': videos})

    except ClientError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_video/<filename>', methods=['GET'])
def get_video(filename):
    """
    Generate a presigned URL to securely download a video.
    """
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': filename},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        return jsonify({'url': url})

    except ClientError as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
