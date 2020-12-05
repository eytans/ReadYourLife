# param 1 path to srt
# param 2 path to wav
# param 3 path to out

import sys
import argparse
import time
import wave
from datetime import datetime


def write_frames(output_path, params, frames, frame_count):
    with wave.open(output_path, 'w') as out_wave:
        params = params[0:2] + (params[2], frame_count) + params[4:]
        out_wave.setparams(params)
        out_wave.writeframes(frames)


def get_times_and_output_from_srt(srt_path):
    times_texts = []
    with open(srt_path, 'r') as srt_file:
        srt_lines = srt_file.readlines()
        for i in range(len(srt_lines)):
            if i % 4 == 1:
                line = srt_lines[i].replace(',', '.')
                timestart = time.strptime(line.split('-->')[0].strip(), '%H:%M:%S.%f')
                timeend = time.strptime(line.split('-->')[1].strip().replace('\n', ''), '%H:%M:%S.%f')
            if i % 4 == 2:
                text = srt_lines[i]
                times_texts.append(((timestart, timeend), text))
    return times_texts


def timedelta_milliseconds(td):
    return td.days*86400000 + td.seconds*1000 + td.microseconds/1000


def read_frames_from_to(in_wave, time_from, time_to):
    from_datetime = datetime.fromtimestamp(time.mktime(time_from))
    to_date_time = datetime.fromtimestamp(time.mktime(time_to))
    milliseconds = timedelta_milliseconds(to_date_time - from_datetime)
    print(milliseconds)
    frame_count = round(milliseconds*(in_wave.getframerate()/1000))
    return in_wave.readframes(frame_count), frame_count


def split_wav_to_params_frames_frames_len(times_text, wav_path):
    results = []
    with wave.open(wav_path, 'r') as in_wave:
        params = in_wave.getparams()
        previous_end = time.strptime('0:0:0.0', '%H:%M:%S.%f')
        for (starttime, endtime), text in times_text:
            if starttime < previous_end:
                print("ERROR, bad timings")
                starttime = previous_end
            else:
                # throw unneded frames
                read_frames_from_to(in_wave, previous_end, starttime)
            # append frames, text
            frames, frames_len = read_frames_from_to(in_wave, starttime, endtime)
            print(frames_len)
            results.append((frames, frames_len, text))
            previous_end = endtime
    return params, results


def main():
    args_parser = argparse.ArgumentParser(description='split wav by srt timings abnd extract srt text')
    args_parser.add_argument('srt', help='path to srt file')
    args_parser.add_argument('wav', help='path to wav file')
    # args_parser.add_argument('out', help='path to out folder. text will be saved by srt name. wav by wav')
    args = args_parser.parse_args(sys.argv[1:])

    # get split times and relevent text
    times_text = get_times_and_output_from_srt(args.srt)
    # now split wav file into multiple small files by time frames and create relevant output
    params, results = split_wav_to_params_frames_frames_len(times_text, args.wav)

    for i in range(len(results)):
        i += 1
        write_frames(args.wav[:-4] + '_out' + str(i) + '.wav', params, results[i-1][0], results[i-1][1])
        with open(args.srt[:-4] + '_out' + str(i) + '.txt', 'w') as out_txt:
            out_txt.write(results[i-1][2])


if __name__ == '__main__':
    main()
