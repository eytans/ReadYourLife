import sys
import os
import subprocess
from srt_to_txt import foo
from texts_to_score import compare_strings

src_dir = sys.argv[1]
transcription_cmd = r"java -jar S:\Technion\SemesterE\Project\ReadYourLife\code\Sphinx_S2T\out\artifacts\RYL1_jar2\RYL1.jar"

accuracy_file = open(r"S:\Technion\SemesterE\Project\TrainingData\accuracy_data", 'w')
for root, dirs, files in os.walk("lms", topdown=False):
    for lm in files:
        lm_path = os.path.join(root, lm)
#lm_path = "resource:/edu/cmu/sphinx/models/en-us/en-us.lm.bin"
#lm_path = r".\lms\Operating_system_r2.lm"
#lm = "default"
#lm = "all_OS"

        for root, dirs, files in os.walk(src_dir, topdown=False):
            for name in files:
                old_name_plus_path = os.path.join(root, name)

                if name.endswith(".wav"):
                    output_tmp_file = r"S:\Technion\SemesterE\Project\TrainingData\output_tmp_file"
                    name_plus_path = os.path.join(root, name)
                    print(name_plus_path + "\t" + output_tmp_file + "\t" + lm_path)
                    #subprocess("java", "-jar", "S:\Technion\SemesterE\Project\ReadYourLife\code\Sphinx_S2T\out\artifacts\RYL1_jar2\RYL1.jar")
                    return_val = os.system(transcription_cmd + ' "' + name_plus_path + '" "' + output_tmp_file + '" "' + lm_path)
                    print("return val = " + str(return_val))
                    true_output_path = name_plus_path.replace("OperatingSystemsVideos", "OperatingSystemsSubtitles").replace(".wav", ".txt")
                    our_output_path = output_tmp_file
                    our_output = open(our_output_path, 'r').readlines()
                    true_output = open(true_output_path, 'r').readlines()
                    accuracy = compare_strings(true_output, our_output)
                    accuracy_file.write(lm + "\t" + name + "\t" + str(accuracy) + "\n")

accuracy_file.close()

                #If I want to change files names
                #fixed_name = '_'.join(name.split(" "))
                #new_name_plus_path = os.path.join(root, fixed_name)
                #os.rename(old_name_plus_path, new_name_plus_path)

                #If I wat to create a txt for each srt
                #if name.endswith(".srt"):
                #    new_name_plus_path = old_name_plus_path.replace(".srt", ".txt")
                #    foo(old_name_plus_path, new_name_plus_path)

                #Mp4 to wav
                # if name.endswith(".mp4"):
                    # new_name = name.replace(".mp4", ".wav")
                    # new_name_plus_path = os.path.join(root, new_name)
                    # if not os.path.exists(new_name_plus_path):
                        # os.system(r"S:\Technion\SemesterE\Project\TrainingData\ffmpeg.exe" + ' -i "'  + old_name_plus_path + '" -vn "' + new_name_plus_path + '"')

            # for name in dirs:
            #     print(os.path.join(root, name))
            #     #If I want to change files names
            #     fixed_name = '_'.join(name.split(" "))
            #     old_name_plus_path = os.path.join(root, name)
            #     new_name_plus_path = os.path.join(root, fixed_name)
            #     os.rename(old_name_plus_path, new_name_plus_path)

