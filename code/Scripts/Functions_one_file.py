import sys
import os
import subprocess
from srt_to_txt import foo
from texts_to_score import compare_strings

# param 1 - path to project base (read your life folder including) default .
path_to_project = "./"
if len(sys.argv) > 1:
	path_to_project = sys.argv[1]

transcription_cmd = r"java -jar " + path_to_project + r"/code/Sphinx_S2T/out/artifacts/RYL1_jar2/RYL1.jar"

accuracy_file = open(path_to_project + r"code/resources/TrainingData/accuracy_data", 'w')
lm = "default"
lm_path = "resource:/edu/cmu/sphinx/models/en-us/en-us.lm.bin"
#lm_path = r"./lms/Operating_system_r2.lm"
#lm = "all_OS"
input_wav_file = path_to_project + r"code/resources/TrainingData/OperatingSystemsVideos/P1L2_ Introduction to Operating Systems/03 - What is an Operating System.wav"
true_output_path = r"code/resources/TrainingData/OperatingSystemsSubtitles/P1L2_ Introduction to Operating Systems/03 - What is an Operating System.txt"
output_tmp_file = path_to_project + r"code/resources/TrainingData/output_tmp_file"

print(input_wav_file + "\t" + output_tmp_file + "\t" + lm_path)
#subprocess("java", "-jar", "S:/Technion/SemesterE/Project/ReadYourLife/code/Sphinx_S2T/out/artifacts/RYL1_jar2/RYL1.jar")
return_val = os.system(transcription_cmd + ' "' + input_wav_file + '" "' + output_tmp_file + '" "' + lm_path)
print("return val = " + str(return_val))
our_output_path = output_tmp_file
our_output = open(our_output_path, 'r').readlines()
true_output = open(true_output_path, 'r').readlines()
accuracy = compare_strings(true_output, our_output)
print("accuracy =" + str(accuracy))
accuracy_file.write(lm + "\t" + str(accuracy) + "\n")

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

