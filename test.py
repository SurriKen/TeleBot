import moviepy.editor as mp

clip = mp.VideoFileClip("temp/video.mp4")
print(clip.fps, clip.duration, int(clip.fps * clip.duration) % 60)
process_time = clip.fps * clip.duration * 0.035
print(f" (About {process_time // 60} min {round(process_time % 60, -1)} sec)")
resize = 360 / clip.size[1] if clip.size[1] > 360 else None

import ffmpeg

vid = ffmpeg.probe("temp/video.mp4")
print(vid['format']['size'])
limit = 50 * 1025 * 1024
print(limit)

x = {
    'streams': [
        {'index': 0, 'codec_name': 'h264', 'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10',
         'profile': 'Main', 'codec_type': 'video', 'codec_tag_string': 'avc1', 'codec_tag': '0x31637661',
         'width': 1280, 'height': 720, 'coded_width': 1280, 'coded_height': 720, 'closed_captions': 0,
         'film_grain': 0, 'has_b_frames': 1, 'sample_aspect_ratio': '1:1', 'display_aspect_ratio': '16:9',
         'pix_fmt': 'yuv420p', 'level': 31, 'color_range': 'tv', 'color_space': 'bt709', 'color_transfer': 'bt709',
         'color_primaries': 'bt709', 'chroma_location': 'left', 'field_order': 'progressive', 'refs': 1,
         'is_avc': 'true', 'nal_length_size': '4', 'id': '0x1', 'r_frame_rate': '24/1', 'avg_frame_rate': '24/1',
         'time_base': '1/12288', 'start_pts': 0, 'start_time': '0.000000', 'duration_ts': 2851840,
         'duration': '232.083333', 'bit_rate': '877666', 'bits_per_raw_sample': '8', 'nb_frames': '5570',
         'extradata_size': 43,
         'disposition': {
             'default': 1, 'dub': 0, 'original': 0, 'comment': 0, 'lyrics': 0,
             'karaoke': 0, 'forced': 0, 'hearing_impaired': 0, 'visual_impaired': 0, 'clean_effects': 0,
             'attached_pic': 0, 'timed_thumbnails': 0, 'captions': 0, 'descriptions': 0, 'metadata': 0, 'dependent': 0,
             'still_image': 0
         },
         'tags': {'creation_time': '2021-02-02T09:32:59.000000Z', 'language': 'und',
                  'handler_name': 'ISO Media file produced by Google Inc. Created on: 02/02/2021.',
                  'vendor_id': '[0][0][0][0]'
                  }
         },
        {
            'index': 1, 'codec_name': 'aac', 'codec_long_name': 'AAC (Advanced Audio Coding)', 'profile': 'LC',
            'codec_type': 'audio', 'codec_tag_string': 'mp4a', 'codec_tag': '0x6134706d', 'sample_fmt': 'fltp',
            'sample_rate': '44100', 'channels': 2, 'channel_layout': 'stereo', 'bits_per_sample': 0, 'id': '0x2',
            'r_frame_rate': '0/0', 'avg_frame_rate': '0/0', 'time_base': '1/44100', 'start_pts': 0,
            'start_time': '0.000000', 'duration_ts': 10234880, 'duration': '232.083447', 'bit_rate': '127999',
            'nb_frames': '9995', 'extradata_size': 16,
            'disposition': {
                'default': 1, 'dub': 0, 'original': 0, 'comment': 0, 'lyrics': 0, 'karaoke': 0, 'forced': 0,
                'hearing_impaired': 0, 'visual_impaired': 0, 'clean_effects': 0, 'attached_pic': 0,
                'timed_thumbnails': 0, 'captions': 0, 'descriptions': 0, 'metadata': 0, 'dependent': 0,
                'still_image': 0
            },
            'tags': {
                'creation_time': '2021-02-02T09:32:59.000000Z', 'language': 'eng',
                'handler_name': 'ISO Media file produced by Google Inc. Created on: 02/02/2021.',
                'vendor_id': '[0][0][0][0]'
            }
        }
    ],
    'format': {
        'filename': 'temp/video2.mp4', 'nb_streams': 2, 'nb_programs': 0,
        'format_name': 'mov,mp4,m4a,3gp,3g2,mj2', 'format_long_name': 'QuickTime / MOV',
        'start_time': '0.000000', 'duration': '232.083415', 'size': '29278732', 'bit_rate': '1009248',
        'probe_score': 100,
        'tags': {
            'major_brand': 'mp42', 'minor_version': '0', 'compatible_brands': 'isommp42',
            'creation_time': '2021-02-02T09:32:59.000000Z'
        }
    }
}
